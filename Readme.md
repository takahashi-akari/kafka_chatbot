# Chatbot with Kafka: 
This application is a chatbot that uses Kafka as a message broker.

# Usage:
```bash
docker-compose build
docker-compose up -d
```

# Demo
URL: [https://kafkabot.akari.mn](https://kafkabot.akari.mn)

# Docker-compose:
```yaml
# @license: MIT License Copyright (c) 2022 Takahashi Akari <akaritakahashioss@gmail.com>
version: '3'

services:
  kafka:
    environment:
      HOSTNAME_COMMAND: "route -n | awk '/UG[ \t]/{print $$2}'"
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092
      KAFKA_LISTENERS: PLAINTEXT://0.0.0.0:9092
    image: wurstmeister/kafka
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - "9092:9092"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - zookeeper
    restart: always

  zookeeper:
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    image: wurstmeister/zookeeper
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
    ports:
      - "2181:2181"
      - "2888:2888"
      - "3888:3888"
    restart: always

  app:
    build: ./app
    ulimits:
      nofile:
        soft: 65536
        hard: 65536
    ports:
     - "3306:80"
    depends_on:
     - kafka
    restart: always
    environment: 
      TRANSACTIONS_TOPIC: test
      KAFKA_BROKER_URL: kafka:9092

```
# Links
- [Kafka](https://kafka.apache.org/)
- [Zookeeper](https://zookeeper.apache.org/)
- [Docker](https://www.docker.com/)
- [Docker-compose](https://docs.docker.com/compose/install/)
- [Takahashi Akari - github.io](https://github.com/takahashi-akari)

# License:
MIT License Copyright (c) 2022 [Takahashi Akari](https://github.com/takahashi-akari)
