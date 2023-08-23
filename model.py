from transformers import AutoModelForCausalLM, AutoTokenizer


from constants import (
    EOD,
    FIM_MIDDLE,
    FIM_PREFIX,
    FIM_SUFFIX,
    FIM_PAD,
    tokenizer_name,
    model_name,
)

special_tokens = {
    "additional_special_tokens": [
        EOD,
        FIM_PREFIX,
        FIM_MIDDLE,
        FIM_SUFFIX,
        FIM_PAD,
    ],
    "pad_token": EOD,
}


def get_model():
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, padding_side="left")
    tokenizer.add_special_tokens(special_tokens)
    model = AutoModelForCausalLM.from_pretrained(model_name, load_in_8bit=True, device_map="auto")

    return model, tokenizer
