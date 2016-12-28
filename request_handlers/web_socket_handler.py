import logging

from tornado import websocket

logger = logging.getLogger(__name__)


class SFTPWebSocket(websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        if self not in self.application.clients:
            self.application.clients.append(self)
        logger.debug('Websocket Opened: {}'.format(self))

    def on_message(self, message):
        logger.debug('Message From {}: {}'.format(self, message))

    def on_close(self):
        if self in self.application.clients:
            self.application.clients.remove(self)
        logger.debug('{} Closed Socket'.format(self))