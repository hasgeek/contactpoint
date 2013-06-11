from tornado import web, websocket
import simplejson as json

class WebHandler(web.RequestHandler):
    def initialize(self, CP):
        self.CP = CP

class JSONHandler(WebHandler):
    def write(self, data):
        self.set_header('Content-Type', 'application/json')
        super(JSONHandler, self).write(data)

class SocketHandler(websocket.WebSocketHandler):
    def initialize(self, CP, name):
        self.CP = CP
        self.name = name

    def open(self):
        if hasattr(self.application, 'clients') is False:
            self.application.clients = {}
        if self.name not in self.application.clients:
            self.application.clients[self.name] = []
        self.application.clients[self.name].append(self)

    def on_close(self):
        self.application.clients[self.name].remove(self)

    def on_message(self, message):
        self.write_message(message)


class WebEmulate(JSONHandler):
    def get(self):
        self.CP.emulate('tag_placed', self.get_argument('tag'))
        self.CP.emulate('tag_removed', self.get_argument('tag'))
        self.write(json.dumps(True))


class SocketListenTaps(SocketHandler):
    pass
