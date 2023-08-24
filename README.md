### twinny-api

**A locally hosted AI code completion server similar to GitHub Copilot, but with 100% privacy.**

Utilizing StarCoder models, you can create your private code completion environment.

This API supports most transformer models based which use the [special token list](https://huggingface.co/bigcode/starcoderbase/blob/main/special_tokens_map.json) from the [bigcode/starcoderbase](https://huggingface.co/bigcode/starcoderbase) model.

#### 📥 Usage

Run `./setup.sh` to set your environment variables to `.env`

Run `start.sh` to start the container.

The script will copy a cached model to the models folder for Docker to use.

`Docker``, `nvidia-docker`` and `docker-compose`` are required.

Models will be loaded from `./models` directory or the location set for `HF_CACHE_DIRECTORY` in .env, this is currently pointed at the default huggingface cache directory `/home/user/.cache/huggingface`.

You can run everythiung manually if you want...

```bash
pip install -r requirements.txt
python api.py
```

You can also download models manually by running this command.  If this is not done before starting the api will attempt download the model from huggingface or use your hugginface cache.

```bash
python download.py bigcode/starcoderbase-1b
```

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
