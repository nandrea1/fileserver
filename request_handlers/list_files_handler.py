import logging
import os
import re

from tornado import web

from sftpserver.settings import VALID_SEARCH_PATH

logger = logging.getLogger(__name__)


class ListFilesHandler(web.RequestHandler):

    def get(self, *args):
        directory = self.get_argument('directory', self.application.sftp_directory)
        sub_dir_ind = self.get_argument('list_sub_directories', 'True')
        if not re.search(VALID_SEARCH_PATH, directory):
            logger.error('Invalid Search Path Provided!')
            self.set_status(401, 'Invalid Search Path Provided')
            self.write('')
        else:
            list_sub_directories = sub_dir_ind.lower()[0] in ['t', 'y', '1']
            if list_sub_directories:
                file_list = [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(directory)) for f in fn]
            else:
                file_list = os.listdir(directory)
            self.write(', '.join(file_list))