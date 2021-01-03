#!/bin/bash
docker stop denoising_backend 
docker rm denoising_backend
cd frontend/app
docker-compose down


