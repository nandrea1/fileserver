from abc import ABCMeta, abstractmethod
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class BaseEventStore(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def store(self, *args, **kwargs):
        pass

class DBEventStore(BaseEventStore):

    __metaclass__ = ABCMeta

    connection = None
    columns = None
    db_name = None
    table_name = None

    @abstractmethod
    def _create_table(self, *args, **kwargs):
        pass

    @abstractmethod
    def _connect(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, query, limit, offset):
        pass

    @abstractmethod
    def get_total_records(self):
        pass

    @abstractmethod
    def store(self, *args, **kwargs):
        pass

    @classmethod
    def _execute_sql(cls, sql, return_results=False, columns=None, connection=None):
        connection = connection or cls.connection
        c = connection.cursor()
        logger.debug(sql)
        print sql
        c.execute(sql)
        connection.commit()
        results = None
        columns = columns or cls.columns
        if return_results:
            results = [{columns[i]: row[i] for i in xrange(len(row))} for row in c.fetchall()]
        c.close()
        return results


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
