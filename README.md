### twinny-api

**A locally hosted AI code completion server similar to GitHub Copilot, but with 100% privacy.**

Utilizing StarCoder models, you can create your private code completion environment.

This API supports most transformer models based which use the [special token list](https://huggingface.co/bigcode/starcoderbase/blob/main/special_tokens_map.json) from the [bigcode/starcoderbase](https://huggingface.co/bigcode/starcoderbase) model.

#### 📥 Downloading the Model

Execute the following command to download a model.  For example we can use the [bigcode/starcoderbase-1b](https://huggingface.co/bigcode/starcoderbase-3b) model.  Alternatively you can simply run the `api.py` file and `transformers` will download the model for you before starting.

Optional: If you want to download the model from the command line, you can run the following command:

```bash
python download.py bigcode/starcoderbase-1b
``````

🚀 Running the API
Once the model has finished downloading, you can start the API using:

```
python api.py
```

#### twinny VSCode Extension

Complement your setup with the twinny VSCode extension, available for download [here](https://github.com/rjmacarthy/twinny).

Enjoy personalized and private code completion. 🎉


#### Requirements

An nvidia 3090 can run [bigcode/starcoderbase-3b](https://huggingface.co/bigcode/starcoderbase-3b) in 8Bit.

All models using StarCode tokenizer below 3B are supported and tested on a 3090. The 1B models provide faster and more realistically useable inference speed.
