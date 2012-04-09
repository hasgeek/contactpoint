from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.System import readers
from smartcard.util import toHexString

from flask import Flask
from coaster.views import jsonp

GET_ID=[0xFF, 0xCA, 0x00, 0x00, 0x04] #Get Serial Number

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, world!"

@app.route('/card_id.json')
def card_id():
    for reader in readers():
        try:
            connection = reader.createConnection()
            connection.connect()
            response, sw1, sw2 = connection.transmit(GET_ID)
            tag = toHexString(response).replace(" ","")
            return jsonp(card_id=tag)
        except (NoCardException, CardConnectionException):
            return jsonp(card_id=None)
    return jsonp(card_id=None)

if __name__=='__main__':
    app.run(debug=True)
