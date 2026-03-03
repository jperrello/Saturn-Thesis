# Cognitive Walkthrough: Saturn Server Setup (Sysadmin/IT)
# Each step is documented as a bullet point below.
#
# PREREQUISITE STEPS (shared with traditional):
#
# - Go to openrouter.ai (or any other API key provisioner)
# - Create an account and sign in
# - Go to settings
# - Click API keys
# - Create a new key
# - Copy key and store it somewhere safe
# - Create a .env file
# - Place key in file as OPENROUTER_API_KEY
#
# --- Saturn and traditional methods diverge here ---
#
# SATURN SERVER SETUP STEPS:
#
# - Import os and dotenv to access environment variables
# - Import fastapi, uvicorn for the HTTP server
# - Import httpx for proxying requests to OpenRouter
# - Import subprocess for dns-sd service registration
# - Import socket for finding available ports and local IP
# - Import json for SSE chunk formatting
# - Call load_dotenv() to load .env file
# - Read OPENROUTER_API_KEY from environment
# - Create FastAPI application instance
# - Define /v1/health endpoint returning {"status": "ok", "saturn": true}
# - Define /v1/models endpoint that proxies GET to OpenRouter's /v1/models
# - Define /v1/chat/completions endpoint that proxies POST to OpenRouter
#   - Handle streaming responses with SSE (text/event-stream)
#   - Handle non-streaming responses as plain JSON
# - Write a function to find an available port starting at 8080
# - Write a function to register the service via dns-sd subprocess
#   - Service type: _saturn._tcp
#   - TXT records: version, api_type, priority, deployment, api_base
# - On startup, find port, register service, run uvicorn
#
# Prerequisite steps: 8
# Saturn code steps: 18
# Grand total: 26
#
# Compare to cog_traditional.py: 8 prerequisites + 4 distribution = 12 total
#   (but no centralized service, no discovery, no proxy)
# Compare to cog_sat_package.py: 8 prerequisites + 6 code steps = 14 total

import os
import json
import socket
import subprocess
import atexit

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import uvicorn

load_dotenv()

KEY = os.getenv("OPENROUTER_API_KEY")
BASE = "https://openrouter.ai/api/v1"

app = FastAPI()


@app.get("/v1/health")
def health():
    return {"status": "ok", "service": "cog_saturn", "saturn": True}


@app.get("/v1/models")
async def models():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BASE}/models", headers={"Authorization": f"Bearer {KEY}"})
        return JSONResponse(content=r.json(), status_code=r.status_code)


@app.post("/v1/chat/completions")
async def completions(request: Request):
    body = await request.json()
    streaming = body.get("stream", False)

    headers = {
        "Authorization": f"Bearer {KEY}",
        "Content-Type": "application/json",
    }

    if not streaming:
        async with httpx.AsyncClient() as client:
            r = await client.post(f"{BASE}/chat/completions", json=body, headers=headers, timeout=120)
            return JSONResponse(content=r.json(), status_code=r.status_code)

    async def generate():
        async with httpx.AsyncClient() as client:
            async with client.stream("POST", f"{BASE}/chat/completions", json=body, headers=headers, timeout=120) as r:
                async for line in r.aiter_lines():
                    if line.startswith("data:"):
                        yield f"{line}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


def port(start=8080):
    for p in range(start, start + 100):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", p)) != 0:
                return p
    return start


def register(name, p):
    proc = subprocess.Popen([
        "dns-sd", "-R",
        name,
        "_saturn._tcp",
        "local",
        str(p),
        "version=1.0",
        "api_type=OpenRouter",
        "priority=50",
        "deployment=openrouter",
        f"api_base={BASE}",
    ])
    atexit.register(proc.terminate)
    return proc


if __name__ == "__main__":
    p = port()
    print(f"Starting Saturn server on port {p}")
    register("cog_saturn", p)
    uvicorn.run(app, host="0.0.0.0", port=p)
