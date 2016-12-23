import os

class DirectoryMonitor(object):

    def __init__(self, directory_to_monitor, new_file_handler, deleted_file_handler, monitor_sub_directories=True,
                 ignore_regex=None, old_files=[]):
        self.directory = directory_to_monitor
        self.old_files = old_files
        self.handle_new_files = new_file_handler
        self.handle_deleted_files = deleted_file_handler
        self.monitor_sub_directories = monitor_sub_directories
        self.ignore_regex = ignore_regex

    def monitor(self):
        current_files = DirectoryMonitor.list_files(self.directory, self.monitor_sub_directories)
        if self.old_files:
            new_files = set(current_files).difference(set(self.old_files))
            self.handle_new_files(new_files)
            deleted_files = set(self.old_files).difference(set(current_files))
            self.handle_deleted_files(deleted_files)
        self.old_files = current_files
        return current_files

    @staticmethod
    def list_files(directory, list_sub_directories=True):
        if list_sub_directories:
            return [os.path.join(dp, f) for dp, dn, fn in os.walk(os.path.expanduser(directory)) for f in fn]
        else:
            return os.listdir(directory)