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


class Payload(BaseModel):
    temperature: float = 0.1
    max_tokens: int = 100
    prompt: str
    one_line: bool = True


class CompletionResponse(BaseModel):
    choices: List[str]


def get_completion(completion: str, one_line: bool) -> str:
    try:
        start = completion.find(FIM_MIDDLE) + len(FIM_MIDDLE)
        stop = completion.find(EOD, start) or len(completion)
        code = completion[start:stop]
        if one_line:
            return [code.splitlines()[0] or code.splitlines()[1]]
        return [code]
    except IndexError:
        return [""]




def codegen(code: str, temperature, max_new_tokens, one_line) -> str:
    prefix, suffix = code.split(INFILL)
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
    return get_completion(tokenizer.decode(outputs[0], skip_special_tokens=False), one_line)


@app.post("/v1/engines/codegen/completions", response_model=CompletionResponse)
async def completions(payload: Payload):
    choices = codegen(payload.prompt, payload.temperature, payload.max_tokens, payload.one_line)
    return CompletionResponse(choices=choices)


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=PORT)
