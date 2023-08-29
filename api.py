import uvicorn
from fastapi import FastAPI

from abstractions import Payload, CompletionResponse
from generator import codegen


from constants import (
    PORT,
)

app = FastAPI()


@app.post("/v1/engines/codegen/completions", response_model=CompletionResponse)
async def completions(payload: Payload):
    return CompletionResponse(choices=codegen(payload))


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=PORT)
