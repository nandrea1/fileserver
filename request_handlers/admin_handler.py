from tornado import web


class AdminHandler(web.RequestHandler):

    def get(self, *args):
        return self.render('index.html')
