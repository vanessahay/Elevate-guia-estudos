# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
from typing import Optional
from google.cloud import storage

from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types

POLICY_BUCKET = "qwiklabs-gcp-00-d6ddd853035d-static-assets-bucket"
POLICY_BLOB = "corporate_travel_policy.txt"
_POLICY_CACHE: Optional[str] = None


def load_policy_document() -> str:
    """Loads the corporate travel policy document from GCS into memory."""
    global _POLICY_CACHE
    if _POLICY_CACHE is not None:
        return _POLICY_CACHE

    try:
        client = storage.Client()
        bucket = client.bucket(POLICY_BUCKET)
        blob = bucket.blob(POLICY_BLOB)
        _POLICY_CACHE = blob.download_as_text()
        return _POLICY_CACHE
    except Exception as e:
        # Fallback to local fallback if available
        local_path = os.path.join(os.path.dirname(__file__), "corporate_travel_policy.txt")
        if os.path.exists(local_path):
            with open(local_path, "r", encoding="utf-8") as f:
                _POLICY_CACHE = f.read()
                return _POLICY_CACHE
        raise RuntimeError(f"Failed to load travel policy from GCS or local file: {e}") from e


def search_travel_policy(query: str) -> str:
    """Searches the Cymbal Group Corporate Travel & Expense Policy Handbook for relevant sections.

    Args:
        query: The search keywords or policy topic (e.g., 'flights', 'lodging', 'receipts', 'meals', 'per diem').

    Returns:
        Matching sections or text snippets from the corporate travel policy document.
    """
    import math
    from collections import Counter

    text = load_policy_document()
    query_terms = [t.strip().lower() for t in query.split() if len(t.strip()) > 1]

    if not query_terms:
        return text[:3000]

    lines = text.split("\n")
    blocks = []
    current_block = []

    for line in lines:
        if line.startswith("====================") or line.startswith("ANNEX ") or re.match(r"^\d+\.\s+[A-Z]", line):
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        current_block.append(line)

    if current_block:
        blocks.append("\n".join(current_block))

    term_block_counts = Counter()
    for b in blocks:
        b_lower = b.lower()
        for term in set(query_terms):
            if term in b_lower:
                term_block_counts[term] += 1

    scored = []
    for b in blocks:
        b_lower = b.lower()
        score = 0.0
        for term in set(query_terms):
            if term in b_lower:
                idf = math.log((len(blocks) + 1) / (term_block_counts[term] + 0.5))
                score += idf * (1.0 + math.log(b_lower.count(term)))
        if score > 0:
            scored.append((score, b))

    scored.sort(key=lambda x: x[0], reverse=True)

    if scored:
        top_blocks = [b for _, b in scored[:5]]
        return "\n\n---\n\n".join(top_blocks)

    return f"No specific section found matching terms: '{query}'. General policy summary:\n\n" + text[:2500]


def get_regional_annex(identifier: str) -> str:
    """Retrieves policy details for a specific Region Code (e.g. R-1001 to R-1150) or Cost Center (e.g. CC-201 to CC-350).

    Args:
        identifier: The region code (e.g., 'R-1001') or cost center code (e.g., 'CC-201').

    Returns:
        The exact rules and limits specified in the corresponding Regional Annex.
    """
    text = load_policy_document()
    clean_id = identifier.strip().upper()

    match = re.search(r"(ANNEX \d+:.*?End of Annex \d+ rules\.)", text, re.DOTALL)
    annexes = re.findall(r"(ANNEX \d+:[\s\S]*?End of Annex \d+ rules\.)", text)

    results = []
    for annex in annexes:
        if clean_id in annex.upper():
            results.append(annex)

    if results:
        return "\n\n---\n\n".join(results)

    return f"No Annex found for region/cost center '{identifier}'. Please check the region code format (e.g., R-1001) or cost center (e.g., CC-201)."


def get_full_travel_policy() -> str:
    """Returns the main overview sections of the Cymbal Corporate Travel Policy Handbook.

    Returns:
        The main overview text covering flights, lodging, meals, ground transport, and expense reporting.
    """
    text = load_policy_document()
    # Return main sections before the annexes
    if "DEPARTMENT SPECIFIC ADDENDUMS & REGIONAL ANNEXES" in text:
        return text.split("DEPARTMENT SPECIFIC ADDENDUMS & REGIONAL ANNEXES")[0]
    return text[:8000]


SYSTEM_INSTRUCTION = """You are the Cymbal Travel Policy Agent, an AI assistant specializing in the Cymbal Group Corporate Travel & Expense Policy Handbook.

Your primary knowledge source is the official corporate policy document available at:
gs://qwiklabs-gcp-00-d6ddd853035d-static-assets-bucket/corporate_travel_policy.txt

Response Guidelines:
1. Always respond clearly, politely, and authoritatively.
2. Ground all answers strictly in the provided policy document. Do not invent or assume external rules.
3. For questions referencing cost centers (CC-xxx) or regions (R-xxxx), inspect the corresponding section in Regional Annexes (ANNEX 1 to 150) using the `get_regional_annex` tool.
4. When stating monetary limits, specify the currency (USD), location tier, and receipt requirements.
5. If an action requires approval (Line Manager, VP, or Regional Director), explicitly highlight it.
6. If the answer cannot be found in the policy document, respond: "This information is not specified in the Cymbal Group Corporate Travel Policy Handbook. Please contact the Global Travel & Expense team for further assistance."
"""

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model="gemini-2.5-flash",
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=SYSTEM_INSTRUCTION,
    tools=[search_travel_policy, get_regional_annex, get_full_travel_policy],
)

app = App(
    root_agent=root_agent,
    name="app",
)

