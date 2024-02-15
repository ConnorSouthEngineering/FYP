#!/bin/bash

cat ~/api.key | docker login nvcr.io --username '$oauthtoken' --password-stdin
docker build -t "cudatf:Dockerfile" .
docker run --gpus all -it --name $1 cudatf:Dockerfile
```