FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    python3-pip git

RUN pip3 install --upgrade pip

COPY requirements.txt ./

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 7000

ENV PORT 7000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "7000"]
