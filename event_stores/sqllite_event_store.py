import sqlite3

from base_event_store import DBEventStore
import settings


def create_table(table_name, connection):
    sql = """
            CREATE TABLE IF NOT EXISTS {table_name}
            (created_at datetime, event_type varchar, event_value varchar);
            """.format(table_name=table_name)
    DBEventStore._execute_sql(sql, connection=connection)


class SQLLiteEventStore(DBEventStore):

    db_name = settings.SQLLITE_DB
    connection = sqlite3.connect(db_name)
    table_name = 'events'
    create_table(table_name, connection)
    columns = ['created_at', 'event_type', 'event_value']

    @classmethod
    def _create_table(cls):
        create_table(cls.table_name, cls.connection)

    @staticmethod
    def _connect(db_name):
        return sqlite3.connect(db_name)

    def get(self, query, limit=10, offset=0, order_by=None):

        limit_str = 'LIMIT {}'.format(limit) if limit else ''
        offset_str = 'OFFSET {}'.format(offset) if offset else ''
        order_str = 'ORDER BY {}'.format(order_by) if order_by else ''
        sql = query or 'SELECT {} FROM {table_name} {order_str} {limit_str} {offset_str}'.format(', '.join(self.columns),
                                                                                                 limit_str=limit_str,
                                                                                                 offset_str=offset_str,
                                                                                                 table_name=self.table_name,
                                                                                                 order_str=order_str)
        return self._execute_sql(sql, return_results=True)

    def get_total_records(self):
        sql = 'SELECT COUNT(*) FROM {}'.format(self.table_name)
        return self._execute_sql(sql, return_results=True, columns=['recordsTotal'])[0]

    def store(self, event):
        value_tuple = (event.created_at, event.event_type, event.event_value)
        sql = """
        INSERT INTO events ({}) VALUES {}
        """.format(', '.join(self.columns), value_tuple)
        self._execute_sql(sql)