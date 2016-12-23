from sftpserver.event_stores.base_event_store import BaseEventStore

LOCAL_EVENT_STORE = []


class LocalEventStore(BaseEventStore):

    global LOCAL_EVENT_STORE

    def get(self, query):
        if not query:
            return LOCAL_EVENT_STORE
        result_set = []
        for event in LOCAL_EVENT_STORE:
            if event.check_event(query):
                result_set.append(event)
        return result_set

    def store(self, event):
        LOCAL_EVENT_STORE.append(event)