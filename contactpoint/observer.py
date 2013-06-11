from smartcard.CardMonitoring import CardObserver
from smartcard.util import toHexString
from smartcard.Exceptions import NoCardException, CardConnectionException
from smartcard.pcsc.PCSCExceptions import EstablishContextException
from smartcard.System import readers
from time import sleep

GET_ID=[0xFF, 0xCA, 0x00, 0x00, 0x04] #Get Serial Number

class Observer( CardObserver ):
    "This is notified with card events"
    
    def __init__(self, CP):
        self.CP = CP

    def update( self, observable, (addedcards, removedcards) ):
        
        for card in addedcards:
            try:
                card.connection = card.createConnection()
                card.connection.connect()
                response, sw1, sw2 = card.connection.transmit( GET_ID )
                card.tag_id = toHexString(response).replace(" ","")
                self.CP.process('tag_placed', card.tag_id)
            except Exception as e:
                pass
        for card in removedcards:
            try:
                self.CP.process('tag_removed', card.tag_id)
                card.connection.disconnect()
            except Exception as e:
                pass