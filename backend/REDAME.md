docker build . -t denoising_backend
docker run --gpus all --restart on-failure -v $(pwd)/:/code:cached -p 8000:8000 denoising_backend 

