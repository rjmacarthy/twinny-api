## twinny-api

**A locally hosted AI code completion server similar to GitHub Copilot, but with 100% privacy.**

**🚀 twinny-api now officially supports [codellama](https://huggingface.co/codellama) 🚀**

This API supports both [codellama](https://huggingface.co/codellama) models and [Starcoder](https://huggingface.co/bigcode/starcoderbase) models.

Support are Startcoder models using [special token list](https://huggingface.co/bigcode/starcoderbase/blob/main/special_tokens_map.json) from the [bigcode/starcoderbase](https://huggingface.co/bigcode/starcoderbase) model.

All [codellama](https://huggingface.co/codellama) models should now work out of the box.

#### 📥 Usage

With `Docker`, `nvidia-docker` and `docker-compose` installed.

Run `./setup.sh` to set your environment variables to `.env` this is your model directories.

Check and set your options in `config.yml` there are defaults for them but you may need to tweak them.

Run `./start.sh` to start the container.

You can run everything manually if you want...

```bash
pip install -r requirements.txt
python api.py
```

You can also download models manually by running this command.  If this is not done before starting the api will attempt download the model from huggingface or use your hugginface cache.

```bash
python download.py bigcode/starcoderbase-1b
```

#### twinny VSCode Extension

Complement your setup with the twinny VSCode extension, available for download [here](https://github.com/rjmacarthy/twinny).

Enjoy personalized and private code completion. 🎉


#### System requirements

For a general idea a single nvidia 3090 can run [bigcode/starcoderbase-3b](https://huggingface.co/bigcode/starcoderbase-3b) in 8Bit comfortably.

An nvidia 3090 can run [CodeLlama-7b-hf](https://huggingface.co/codellama/CodeLlama-7b-hf) in full, 8Bit or 4Bit.

All models using StarCode tokenizer below 3B are probably working. The 1B models provide faster and more realistically useable inference speed depending on your hardware.
