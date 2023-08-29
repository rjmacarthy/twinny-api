import torch
import re
from model import get_model
from abstractions import Choice

from constants import (
    STARCODER_TOKENS,
    LLAMA_TOKENS,
    INFILL,
    DEVICE,
)


model, tokenizer = get_model()


def get_inputs(prompt):
    return tokenizer(
        prompt, return_tensors="pt", padding=True, return_token_type_ids=False
    ).to(DEVICE)


def get_prefix_suffix(prompt):
    return (prompt.split(INFILL) + ["", ""])[:2]


def get_outputs(payload, prompt):
    with torch.no_grad():
        outputs = model.generate(
            **get_inputs(prompt),
            top_k=payload.top_k,
            top_p=payload.top_p,
            num_return_sequences=payload.num_return_sequences,
            do_sample=True,
            temperature=payload.temperature,
            max_new_tokens=payload.max_tokens,
            pad_token_id=tokenizer.eos_token_id,
        )
    return outputs


def get_starcoder_completion(payload):
    prefix, suffix = get_prefix_suffix(payload.prompt)
    prompt = f"{STARCODER_TOKENS['PRE']}{prefix}{STARCODER_TOKENS['SUF']}{suffix}{STARCODER_TOKENS['MID']}"
    outputs = get_outputs(payload, prompt)
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=False)
    start = decoded.find(STARCODER_TOKENS["MID"]) + len(STARCODER_TOKENS["MID"])
    end = decoded.find(STARCODER_TOKENS["EOD"], start) or len(decoded)
    completion = decoded[start:end]
    try:
        if not completion:
            text = ""
        if payload.one_line:
            text = completion.splitlines()[0] or completion.splitlines()[1]
    except:
        text = ""
    return [Choice(text=text)]


def get_llama_completion(payload):
    prefix, suffix = get_prefix_suffix(payload.prompt)
    prompt = f"{LLAMA_TOKENS['PRE']} {prefix} {LLAMA_TOKENS['SUF']}{suffix} {LLAMA_TOKENS['MID']}"
    outputs = get_outputs(payload, prompt)
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
