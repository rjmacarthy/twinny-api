import uvicorn
import torch
import yaml
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

from model import get_model

from constants import (
    DEVICE,
    EOD,
    FIM_MIDDLE,
    FIM_PREFIX,
    FIM_SUFFIX,
    INFILL,
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
    choices: List[str]


def codegen(payload: Payload) -> str:
    prefix, suffix = (payload.prompt.split(INFILL) + ["", ""])[:2]
    prompt = f"{FIM_PREFIX}{prefix}{FIM_SUFFIX}{suffix}{FIM_MIDDLE}"
    inputs = tokenizer(
        prompt, return_tensors="pt", padding=True, return_token_type_ids=False
    ).to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            do_sample=True,
            temperature=payload.temperature,
            max_new_tokens=payload.max_tokens,
            pad_token_id=tokenizer.pad_token_id,
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)
    start = decoded.find(FIM_MIDDLE) + len(FIM_MIDDLE)
    end = decoded.find(EOD, start) or len(decoded)
    completion = decoded[start:end]

    try:
        if not completion:
            return ""
        if payload.one_line:
            return completion.splitlines()[0] or completion.splitlines()[1]
        return completion
    except:
        return ""



@app.post("/v1/engines/codegen/completions", response_model=CompletionResponse)
async def completions(payload: Payload):
    return CompletionResponse(choices=[codegen(payload)])


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=PORT)
