### twinny-api

**A locally hosted AI code completion server similar to GitHub Copilot, but with 100% privacy.**

Utilizing [bigcode/starcoderbase-3b](https://huggingface.co/bigcode/starcoderbase-3b) by default, you can create your private code completion environment.

#### 📥 Downloading the Model

Execute the following command to download the [bigcode/starcoderbase-3b](https://huggingface.co/bigcode/starcoderbase-3b) model:

```bash
python download.py bigcode/starcoderbase-3b
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

Nvidia 3090 can run [bigcode/starcoderbase-3b](https://huggingface.co/bigcode/starcoderbase-3b) in 8Bit.

All models using StarCode tokenizer below 3B are supported in full.
