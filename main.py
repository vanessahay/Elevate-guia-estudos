import os
import logging
import inspect
import json
from fastapi import FastAPI, HTTPException, Request, encoders, responses
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.sessions.base_session_service import GetSessionConfig
from google.adk.agents.run_config import RunConfig, StreamingMode
from google.genai import types
from google.adk.apps import App
from vertexai.agent_engines.templates.adk import AdkApp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cymbal_policy_concierge")

# Import the agent
from app.agent import root_agent

app = FastAPI(title="Cymbal Group Travel Policy Concierge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Session Service, ADK App, and Runner
session_service = InMemorySessionService()
adk_app = App(name="cymbal_policy_concierge", root_agent=root_agent)
runner = Runner(
    agent=root_agent,
    session_service=session_service,
    auto_create_session=True,
    app_name="cymbal_policy_concierge"
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {
        "status": "online",
        "agent": "Cymbal Group Travel Policy Concierge",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        session_config = GetSessionConfig(num_recent_events=20)
        run_config = RunConfig(
            streaming_mode=StreamingMode.NONE,
            get_session_config=session_config
        )
        response_text = ""
        new_message = types.Content(
            role="user",
            parts=[types.Part(text=request.message)]
        )
        
        async for event in runner.run_async(
            new_message=new_message,
            user_id=request.session_id,
            session_id=request.session_id,
            run_config=run_config
        ):
            logger.info(f"Received event from {event.author}: {event.content}")
            if event.content and event.content.parts and event.author != "user":
                for part in event.content.parts:
                    if part.text:
                        response_text += part.text
                        
        return ChatResponse(response=response_text)
    
    except Exception as e:
        logger.error(f"Error during chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Attach Vertex AI Agent Engine Reasoning Engine endpoints
runtime_instance: AdkApp | None = None
streaming_methods: set[str] = set()
sync_methods: set[str] = set()

def get_runtime() -> AdkApp:
    global runtime_instance, streaming_methods, sync_methods
    if runtime_instance is None:
        runtime_instance = AdkApp(app=adk_app)
        runtime_instance.set_up()
        operations = runtime_instance.register_operations()
        streaming_methods = set(operations.get("stream", [])) | set(
            operations.get("async_stream", [])
        )
        sync_methods = set(operations.get("", [])) | set(
            operations.get("async", [])
        )
    return runtime_instance

def resolve_method(class_method: str, *, streaming: bool):
    rt = get_runtime()
    allowed = streaming_methods if streaming else sync_methods
    if class_method not in allowed:
        raise HTTPException(
            status_code=404,
            detail=f"Unsupported reasoning_engine method: {class_method!r}",
        )
    return getattr(rt, class_method)

@app.post("/api/stream_reasoning_engine")
async def stream_reasoning_engine(request: Request) -> responses.StreamingResponse:
    body = await request.json()
    method = resolve_method(body["class_method"], streaming=True)

    async def generator():
        res = method(**(body.get("input") or {}))
        if inspect.isasyncgen(res):
            async for event in res:
                yield json.dumps(event) + "\n"
        else:
            for event in res:
                yield json.dumps(event) + "\n"

    return responses.StreamingResponse(
        content=generator(), media_type="application/json"
    )

@app.post("/api/reasoning_engine")
async def reasoning_engine(request: Request) -> responses.JSONResponse:
    body = await request.json()
    method = resolve_method(body["class_method"], streaming=False)
    kwargs = body.get("input") or {}
    output = (
        await method(**kwargs)
        if inspect.iscoroutinefunction(method)
        else method(**kwargs)
    )
    return responses.JSONResponse(
        content=encoders.jsonable_encoder({"output": output})
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
