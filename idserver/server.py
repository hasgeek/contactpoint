import os
from serverhandlers import *
import hashlib
from tornado import ioloop

class Server(web.Application):
    clients = {}

    def __init__(self, CP, debug = False):
        self.CP = CP
        if debug is True:
            host = '0.0.0.0'
        else:
            host = '127.0.0.1'

        handlers = [
            (r"/card_id.json", WebCardId, dict(CP = CP)),
            (r"/print/(.*)/(.*)", WebPrintTwitter, dict(CP = CP)),
            (r"/listen_taps", SocketListenTaps, dict(CP = CP, name = 'listen_taps'))
        ]

        if debug:
            handlers.append((r"/emulate", WebEmulate, dict(CP = CP)))
        
        return super(Server, self).__init__(
            handlers = handlers,
            default_host = host,
            debug = debug,
            template_path = os.path.join(os.path.dirname(__file__), "templates"),
            static_path = os.path.join(os.path.dirname(__file__), "static"),
            cookie_secret = hashlib.md5('server_cookie_data_asfjanfjdnf').hexdigest(),
            login_url = '/'
        )

    def listen(self, port):
        self.CP.logger.log('Loading Server...')
        try:
            super(Server, self).listen(port = port)
            self.CP.logger.log('Server Ready & Listening on http://%s:%s ...' % (self.default_host, port))
            ioloop.IOLoop.instance().start()
        except Exception, e:
            self.CP.logger.log('Error in starting server: ' + e.message)

    def send_msg(self, to, msg):
        for client in self.clients[to]:
            client.write_message(msg)