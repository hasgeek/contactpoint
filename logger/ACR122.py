from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.util import toHexString
from time import sleep
logs = open('ids_at_booth.txt','a')


GET_ID=[0xFF, 0xCA, 0x00, 0x00, 0x04] #Get Serial Number

class ourobserver( CardObserver ):
    "This is notified with card events"

    def update( self, observable, (addedcards, removedcards) ):
        for card in addedcards:
            try:
                card.connection = card.createConnection()
                card.connection.connect()
                response, sw1, sw2 = card.connection.transmit( GET_ID )
                tag = toHexString(response).replace(" ","")
                logs.write(tag+"\n")
                logs.flush()
                print tag
            except Exception as e:
                pass


cardmonitor = CardMonitor()
cardobserver = ourobserver()
cardmonitor.addObserver( cardobserver )

while True:
    try:
        sleep(1)
    except:
        print "Bye"
        break
