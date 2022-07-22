'''
@title app.py
@author: Takahashi Akari <akaritakahashioss@gmail.com>
@date: 2022/07/23
@version: 1.0.1
@description: This application is a chatbot that uses Kafka as a message broker.
@license: MIT License Copyright (c) 2020 Takahashi Akari <akaritakahashioss@gmail.com>
'''

from email import message
from sys import api_version
from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from kafka import KafkaProducer, KafkaConsumer
import os
import json

## Config API
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
cors = CORS(app)
app.config["CORS_HEADERS"] = "Content-Type"
# Config model

BOOTSTRAP_SERVERS = os.environ.get("KAFKA_BROKER_URL")  #'kafka:9092'
TOPIC_NAME = os.environ.get("TRANSACTIONS_TOPIC")

# Local config :
BOOTSTRAP_SERVERS = "kafka:9092"
TOPIC_NAME = "test"


@app.route("/")
@cross_origin()
def home():
    return render_template("index.html")


""" Kafka endpoints """


@socketio.on("connect", namespace="/kafka")
def test_connect():
    print('Connected via Websocket')

@socketio.on("kafka_message", namespace="/kafka")
def kafka_message(message):
    # kafka producer sends messages
    print(message)
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, api_version=(0, 11, 5))
    producer.send(TOPIC_NAME, json.dumps(message).encode("utf-8"))
    producer.flush()
    print("Message sent to Kafka")
    consumer = KafkaConsumer(
        TOPIC_NAME, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset="earliest", group_id="test-consumer-group", enable_auto_commit=False
    )
    print("Consumer created")

    for message in consumer:
        parsed = json.loads(message.value.decode("utf-8"))
        print(parsed)
        msg = parsed["message"]
        print(msg)
        chatbot_message = chatbot(msg)
        print(chatbot_message)
        response = {"message": chatbot_message}
        emit("kafka_message", response, broadcast=True)
        print("Message sent to client")
        consumer.commit()
        print("Committed")
        break


        
if __name__ == "__main__":
    from model import chatbot  
    socketio.run(app, host="0.0.0.0", port=80, debug=False, certfile='cert.pem', keyfile='key.pem')

