import uvicorn
import yaml
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from model import get_model, is_llama_model
from completion import get_llama_completion, get_starcoder_completion

from constants import (
    LLAMA_TOKENS,
    STARCODER_TOKENS,
    PORT,
)

model, tokenizer = get_model()

app = FastAPI()

config = yaml.safe_load(open("./config.yml"))


class Payload(BaseModel):
    max_tokens: int = 100
    one_line: bool = True
    prompt: str
    temperature: float = 0.1


class CompletionResponse(BaseModel):
    choices: List


def codegen(payload: Payload) -> str:
    if is_llama_model:
        return get_llama_completion(payload)
    return get_starcoder_completion(payload)


@app.post("/v1/engines/codegen/completions", response_model=CompletionResponse)
async def completions(payload: Payload):
    return CompletionResponse(choices=codegen(payload))


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=PORT)
