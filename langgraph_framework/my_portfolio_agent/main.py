"""FastAPI app exposing an endpoint your frontend can call to trigger the agent.

Endpoint: POST /trigger-agent
Body: optional JSON (it will be merged into the agent input payload)

Security: For production, protect this endpoint (API key, token, or restrict by
origin). This example is intentionally simple for local testing.
"""

import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn


load_dotenv()

from langgraph_app.graph import trigger_portfolio_agent

app = FastAPI()


class TriggerBody(BaseModel):
    source: str | None = None

@app.post("/trigger-agent")
async def trigger_agent():
# Basic rate-limiting / abuse protection is not included here. Add as-needed.
    try:
    # You can pass extra metadata from the request to the agent by extending the payload
        response = trigger_portfolio_agent()
        return {"status": "ok", "agent_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)