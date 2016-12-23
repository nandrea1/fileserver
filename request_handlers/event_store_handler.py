import json
from tornado import web

class EventStoreHandler(web.RequestHandler):

    def get(self, *args):
        store = self.get_argument('store', 'LocalEventStore')
        query = self.get_argument('query', None)
        store_obj = [x for x in self.application.event_stores if x.__class__.__name__ == store]
        events = []
        if store_obj:
            events = [x.__dict__ for x in store_obj[0].get(query)]
        self.write(json.dumps(events))