import yaml
import os
from transformers import AutoModelForCausalLM, AutoTokenizer


from constants import (
    SPECIAL_TOKENS,
    DEVICE,
)

config = yaml.safe_load(open("./config.yml"))


def get_model():
    load_in_4_bit = config["load_in_4bit"]
    load_in_8bit = config["load_in_8bit"]
    model_name = config["model_name"]
    tokenizer_name = config["tokenizer_name"]
    local_model_dir = f"./models/{model_name}"
    is_downloaded_model = os.path.exists(local_model_dir)
    model_name_or_path = local_model_dir if is_downloaded_model else model_name

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    tokenizer.add_special_tokens(SPECIAL_TOKENS)

    if load_in_4_bit or load_in_8bit:
        model = AutoModelForCausalLM.from_pretrained(
            model_name_or_path,
            load_in_4bit=load_in_4_bit,
            load_in_8bit=load_in_8bit,
            device_map="auto",
            local_files_only=is_downloaded_model,
        )

        return model, tokenizer

    model = AutoModelForCausalLM.from_pretrained(
        model_name_or_path, local_files_only=is_downloaded_model
    ).to(DEVICE)

    return model, tokenizer
