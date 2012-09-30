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


class WebCardId(WebHandler):
    def get(self):
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
                    response = jsonp(card_id=None, error='no_card')
        except EstablishContextException:
            response = dict(card_id=None, error='no_pcscd')
        if response is None:
            response = dict(card_id=None, error='no_reader')

        #response.headers['Cache-Control'] = 'no-store'
        #response.headers['Pragma'] = 'no-cache'
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


class WebEmulate(WebHandler):
    def get(self):
        self.CP.emulate(self.get_argument('tag'))
        self.write(jsonp(True))


class SocketListenTaps(SocketHandler):
    pass
