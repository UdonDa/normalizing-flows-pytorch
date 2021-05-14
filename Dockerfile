FROM pytorch/pytorch:1.7.1-cuda11.0-cudnn8-devel

ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
        build-essential \
        nasm \
        cmake \
        curl \
        git \
        unzip \
        imagemagick \
        bzip2 \
        graphviz \
        vim \
        sudo \
        tree \
        ca-certificates \
        libjpeg-dev \
        libopencv-dev \
        libgl1-mesa-dev \
        libpng-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src

ENV HOME /src
ENV SHELL /bin/bash

ADD requirements.txt /src
RUN pip install -r requirements.txt
RUN pip install git+https://github.com/S-aiueo32/lpips-pytorch.git