from observer import Observer
from logger import Logger
from server import Server
from smartcard.CardMonitoring import CardMonitor

class ContactPoint:
    """
    ContactPoint is the central class of the application.
    """
    debug = False
    local_config = {}
    listening = False

    def __init__(self, debug = False):
        '''
        Initialises the debug mode, logger, loads the last state of the
        application, and performs an initial system synchronisation from the
        cloud.
        '''
        self.debug = debug
        self.init_emulator()
        self.logger = Logger(debug)
        self.logger.log('System started...')
        self.server = Server(self, debug)

    def process(self, tag):
        '''
        The process function is called each time a card is tapped onto the
        reader. It identifies if the card is an admin. If it is an admin card,
        it pushes this data forward to clients, if any. If it not an admin
        card, it queues it up to be processed for making an action API call.
        '''
        self.logger.debug("Card tapped: " + tag)
        self.server.send_msg('tap', dict(tap = tag))

    def init_emulator(self):
        '''
        If the application is running in development mode, the process method is
        aliased as emulate too. This is for nomenclature convenience. This function
        shall be called as emulate, to emulate card taps in development mode.
        '''
        if self.debug is True:
            self.emulate = self.process

    def listen(self):
        '''
        The listen function is called during initialisation of the class & the
        application. It initialises the process of starting to listen to card taps
        on the reader.
        '''
        self.monitor = CardMonitor()
        self.observer = Observer(self)
        self.monitor.addObserver(self.observer)
