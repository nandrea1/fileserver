import json
import logging

import pika

from base_event_store import BaseEventStore 
import settings

logger = logging.getLogger(__name__)


class RabbitMQEventStore(BaseEventStore):

    def store(self, event):
        connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST))
        channel = connection.channel()
        channel.basic_publish(exchange='',
                              routing_key=settings.RABBITMQ_QUEUE_NAME,
                              body=json.dumps(event.__dict__)
                              )
        connection.close()

    def get(self, query):
        logger.error('RabbitMQEventStore does not support query')