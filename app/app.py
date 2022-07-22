from email import message
from flask import Flask, render_template
from flask_cors import CORS, cross_origin
from flask_socketio import SocketIO, emit
from kafka import KafkaProducer, KafkaConsumer, TopicPartition
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
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    producer.send(TOPIC_NAME, json.dumps(message).encode("utf-8"))
    producer.flush()
    print("Message sent to Kafka")
    consumer = KafkaConsumer(
        TOPIC_NAME, bootstrap_servers=BOOTSTRAP_SERVERS, auto_offset_reset="earliest", group_id="test-consumer-group", auto_commit_enable=False, auto_commit_interval_ms=1000, value_deserializer=lambda m: json.loads(m.decode("utf-8"))
    )
    print("Consumer created")

    # message count
    message_count = 0
    for message in consumer:
        message_count += 1

    i = 0
    # end message
    for message in consumer:
        i += 1
        if i == message_count:
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

