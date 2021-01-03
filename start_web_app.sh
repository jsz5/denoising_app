#!/bin/bash
cd backend
docker run -d --name denoising_backend --gpus all --restart on-failure -v $(pwd)/:/code:cached -p 8000:8000 denoising_backend 
cd ../frontend/app
docker-compose up -d


