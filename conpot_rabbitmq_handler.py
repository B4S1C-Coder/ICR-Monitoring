import logging
import pika

class RabbitMQHandler(logging.Handler):
    def __init__(self,rabbitmq_host='rabbitmq',queue_name='conpot_logs'):
        super().__init__()
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue_name)

    def emit(self, record):
        log_entry = self.format(record)
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=log_entry)

    def close(self):
        self.connection.close()
        super().close()
