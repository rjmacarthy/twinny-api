rm .env
echo "Creating config file"
cp config.example.yml config.yml
echo "Setting model directories"
HF_CACHE_DIRECTORY="HF_CACHE_DIRECTORY=$HOME/.cache/huggingface"
MODEL_DIRECTORY="MODEL_DIRECTORY=./models"
echo $HF_CACHE_DIRECTORY >> .env
echo $MODEL_DIRECTORY >> .env
echo "Setup complete, check .env to make sure all went well."