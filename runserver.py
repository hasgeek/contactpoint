#!/usr/bin/env python
import argparse
import socket
from os import environ
from contactpoint import ContactPoint
from contactpoint.host2ip import start_host2ip

# Init ContactPoint
CP = ContactPoint()

app = CP.server

'''
This initializes the application
'''
if __name__ == "__main__":

    if 'PEOPLEFLOW_HOSTNAME' in environ:
        start_host2ip(CP, 60)

    port = 8008

    '''
    Better command line argument parsing
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='Run the application using the port specified', type=int)
    args = parser.parse_args()
    if args.port:
        port = args.port

    try:
        app.listen(port)
    except KeyboardInterrupt:
        CP.logger.log('Server forced closed by user.')
