import pandas as pd
import time
import pika
import json
import socket
import threading

class DataDispatcher:
    def __init__(self, type_, queue_name, data_source, port, num_samples, interval):
        self.__type    = type_       # Type of dispatcher eg. PLC, RTU, etc.
        self.__data    = None        # Data to be pushed
        self.__channel = None        # RabbitMQ Connection Channel
        self.__queue   = queue_name  # Queue to push data to
        self.__active  = True        # Controls if data will be pushed or not
        self.__client  = None        # Socket Client for listening for commands
        self.__samples = num_samples # Number of Samples to dispatch in all
        self.__interval= interval    # Number of seconds to sleep after each dispatch

        try:
            self.__data = pd.read_csv(data_source)
            print(f"[ INFO ] Data Source loaded: {data_source}")
        except Exception as err:
            print(f"[ WARN ] Data Source is empty: {err}")

        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
            self.__channel = connection.channel()
            self.__channel.queue_declare(queue=self.__queue)
            print(f"[ INFO ] Connected to RabbitMQ")
        except Exception as err:
            print(f"[ FAIL ] Unable to connect to RabbitMQ: {err}")

        try:
            self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__client.connect(('127.0.0.1', port))
            print(f"[ INFO ] Connected to Command Server")
        except Exception as err:
            print(f"[ FAIL ] Unable to connect to Command Server: {err}")

        print(f"Dispatcher (type: {self.__type}, queue: {self.__queue}) active ...")

    def __dispatching_loop(self):
        print(f"[ INFO ] Dispatching loop started ...")

        counter = 0
        while ((counter < self.__samples) and (self.__active)):

            payload = json.dumps({
                "data": self.__data.loc[counter].values.tolist()
            })

            self.__channel.basic_publish(
                exchange='',
                routing_key=self.__queue,
                body=payload.encode('utf-8')
            )

            print("[ INFO ] Pushed to queue.")

            time.sleep(self.__interval)

            counter += 1

            if (counter >= self.__samples):
                counter = 0
            
    def __command_processor_loop(self):
        try:
            while True:
                command = self.__client.recv(1024).decode('utf-8')

                if not command:
                    print("[ WARN ] Connection from Command Server lost.")
                    break

                self.__active = not self.__active
                print(f"[ WARN ] Node status self.__active = {self.__active}")

        except KeyboardInterrupt:
            print("[ WARN ] Shutting down due to manual intervention ...")

        finally:
            self.__client.close()

    def start(self):
        if self.__channel:
            dispatch_thread = threading.Thread(target=self.__dispatching_loop)
            dispatch_thread.start()
            print("[ INFO ] Dispatch thread started ...")

        if self.__client:
            command_thread = threading.Thread(target=self.__command_processor_loop)
            command_thread.start()
            print("[ INFO ] Command thread started ...")

