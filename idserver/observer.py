from smartcard.CardMonitoring import CardObserver
from smartcard.util import toHexString
from time import sleep

GET_ID=[0xFF, 0xCA, 0x00, 0x00, 0x04] #Get Serial Number

class Observer( CardObserver ):
    "This is notified with card events"
    
    def __init__(self, server):
        self.server = server

    def update( self, observable, (addedcards, removedcards) ):
        
        for card in addedcards:
            try:
                card.connection = card.createConnection()
                card.connection.connect()
                response, sw1, sw2 = card.connection.transmit( GET_ID )
                card.connection.disconnect()
                tag = toHexString(response).replace(" ","")
                self.server.process(tag)
            except Exception as e:
                pass