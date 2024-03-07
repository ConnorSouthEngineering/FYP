#!/bin/bash

cat ~/api.key | docker login nvcr.io --username '$oauthtoken' --password-stdin
docker build -t "triton:latest" . > docker_build.log 2>&1
#docker run --rm --runtime=nvidia --gpus all -p8000:8000 -p8001:8001 -p8002:8002 -v/home/nvidia/server/docs/examples/model_repository:/models "trition:latest" --model-repository=/models
``