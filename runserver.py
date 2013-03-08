#!/usr/bin/env python
import argparse
from contactpoint import ContactPoint

# Init ContactPoint
CP = ContactPoint()

app = CP.server

'''
This initializes the application
'''
if __name__ == "__main__":
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
