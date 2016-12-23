from abc import ABCMeta, abstractmethod
from datetime import datetime


class BaseEventStore(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def store(self, *args, **kwargs):
        pass


class FileSystemEvent(object):

    def __init__(self, event_type, event_value):
        self.event_type = event_type
        self.event_value = event_value
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S %f')

    def __iter__(self):
        return self.__dict__

    def check_event(self, check_dict):
        check_val = True
        for key, value in check_dict.items():
            check_val == getattr(self, key) == value and check_val
        return check_val
