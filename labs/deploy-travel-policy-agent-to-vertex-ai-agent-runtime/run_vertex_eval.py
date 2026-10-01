import os
import json
import asyncio
import pandas as pd

from google.cloud import aiplatform
from google.cloud.aiplatform.metadata.metadata_store import _MetadataStore
import vertexai
from vertexai.evaluation import EvalTask

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from travel_policy_agent.agent import app

def main():
    # 1. Configuration & GCP Initialization
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        import google.auth
        _, project_id = google.auth.default()
    
    location = "us-central1"
    experiment_name = "cymbal-travel-policy-eval"

    print(f"Project ID: {project_id}")
    print(f"Location: {location}")
    print(f"Experiment Name: {experiment_name}")

    # Set required environment variables for ADK agent runtime & Vertex AI
    os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
    os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"

    # Initialize Vertex AI in region us-central1
    aiplatform.init(project=project_id, location=location, experiment=experiment_name)
    vertexai.init(project=project_id, location=location)

    # Ensure default Vertex AI Metadata Store exists in us-central1
    metadata_store = _MetadataStore.get_or_create(project=project_id, location=location)
    print(f"Vertex AI Metadata Store ensured: {metadata_store.resource_name}")

    # 2. Load evaluation dataset from evaluation.json
    eval_json_path = os.path.join(os.path.dirname(__file__), "evaluation.json")
    with open(eval_json_path, "r") as f:
        eval_data = json.load(f)

    test_cases = eval_data.get("test_cases", [])
    eval_config = eval_data.get("evaluation_config", {})
    metrics_list = eval_config.get("evaluation_metrics", ["groundedness", "instruction_following", "safety"])

    print(f"Loaded {len(test_cases)} test cases from evaluation.json")
    print(f"Evaluation Metrics: {metrics_list}")

    # Create dataset DataFrame for EvalTask
    eval_records = []
    for tc in test_cases:
        eval_records.append({
            "prompt": tc["query"],
            "reference": tc["ground_truth"],
            "instruction": tc.get("evaluation_instructions", "")
        })
    eval_df = pd.DataFrame(eval_records)

    # 3. Agent model function wrapper
    def cymbal_agent_model_fn(prompt) -> str:
        if isinstance(prompt, dict):
            prompt_str = prompt.get("prompt", str(prompt))
        elif hasattr(prompt, "get"):
            prompt_str = prompt.get("prompt", str(prompt))
        else:
            prompt_str = str(prompt)

        async def _run_agent():
            session_service = InMemorySessionService()
            runner = Runner(app=app, session_service=session_service, auto_create_session=True)
            new_msg = types.Content(role="user", parts=[types.Part(text=prompt_str)])
            response_text = ""
            async for event in runner.run_async(new_message=new_msg, user_id="eval_user", session_id="eval_user"):
                if event.content and event.content.parts and event.author != "user":
                    for part in event.content.parts:
                        if part.text:
                            response_text += part.text
            return response_text
        return asyncio.run(_run_agent())

    # 4. Create Vertex AI EvalTask
    eval_task = EvalTask(
        dataset=eval_df,
        metrics=metrics_list,
        experiment=experiment_name
    )

    import time
    timestamp = int(time.time())
    experiment_run_name = f"eval-run-cymbal-travel-policy-{timestamp}"
    print(f"Starting EvalTask execution under experiment '{experiment_name}', run '{experiment_run_name}'...")

    # 5. Execute Evaluation
    eval_result = eval_task.evaluate(
        model=cymbal_agent_model_fn,
        experiment_run_name=experiment_run_name
    )

    print("\nEvaluation Summary Metrics:")
    print(eval_result.summary_metrics)
    print("\nMetrics Table:")
    print(eval_result.metrics_table)

    # 6. Verify and ensure experiment run context in MetadataStore reaches COMPLETE state
    try:
        exp_run = aiplatform.ExperimentRun(
            run_name=experiment_run_name,
            experiment=experiment_name,
            project=project_id,
            location=location
        )
        print(f"Experiment run state: {exp_run.get_state()}")
        if exp_run.get_state() != "COMPLETE":
            exp_run.end_run(state=aiplatform.gapic.Execution.State.COMPLETE)
            print("Experiment run state manually updated to COMPLETE.")
        else:
            print("Experiment run context successfully registered and is in COMPLETE state.")
    except Exception as e:
        print(f"Ensuring run completion check: {e}")
        try:
            aiplatform.end_run()
        except Exception:
            pass

if __name__ == "__main__":
    main()
