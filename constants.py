DEVICE = "cuda"
EOD = "<|endoftext|>"
FIM_MIDDLE = "<fim_middle>"
FIM_PAD = "<fim_pad>"
FIM_PREFIX = "<fim_prefix>"
FIM_SUFFIX = "<fim_suffix>"
INFILL = "<FILL_HERE>"
PORT = 5000

SPECIAL_TOKENS = {
    "additional_special_tokens": [
        EOD,
        FIM_PREFIX,
        FIM_MIDDLE,
        FIM_SUFFIX,
        FIM_PAD,
    ],
    "pad_token": EOD,
}
