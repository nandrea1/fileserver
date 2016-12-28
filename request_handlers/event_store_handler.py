import json
from tornado import web

import settings
from event_stores import DBEventStore

class EventStoreHandler(web.RequestHandler):

    def get(self, *args):
        store = self.get_argument('store', settings.ADMIN_EVENT_STORE)
        query = self.get_argument('query', None)
        limit = self.get_argument('length', 10)
        offset = self.get_argument('start', 0)
        order_by = self.get_argument('order_by', None) or int(self.get_argument('order[0][column]', 0))
        order_by_type = self.get_argument('order_by_type', None) or self.get_argument('order[0][dir]', 'asc')
        store_obj = [x for x in self.application.event_stores if x.__class__.__name__ == store]
        events = []
        if store_obj:
            data_store = store_obj[0]
            if isinstance(order_by, int):
                order_by = data_store.columns[order_by]
            order_by = order_by + ' ' + order_by_type
            events = {'data': [x for x in data_store.get(query, limit, offset, order_by)]}
            if issubclass(data_store.__class__, DBEventStore):
                record_count = data_store.get_total_records()['recordsTotal']
                events.update({'recordsTotal': record_count, 'recordsFiltered': record_count})
        self.write(json.dumps(events))