from abc import ABC, abstractmethod

from completion import get_llama_completion, get_starcoder_completion
from model import is_llama_model
from abstractions import Payload


class CodeGeneration(ABC):
    @abstractmethod
    def generate(self, model_name_or_path, is_downloaded_model):
        pass


class LlamaCodeGeneration(CodeGeneration):
    def generate(self, payload):
        return get_llama_completion(payload)


class StarCoderCodeGeneration(CodeGeneration):
    def generate(self, payload):
        return get_starcoder_completion(payload)


def get_generator():
    if is_llama_model:
        return LlamaCodeGeneration()
    return StarCoderCodeGeneration()


def codegen(payload: Payload) -> str:
    generator = get_generator()
    return generator.generate(payload)
