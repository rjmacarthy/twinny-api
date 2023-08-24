#!/bin/bash
source .env

echo """
   __           _                  
  / /__      __(_)___  ____  __  __
 / __/ | /| / / / __ \/ __ \/ / / /
/ /_ | |/ |/ / / / / / / / / /_/ / 
\__/ |__/|__/_/_/ /_/_/ /_/\__, /  
                          /____/
"""  

echo "Huggingface model directory: $HF_CACHE_DIRECTORY"
echo "Model directory: ./models"
echo "Using config in './config.yml"
echo ""
cat config.yml
echo ""
docker-compose up