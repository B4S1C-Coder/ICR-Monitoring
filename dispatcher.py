import pandas as pd
import time
import pika
import json

data = pd.read_csv("smart_grid_stability_augmented.csv")

#print(data.head())

class GridDataDispatcher:
    def __init__(self):
        self.message_delay = 1
        self.counter = 0
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )

        self.channel = connection.channel()
        self.channel.queue_declare(queue="grid_logs")

    def test(self):
        #print(f"counter = {self.counter}")
        while True:
            print(data.loc[self.counter].values.tolist())

            payload = json.dumps({
                "data": data.loc[self.counter].values.tolist()
            })

            self.channel.basic_publish(exchange='',routing_key="grid_logs", body=payload.encode('utf-8'))
            print("Pushed to queue")
            time.sleep(self.message_delay)
            self.counter += 1

gdd = GridDataDispatcher()
gdd.test()
