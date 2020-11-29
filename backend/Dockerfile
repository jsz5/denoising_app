FROM nvidia/cuda:10.1-base
CMD nvidia-smi



RUN apt-get update && apt-get install --no-install-recommends --no-install-suggests -y curl libjpeg-dev libsm6 libxext6 libxrender-dev
RUN apt-get -y install python3
RUN apt-get -y install python3-pip

COPY ./requirements.txt  /tmp/requirements.txt
RUN pip3 --no-cache-di install -r  /tmp/requirements.txt \
    && apt-get clean

RUN mkdir /code
WORKDIR /code
COPY . /code/


ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /code:$PYTHONPATH
ENV DJANGO_SETTINGS_MODULE app.settings

EXPOSE 8000
CMD ["python3", "manage.py", "migrate"]
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

