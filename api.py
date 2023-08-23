import uvicorn
import torch
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from constants import (
    EOD,
    FIM_MIDDLE,
    FIM_PREFIX,
    FIM_SUFFIX,
    device,
    PORT,
    INFILL,
)

from model import get_model

model, tokenizer = get_model()

app = FastAPI()


class Prompt(BaseModel):
    temperature: float = 0.1
    max_tokens: int = 100
    prompt: str


class CompletionResponse(BaseModel):
    choices: List[str]


def get_completion(completion: str) -> str:
    try:
        start = completion.find(FIM_MIDDLE) + len(FIM_MIDDLE)
        stop = completion.find(EOD, start) or len(completion)
        code = completion[start:stop]
        return [code]
    except IndexError:
        return [""]


def infill(prefix, suffix, max_new_tokens, temperature):
    prompt = f"{FIM_PREFIX}{prefix}{FIM_SUFFIX}{suffix}{FIM_MIDDLE}"
    inputs = tokenizer(
        prompt, return_tensors="pt", padding=True, return_token_type_ids=False
    ).to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            do_sample=True,
            temperature=temperature,
            max_new_tokens=max_new_tokens,
            pad_token_id=tokenizer.pad_token_id,
        )
    return get_completion(tokenizer.decode(outputs[0], skip_special_tokens=False))


def codegen(prompt: str, max_tokens: str, temperature: str) -> str:
    prefix, suffix = prompt.split(INFILL)
    return infill(prefix, suffix, max_tokens, temperature)


@app.post("/v1/engines/codegen/completions", response_model=CompletionResponse)
async def completions(prompt: Prompt):
    choices = codegen(prompt.prompt, prompt.max_tokens, prompt.temperature)
    return CompletionResponse(choices=choices)


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=PORT)
