import logging
import os

LOG_LEVEL = logging.DEBUG
VALID_SEARCH_PATH = r'^~/Development/test'

SQLLITE_DB = 'events'

APP_FOLDER = 'server-ui/app/'

ADMIN_EVENT_STORE = 'SQLLiteEventStore'

SFTP_DIRECTORY = os.getenv('SFTP_DIRECTORY', '~/Development/test')
MONITOR_FREQUENCY = os.getenv('MONITOR_FREQUENCY', 1000)
LISTEN_PORT = os.getenv('LISTEN_PORT', 8000)

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_QUEUE_NAME = os.getenv('RABBITMQ_QUEUE', 'sftp_events')

EVENT_STORES = [
    'LocalEventStore',
    'RabbitMQEventStore',
    'SQLLiteEventStore'
]
