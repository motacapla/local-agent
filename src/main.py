from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional

import json
import asyncio
import uvicorn

from graph import SimpleAgentGraph

app = FastAPI(
    title="API svr for LLM", description="API server for local LLM", version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = SimpleAgentGraph()


class AgentRequest(BaseModel):
    message: str


@app.get("/")
async def root():
    return {"message": "OK"}


@app.post("/agent")
async def process_agent_request(
    request: AgentRequest,
) -> StreamingResponse:
    try:

        async def generate_response():
            events = graph.run(request.message)
            async for event in events:
                data = {"message": json.dumps(event, ensure_ascii=False)}
                yield f"data: {json.dumps(data)}\n\n"
                # if "chatbot" in event:
                #     message = event["chatbot"]["messages"][0].content
                #     data = {"message": json.dumps(message, ensure_ascii=False)}
                #     yield f"data: {json.dumps(data)}\n\n"
                # else:  # tool use
                #     messages = event["tools"]["messages"]
                #     for message in messages:
                #         print(message)
                #         data = {"message": json.dumps("tool use", ensure_ascii=False)}
                #         yield f"data: {json.dumps(data)}\n\n"

        return StreamingResponse(
            content=generate_response(),
            media_type="text/event-stream",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# async def stream_json_example():
#     async def generate_json_data():
#         for i in range(10):
#             data = {"index": i, "message": f"Hello from index {i}"}
#             await asyncio.sleep(1.0)
#             yield f"data:{json.dumps(data)}\n\n"

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
