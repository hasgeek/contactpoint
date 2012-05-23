from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException
from smartcard.System import readers
from smartcard.util import toHexString

from flask import Flask
from coaster.views import jsonp

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from os import popen

GET_ID = [0xFF, 0xCA, 0x00, 0x00, 0x04]  # Get serial number for Mifare NFC

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, world!"


@app.route('/card_id.json')
def card_id():
    response = None
    try:
        for reader in readers():
            try:
                connection = reader.createConnection()
                connection.connect()
                response, sw1, sw2 = connection.transmit(GET_ID)
                tag = toHexString(response).replace(" ", "")
                if len(tag)<8:
                    response = jsonp(card_id=None, error='invalid_id')
                response = jsonp(card_id=tag)
            except (NoCardException, CardConnectionException):
                response = jsonp(card_id=None, error='no_card')
    except EstablishContextException:
        response = jsonp(card_id=None, error='no_pcscd')
    if response is None:
        response = jsonp(card_id=None, error='no_reader')

    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


@app.route('/print/<name>/<twitter>', methods=['POST'])
def label(name, twitter):
    c = canvas.Canvas(name.split()[0]+".pdf", pagesize=(90*mm, 29*mm))
    c.drawCentredString(45*mm, 20*mm, name);
    c.setFontSize(10)
    c.drawCentredString(45*mm, 15*mm, twitter);
    c.showPage()
    try:
        c.save()
        popen("lpr "+name.split()[0]+".pdf")
        return "success"
    except:
        return "fail"




if __name__ == '__main__':
    app.run('127.0.0.1', 8008, debug=True)
