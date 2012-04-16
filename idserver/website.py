from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException
from smartcard.System import readers
from smartcard.util import toHexString

from flask import Flask
from coaster.views import jsonp

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


if __name__ == '__main__':
    app.run('127.0.0.1', 8008, debug=False)
