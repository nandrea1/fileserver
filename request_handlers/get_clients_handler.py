from tornado import web


class ClientHandler(web.RequestHandler):

    def get(self, *args):
        clients = self.application.clients
        self.write(', '.join(clients))