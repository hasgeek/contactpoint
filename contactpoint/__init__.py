import instance.env
from os import environ

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

    def __init__(self):
        '''
        Initialises the debug mode, logger.
        '''
        self.env = environ['CONTACTPOINT_ENV']
        if self.env == 'development':
            self.debug = True
        self.init_emulator()
        self.logger = Logger(self.debug)
        self.logger.log('System started...')
        self.server = Server(self, self.debug)
        self.listen()

    def process(self, action, tag_id=None):
        '''
        The process function is called each time an action happens on the RFID
        reader.
        '''
        response = dict(action=action)
        if tag_id is not None:
            response['tag_id'] = tag_id
        self.logger.debug(response)
        self.server.send_msg('listen_taps', response)

    def init_emulator(self):
        '''
        If the application is running in development mode, the process method is
        aliased as emulate too. This is for nomenclature convenience. This
        function shall be called as emulate, to emulate card taps in development
        mode.
        '''
        if self.debug is True:
            self.emulate = self.process

    def listen(self):
        '''
        The listen function is called during initialisation of the class & the
        application. It initialises the process of starting to listen to card
        taps on the reader.
        '''
        self.monitor = CardMonitor()
        self.observer = Observer(self)
        self.monitor.addObserver(self.observer)
