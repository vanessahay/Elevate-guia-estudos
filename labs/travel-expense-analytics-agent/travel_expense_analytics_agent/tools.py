import json
import os
from typing import Any, Dict, List, Literal
from google import genai
from google.cloud import storage
from google.cloud.alloydb.connector import Connector, IPTypes
from google.genai import types
from pydantic import BaseModel, Field


class ExpenseDocument(BaseModel):
    category: Literal["taxi invoice", "hotel bill", "flight booking"] = Field(
        description="Category of expense: exactly one of 'taxi invoice', 'hotel bill', or 'flight booking'"
    )
    transaction_date: str = Field(description="Transaction date formatted as YYYY-MM-DD")
    amount_usd: float = Field(description="Total amount in USD as float")
    description: str = Field(default="", description="Brief description of the receipt")


def gcs_expense_processor(bucket_url: str = "gs://qwiklabs-gcp-00-ae747d64a28b-cepf/cymbal_group_expenses/") -> List[Dict[str, Any]]:
    """
    Connects to Google Cloud Storage bucket, iteratively inspects every raw travel receipt file (receipts, PDF invoices, images),
    classifies each document into exactly one category ('taxi invoice', 'hotel bill', or 'flight booking'),
    extracts transaction date (YYYY-MM-DD) and amount in USD (float),
    and saves the processed output as travel_receipts.json within the Cloud Storage bucket.

    Args:
        bucket_url: GCS bucket URL (e.g., gs://qwiklabs-gcp-00-ae747d64a28b-cepf/cymbal_group_expenses/ or gs://qwiklabs-gcp-00-ae747d64a28b-cepf/).

    Returns:
        List of dictionaries with file_name, category, transaction_date, and amount_usd.
    """
    if bucket_url.startswith("gs://"):
        path_parts = bucket_url[5:].split("/", 1)
        bucket_name = path_parts[0]
        prefix = path_parts[1] if len(path_parts) > 1 else ""
    else:
        bucket_name = bucket_url
        prefix = ""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    blobs = list(bucket.list_blobs(prefix=prefix))
    if not blobs and prefix:
        blobs = list(bucket.list_blobs())

    project = os.environ.get("GOOGLE_CLOUD_PROJECT", "qwiklabs-gcp-00-ae747d64a28b")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
    genai_client = genai.Client(vertexai=True, location=location, project=project)

    results = []
    for blob in blobs:
        file_name = blob.name.split("/")[-1]
        if not file_name or blob.name.endswith("/") or file_name.endswith(".json") or file_name.endswith(".sql"):
            continue

        content_bytes = blob.download_as_bytes()
        if len(content_bytes) == 0:
            continue

        mime_type = blob.content_type
        if not mime_type or mime_type == "application/octet-stream":
            ext = file_name.lower().split(".")[-1]
            if ext in ["png"]:
                mime_type = "image/png"
            elif ext in ["jpg", "jpeg"]:
                mime_type = "image/jpeg"
            elif ext in ["pdf"]:
                mime_type = "application/pdf"
            elif ext in ["webp"]:
                mime_type = "image/webp"
            else:
                mime_type = "image/png"

        try:
            response = genai_client.models.generate_content(
                model="gemini-3.6-flash",
                contents=[
                    types.Part.from_bytes(data=content_bytes, mime_type=mime_type),
                    "Extract expense information from this document. Classify into exactly one category: 'taxi invoice', 'hotel bill', or 'flight booking'. Extract transaction date as YYYY-MM-DD and amount in USD as float."
                ],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ExpenseDocument,
                )
            )
            data = ExpenseDocument.model_validate_json(response.text)
            results.append({
                "file_name": file_name,
                "category": data.category,
                "transaction_date": data.transaction_date,
                "amount_usd": data.amount_usd,
                "description": data.description
            })
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

    json_str = json.dumps(results, indent=2)

    output_blob_root = bucket.blob("travel_receipts.json")
    output_blob_root.upload_from_string(json_str, content_type="application/json")

    if prefix and prefix != "travel_receipts.json":
        prefix_clean = prefix.rstrip("/")
        output_blob_prefix = bucket.blob(f"{prefix_clean}/travel_receipts.json")
        output_blob_prefix.upload_from_string(json_str, content_type="application/json")

    return results


def alloydb_expense_analytics(year: int = 2025) -> List[Dict[str, Any]]:
    """
    Connects to AlloyDB PostgreSQL database using google-cloud-alloydb-connector with IAM authentication,
    ensures the travel_expenses table is populated, and executes SQL queries to aggregate overall travel expenses
    grouped by team_name and month, calculating total_amount_usd.

    Args:
        year: Year for aggregation (default: 2025).

    Returns:
        List of dictionaries with team_name, month, and total_amount_usd.
    """
    instance_uri = os.environ.get(
        "ALLOYDB_INSTANCE",
        "projects/qwiklabs-gcp-00-ae747d64a28b/locations/us-central1/clusters/cepf-elevate-expenses/instances/cepf-elevate-expenses-primary",
    )
    user = os.environ.get("ALLOYDB_USER", "student-04-1bcca417bfd3@qwiklabs.net")
    db = os.environ.get("ALLOYDB_DATABASE", "postgres")
    password = os.environ.get("ALLOYDB_PASSWORD", "Password01")

    connector = Connector()
    conn = connector.connect(
        instance_uri=instance_uri,
        driver="pg8000",
        db=db,
        user=user,
        password=password,
        enable_iam_auth=True,
        ip_type=IPTypes.PUBLIC,
    )
    cursor = conn.cursor()

    # Check if travel_expenses table exists and has data
    try:
        cursor.execute("SELECT COUNT(*) FROM travel_expenses;")
        count = cursor.fetchone()[0]
        if count == 0:
            raise Exception("Table is empty")
    except Exception:
        # Import travel_expenses table from GCS dump
        storage_client = storage.Client()
        bucket = storage_client.bucket("qwiklabs-gcp-00-ae747d64a28b-cepf")
        blob = bucket.blob("travel_expenses_alloydb_export.sql")
        sql_content = blob.download_as_text()

        copy_rows = []
        in_copy = False
        for line in sql_content.splitlines():
            if line.startswith("COPY public.travel_expenses"):
                in_copy = True
                continue
            if in_copy:
                if line == r"\." or line == "\\.":
                    in_copy = False
                    continue
                parts = line.split("\t")
                if len(parts) == 6:
                    id_val, amount, expense_type, team, expense_date, description = parts
                    desc_escaped = description.replace("'", "''")
                    exp_escaped = expense_type.replace("'", "''")
                    team_escaped = team.replace("'", "''")
                    copy_rows.append(f"({id_val}, {amount}, '{exp_escaped}', '{team_escaped}', '{expense_date}', '{desc_escaped}')")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS public.travel_expenses (
            id integer NOT NULL PRIMARY KEY,
            amount numeric(10,2) NOT NULL,
            expense_type character varying(50) NOT NULL,
            team character varying(50) NOT NULL,
            expense_date date NOT NULL,
            description character varying(255)
        );
        """)
        conn.commit()

        if copy_rows:
            chunk_size = 50
            for i in range(0, len(copy_rows), chunk_size):
                chunk = copy_rows[i:i + chunk_size]
                values_sql = ",\n".join(chunk)
                cursor.execute(f"INSERT INTO public.travel_expenses (id, amount, expense_type, team, expense_date, description) VALUES\n{values_sql};")
            conn.commit()

    query = """
    SELECT 
        team AS team_name,
        EXTRACT(MONTH FROM expense_date)::INTEGER AS month,
        SUM(amount) AS total_amount_usd
    FROM travel_expenses
    WHERE EXTRACT(YEAR FROM expense_date) = %s
    GROUP BY team, EXTRACT(MONTH FROM expense_date)
    ORDER BY team_name, month;
    """
    cursor.execute(query, (year,))
    rows = cursor.fetchall()

    results = []
    for row in rows:
        results.append({
            "team_name": row[0],
            "month": int(row[1]),
            "total_amount_usd": float(row[2])
        })

    conn.close()
    connector.close()

    # Save output to GCS bucket as travel_expenses.json
    try:
        json_str = json.dumps(results, indent=2)
        storage_client = storage.Client()
        bucket = storage_client.bucket("qwiklabs-gcp-00-ae747d64a28b-cepf")
        output_blob = bucket.blob("travel_expenses.json")
        output_blob.upload_from_string(json_str, content_type="application/json")
    except Exception as e:
        print(f"Error uploading travel_expenses.json to GCS: {e}")

    return results
