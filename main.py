import asyncio
import json
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")


class GenerateRequest(BaseModel):
    prompt: str


async def generate_stream(prompt: str) -> AsyncGenerator[str]:
    """
    Stream agent messages as they work on generating the app.
    This is a mock for now - will integrate with real agents later.
    """

    # Mock agent conversation for demo
    agents = [
        {"agent": "PM", "message": "Analyzing requirements..."},
        {"agent": "PM", "message": f"Project: {prompt}"},
        {"agent": "Frontend", "message": "Creating Next.js application structure..."},
        {"agent": "Frontend", "message": "Building components..."},
        {"agent": "Backend", "message": "Setting up API endpoints..."},
        {"agent": "DevOps", "message": "Preparing deployment configuration..."},
    ]

    for msg in agents:
        yield f"data: {json.dumps({'type': 'agent', **msg})}\n\n"
        await asyncio.sleep(1)  # Simulate work

    # Mock success
    yield f"data: {
        json.dumps(
            {
                'type': 'success',
                'message': 'Application deployed successfully!',
                'url': 'https://example.vercel.app',
            }
        )
    }\n\n"


@app.get("/")
async def read_root():
    return FileResponse("static/index.html")


@app.post("/api/generate")
async def generate_app(request: GenerateRequest):
    """
    Generate and deploy an application based on the prompt.
    Returns a streaming response with agent updates.
    """
    return StreamingResponse(
        generate_stream(request.prompt),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
