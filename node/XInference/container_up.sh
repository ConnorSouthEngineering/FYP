#!/bin/bash

cat ~/api.key | docker login nvcr.io --username '$oauthtoken' --password-stdin
docker build -t "trition:latest" .
```