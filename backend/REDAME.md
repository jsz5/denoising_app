docker build . -t nvidia-test
docker run --gpus all -it -p 8000:8000 denoising_backend bash
