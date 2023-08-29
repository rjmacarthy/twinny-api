import yaml
import re
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
from auto_gptq import AutoGPTQForCausalLM
from abc import ABC, abstractmethod

from constants import (
    LLAMA_SPECIAL_TOKENS as LST,
    STARCODER_SPECIAL_TOKENS as SCSP,
    DEVICE,
)

config = yaml.safe_load(open("./config.yml"))
model_name = config["model_name"]
is_llama_model = re.search(r"(?i)llama", model_name)
is_gptq_model = re.search(r"(?i)gptq", model_name)


class ModelLoader(ABC):
    @abstractmethod
    def load(self, model_name_or_path, is_downloaded_model):
        pass


class GPTQLoader(ModelLoader):
    def load(self, model_name_or_path, _):
        return AutoGPTQForCausalLM.from_quantized(
            model_name_or_path, use_safetensors=True
        ).to(DEVICE)


class BitLoader(ModelLoader):
    def __init__(self, load_in_4bit, load_in_8bit):
        self.load_in_4_bit = load_in_4bit
        self.load_in_8_bit = load_in_8bit

    def load(self, model_name_or_path, is_downloaded_model):
        return AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            load_in_4bit=self.load_in_4_bit,
            load_in_8bit=self.load_in_8_bit,
            device_map="auto",
            local_files_only=is_downloaded_model,
        )


class DefaultLoader(ModelLoader):
    def load(self, model_name_or_path, is_downloaded_model):
        return AutoModelForCausalLM.from_pretrained(
            model_name_or_path, local_files_only=is_downloaded_model
        ).to(DEVICE)


def get_model_loader(is_gptq_model, load_in_4_bit, load_in_8bit):
    if is_gptq_model:
        return GPTQLoader()
    if load_in_4_bit or load_in_8bit:
        return BitLoader(load_in_4_bit, load_in_8bit)
    return DefaultLoader()


def get_model():
    load_in_4bit = config["load_in_4bit"]
    load_in_8bit = config["load_in_8bit"]
    tokenizer_name = config["tokenizer_name"]
    is_llama_model = re.search(r"(?i)llama", model_name)
    is_gptq_model = re.search(r"(?i)gptq", model_name)
    local_model_dir = f"./models/{model_name}"
    is_downloaded_model = os.path.exists(local_model_dir)
    model_name_or_path = local_model_dir if is_downloaded_model else model_name
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)
    tokenizer.add_special_tokens(LST if is_llama_model else SCSP)
    loader = get_model_loader(is_gptq_model, load_in_4bit, load_in_8bit)
    model = loader.load(model_name_or_path, is_downloaded_model)
    return model, tokenizer
