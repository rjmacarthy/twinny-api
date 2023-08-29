from pydantic import BaseModel
from typing import List


class CompletionResponse(BaseModel):
    choices: List


class Choice(BaseModel):
    text: str


class Payload(BaseModel):
    max_tokens: int = 100
    num_return_sequences: int
    one_line: bool = True
    prompt: str
    temperature: float = 0.1
    top_k: int
    top_p: float
