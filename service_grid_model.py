import pika
import joblib
import json
import os
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

channel.queue_declare(queue="grid_logs")

model = joblib.load('gridModel2.pkl')

def process_entry(ch, method, properties, body):
    body = body.decode('utf-8')
    body = json.loads(body)
    print(body["data"])
#    arr = scaler.transform(body["data"][:-2])

    y_pred = model.predict([body["data"][:-2]])

    print(y_pred)

def run_service():
    channel.basic_consume(queue="grid_logs", on_message_callback=process_entry, auto_ack=True)
    print("Grid Model Service ready.")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        run_service()
    except KeyboardInterrupt:
        print("Stopping ...")
        try:
            sys.exit(0)
        except:
            os._exit(0)
