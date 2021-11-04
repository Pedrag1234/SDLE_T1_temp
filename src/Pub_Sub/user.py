import zmq
import sys
from datetime import datetime


def signal_handler(sig, frame):
    print("USER : TERMINATING PROXY")
    exit(0)


class publisher:

    def __init__(self, id, connection, topic, message):
        self.id = id
        self.connection = connection
        self.topic = topic
        self.sub_socket = zmq.Context().socket(zmq.PUB)
        self.message = message

    def connect(self):
        try:
            self.sub_socket.connect(self.connection)
        except:
            print("PUBLISHER : CONNECTION FAILED. EXITING")
            sys.exit(-1)

    def put(self):
        msg = "{topic}: {id} - {time} - {message}".format(
            topic=self.topic, id=self.id, time=datetime.now().strftime("%H:%M:%S"), message=self.message)
        print("USER_SND : " + msg)
        self.sub_socket.send_string(msg)

    def run(self):
        self.connect()
        self.put()


class subscriber:

    def __init__(self, id, connection, topic):
        self.id = id
        self.connection = connection
        self.topic = topic
        self.sub_socket = zmq.Context().socket(zmq.SUB)

    def connect(self):
        try:
            self.sub_socket.connect(self.connection)
        except:
            print("SUBSCRIBER : CONNECTION FAILED. EXITING")
            sys.exit(-1)

    def subscribe(self):
        self.sub_socket.setsockopt_string(zmq.SUBSCRIBE, self.topic)

    def unsubscribe(self):
        self.sub_socket.unsubscribe(self.topic)

    def receive(self):
        while True:
            try:
                print("USER_RCV : " + self.sub_socket.recv(zmq.NOBLOCK))
            except:
                pass

    def run(self):
        self.connect()
        self.subscribe()
        self.receive()


def printUsage():
    print("Usage : ./pub_sub -<pub/sub> <id> <connection> <topic> <message>")
    print("Example : ")
    print("      For publishers: ./pub_sub -pub 1 tcp://*:5560 football gandagolo")
    print("      For subscribers: ./pub_sub -sub 1 tcp://*:5561 football")


def _main():
    args = sys.argv[1:]
    print(args)

    if len(args) != 4 and len(args) != 5:
        printUsage()
        sys.exit(0)

    if args[0] == "-pub":
        pub = publisher(args[1], args[2], args[3], args[4])
        pub.run()
    elif args[0] == "-sub":
        sub = subscriber(args[1], args[2], args[3])
        sub.run()
    else:
        printUsage()
        sys.exit(0)


if __name__ == "__main__":
    _main()
