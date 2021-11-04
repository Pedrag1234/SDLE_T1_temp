import sys
import signal
import zmq
from zmq.backend import proxy


def signal_handler(sig, frame):
    print("PROXY : TERMINATING PROXY")
    exit(0)


class Proxy:
    def __init__(self, xsub_connection, xpub_connection):
        self.context = zmq.Context()
        self.xsub_socket = self.context.socket(zmq.XSUB)
        self.xpub_socket = self.context.socket(zmq.XPUB)
        self.xsub_connection = xsub_connection
        self.xpub_connection = xpub_connection

    def run(self):
        print("***********************************************************************")
        print("PROXY : STARTING XSUB SOCKET")

        try:
            self.xsub_socket.bind(self.xsub_connection)
        except:
            print("PROXY : ERROR BINDING XSUB SOCKET TO CONNECTION. EXITING")
            sys.exit(-1)

        print("PROXY : STARTED XSUB SOCKET")
        print("***********************************************************************")
        print("PROXY : STARTING XPUB SOCKET")

        try:
            self.xpub_socket.bind(self.xpub_connection)
        except:
            print("PROXY : ERROR BINDING XPUB SOCKET TO CONNECTION. EXITING")
            sys.exit(-1)

        print("PROXY : STARTED XSUB SOCKET")
        print("***********************************************************************")
        print("PROXY : PROXY STARTED")
        zmq.proxy(self.xsub_socket, self.xsub_socket)


def _main():
    args = sys.argv[1:]

    if len(args) != 2:
        print("Usage: ./proxy <xsub_connection> <xpub_connection> ")
        print("Ex: ./proxy tcp://*:5560 tcp://*:5561")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    proxy = Proxy(args[0], args[1])
    proxy.run()


if __name__ == "__main__":
    _main()
