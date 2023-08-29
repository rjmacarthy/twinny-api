DEVICE = "cuda"

PORT = 7000

INFILL = "<FILL_HERE>"

LLAMA_TOKENS = {
    "EOD": "<EOD>",
    "MID": "<MID>",
    "PRE": "<PRE>",
    "SUF": "<SUF>",
    "PAD": "<PAD>",
}


LLAMA_SPECIAL_TOKENS = {
    "pad_token": LLAMA_TOKENS["PAD"],
}

STARCODER_TOKENS = {
    "EOD": "<|endoftext|>",
    "MID": "<fim_middle>",
    "PAD": "<fim_pad>",
    "PRE": "<fim_prefix>",
    "SUF": "<fim_suffix>",
}

STARCODER_SPECIAL_TOKENS = {
    "additional_special_tokens": [
        STARCODER_TOKENS["EOD"],
        STARCODER_TOKENS["PRE"],
        STARCODER_TOKENS["MID"],
        STARCODER_TOKENS["SUF"],
        STARCODER_TOKENS["PAD"],
    ],
    "pad_token": STARCODER_TOKENS["EOD"],
}
