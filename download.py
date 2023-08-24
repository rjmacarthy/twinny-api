import requests
import os
import yaml
from tqdm import tqdm

config = yaml.safe_load(open("./config.yml"))


def download_file(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    response = requests.get(url, stream=True)
    total_size_in_bytes = int(response.headers.get("content-length", 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size_in_bytes, unit="iB", unit_scale=True)

    with open(path, "wb") as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)

    progress_bar.close()


def download_model(model_name):
    destination_folder = "models"

    destination = f"{destination_folder}/{model_name}"

    if os.path.exists(destination):
        print(f"Model already exists {destination}")
        return

    base_url = f"https://huggingface.co/{model_name}/resolve/main"
    headers = {"User-Agent": "Hugging Face Python"}

    response = requests.get(
        f"https://huggingface.co/api/models/{model_name}", headers=headers
    )
    response.raise_for_status()

    files_to_download = [file["rfilename"] for file in response.json()["siblings"]]

    os.makedirs(destination, exist_ok=True)

    for file in files_to_download:
        print(f"Downloading {file}...")
        download_file(f"{base_url}/{file}", f"{destination_folder}/{model_name}/{file}")


if __name__ == "__main__":
    download_model(config["model_name"])
