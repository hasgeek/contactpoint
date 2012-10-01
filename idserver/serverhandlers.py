from tornado import web, websocket

from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException
from smartcard.System import readers
from smartcard.util import toHexString
from coaster.views import jsonp

#Importing json to make this work right now. Not delving deeper into coaster's jsonp as of now.
import simplejson as json

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from os import popen

class WebHandler(web.RequestHandler):
    def initialize(self, CP):
        self.CP = CP

#Reference: http://stackoverflow.com/questions/9336392/jsonp-requests-with-tornado
class JSONPHandler(WebHandler):
    def write(self, data):
        self.set_header('Content-Type', 'application/javascript')
        super(JSONPHandler, self).write('callback(' + json.dumps(data) + ')')
        '''
        callback needs to be replaced with the function name that would get called.
        But, why even get into that if we are implementing WebSockets!? :D
        '''

class JSONHandler(WebHandler):
    def write(self, data):
        self.set_header('Content-Type', 'application/json')
        super(JSONHandler, self).write(data)

class SocketHandler(websocket.WebSocketHandler):
    def initialize(self, CP, name):
        self.CP = CP
        self.name = name

    def open(self):
        if self.name not in self.application.clients:
            self.application.clients[self.name] = []
        self.application.clients[self.name].append(self)

    def on_close(self):
        self.application.clients[self.name].remove(self)

    def on_message(self, message):
        self.write_message(message)


class WebCardId(JSONPHandler):
    def get(self):
        GET_ID=[0xFF, 0xCA, 0x00, 0x00, 0x04] #Get Serial Number
        response = None
        try:
            for reader in readers():
                try:
                    connection = reader.createConnection()
                    connection.connect()
                    response, sw1, sw2 = connection.transmit(GET_ID)
                    tag = toHexString(response).replace(" ", "")
                    if len(tag)<8:
                        response = dict(card_id=None, error='invalid_id')
                    response = dict(card_id=tag)
                except (NoCardException, CardConnectionException):
                    response = dict(card_id=None, error='no_card')
        except EstablishContextException:
            response = dict(card_id=None, error='no_pcscd')
        if response is None:
            response = dict(card_id=None, error='no_reader')

        self.set_header("Pragma", "no-cache")
        self.set_header("Cache-Control", "no-store")
        self.write(json.dumps(response))

class WebPrintTwitter(WebHandler):
    def get(self, name, twitter):
        c = canvas.Canvas(name.split()[0]+".pdf", pagesize=(70*mm, 29*mm))
        c.setFontSize(18)
        c.drawCentredString(35*mm, 18*mm, name);
        c.setFontSize(13)
        c.drawCentredString(35*mm, 12*mm, twitter);
        c.showPage()
        try:
            c.save()
            popen("lpr "+name.split()[0]+".pdf")
            self.write("success")
        except:
            self.write("fail")


class WebEmulate(JSONHandler):
    def get(self):
        self.CP.emulate(self.get_argument('tag'))
        self.write(json.dumps(True))


class SocketListenTaps(SocketHandler):
    pass
