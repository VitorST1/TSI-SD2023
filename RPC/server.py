# server.py

import getopt
import sys
from rpc.server import Server

HOST = '127.0.0.1'
PORT = 6001

def main(port):
    server = Server(HOST, port or PORT)
    server.start()

if __name__ == '__main__':
    # Get command line arguments
    opts, args = getopt.getopt(sys.argv[1:], "p:", ["port="])
    port = None

    # Get the port number
    for opt, arg in opts:
        if opt in ("-p", "--port"):
            port = int(arg)
    
    main(port)