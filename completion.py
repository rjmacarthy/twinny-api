import torch
import re
from pydantic import BaseModel

from model import get_model

from constants import (
    STARCODER_TOKENS,
    LLAMA_TOKENS,
    INFILL,
    DEVICE,
)


class Choice(BaseModel):
    text: str


model, tokenizer = get_model()


def get_inputs(prompt):
    return tokenizer(
        prompt, return_tensors="pt", padding=True, return_token_type_ids=False
    ).to(DEVICE)


def get_prefix_suffix(prompt):
    return (prompt.split(INFILL) + ["", ""])[:2]


def get_starcoder_completion(payload):
    prefix, suffix = get_prefix_suffix(payload.prompt)
    prompt = f"{STARCODER_TOKENS['PRE']}{prefix}{STARCODER_TOKENS['SUF']}{suffix}{STARCODER_TOKENS['MID']}"
    with torch.no_grad():
        outputs = model.generate(
            **get_inputs(prompt),
            do_sample=True,
            temperature=payload.temperature,
            max_new_tokens=payload.max_tokens,
            pad_token_id=tokenizer.pad_token_id,
        )
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)
    start = decoded.find(STARCODER_TOKENS["MID"]) + len(STARCODER_TOKENS["MID"])
    end = decoded.find(STARCODER_TOKENS["EOD"], start) or len(decoded)
    completion = decoded[start:end]
    return completion.rstrip()


def get_llama_completion(payload):
    prefix, suffix = get_prefix_suffix(payload.prompt)
    prompt = f"{LLAMA_TOKENS['PRE']} {prefix} {LLAMA_TOKENS['SUF']}{suffix} {LLAMA_TOKENS['MID']}"
    with torch.no_grad():
        outputs = model.generate(
            **get_inputs(prompt),
            top_k=3,
            top_p=0.95,
            num_return_sequences=1,
            do_sample=True,
            temperature=payload.temperature,
            max_new_tokens=payload.max_tokens,
            pad_token_id=tokenizer.eos_token_id,
        )
    choices = []
    for output in outputs:
        text = tokenizer.decode(output, skip_special_tokens=False)
        match = re.search(r"<MID>(.*)", text)
        if match:
            completion = match.group(1)
            completion = completion.replace("<EOT></s>", "")
            choices.append(Choice(text=completion.rstrip()))
        else:
            choices.append(Choice(text=""))
    return choices
