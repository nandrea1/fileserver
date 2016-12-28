import json
import logging
import os

from tornado import web, ioloop

import event_stores
from request_handlers import ClientHandler, ListFilesHandler, EventStoreHandler, SFTPWebSocket, AdminHandler
from util import DirectoryMonitor
import settings

logger = logging.getLogger(__name__.split('.')[0])
logger.setLevel(settings.LOG_LEVEL)

ch = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)

logger.addHandler(ch)


class SFTPServer(web.Application):

    FILE_ADD_EVENT = 'file_add_event'
    FILE_DELETE_EVENT = 'file_delete_event'

    def __init__(self, event_stores, sftp_directory=None, monitor_frequency=None, listen_on=None, **options):

        handlers = [
            (r'/', AdminHandler),
            (r'/api/clients', ClientHandler),
            (r'/api/list_files', ListFilesHandler),
            (r'/api/events', EventStoreHandler),
            (r'/server-ui/app/(.*)', web.StaticFileHandler, {'path': settings.APP_FOLDER}),
            (r'/ws', SFTPWebSocket)
        ]

        self.sftp_directory = sftp_directory or settings.SFTP_DIRECTORY
        self.monitor_frequency = monitor_frequency or settings.MONITOR_FREQUENCY
        self.old_files = []
        self.listen_on = listen_on or settings.LISTEN_PORT
        self.clients = []
        self.event_stores = event_stores
        super(SFTPServer, self).__init__(handlers, **options)

    def new_file_handler(self, new_files):
        if new_files:
            for new_file in new_files:
                event = event_stores.FileSystemEvent(event_type=self.FILE_ADD_EVENT, event_value=new_file)
                for store in self.event_stores:
                    store.store(event)
                    logger.debug('New File: {}'.format(event.__dict__))
                for client in self.clients:
                    client.write_message(json.dumps(event.__dict__))

    def deleted_file_handler(self, deleted_files):
        if deleted_files:
            for deleted_file in deleted_files:
                event = event_stores.FileSystemEvent(event_type=self.FILE_DELETE_EVENT, event_value=deleted_file)
                for store in self.event_stores:
                    store.store(event)
                    logger.debug('Deleted File: {}'.format(event.__dict__))
                for client in self.clients:
                    client.write_message(json.dumps(event.__dict__))

    def _monitor_directory(self):

        dm = DirectoryMonitor(self.sftp_directory, self.new_file_handler, self.deleted_file_handler,
                              old_files=self.old_files)
        self.old_files = dm.monitor()

    def start(self):
        logger.info('Server Running on port {}...'.format(self.listen_on))
        self.listen(self.listen_on)
        monitor = ioloop.PeriodicCallback(callback=self._monitor_directory, callback_time=self.monitor_frequency)
        monitor.start()
        ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    
    try:
        event_store_objs = [getattr(event_stores, store_name)() for store_name in settings.EVENT_STORES]
        template_path = os.path.join(os.path.dirname(__file__), settings.APP_FOLDER)
        static_path = os.path.join(os.path.dirname(__file__), settings.APP_FOLDER)
        server_obj = SFTPServer(event_stores=event_store_objs, template_path=template_path, static_path=static_path,
                                static_url_prefix=settings.APP_FOLDER)
        server_obj.start()
    
    except KeyboardInterrupt:
        logger.info('Keyboard Interrupt Received, Shutting Down Server...')
