# @title Dockerfile
# @author: Takahashi Akari <akaritakahashioss@gmail.com>
# @date: 2022/07/23
# @version: 1.0.4
# @description: This application is a chatbot that uses Kafka as a message broker.
# @license: MIT License Copyright (c) 2020 Takahashi Akari <akaritakahashioss@gmail.com>
FROM python:3.8.13
WORKDIR /app
COPY ./ ./
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip --default-timeout=1000 install -r requirements.txt
CMD python -u app.py
