from _typeshed import Self
import zmq


class client:
    def __init__(self, pub_connection, sub_connection, sub_topic, pub_topic):
        self.context = zmq.Context()
        self.pub_socket = self.context.socket(zmq.PUB)
        self.sub_socket = self.context.socket(zmq.SUB)
        self.poller_socket = self.connect.soc
        self.pub_connection = pub_connection
        self.sub_connection = sub_connection
        self.sub_topic = sub_topic
        self.pub_topic = pub_topic

    def connect(self):
        self.pub_socket.connect(self.pub_connection)
        self.sub_socket.connect(self.sub_connection)

    def subscribe(self):
        for topic in range(self.sub_topics):
            self.sub_socket.setsockopt(zmq.SUBSCRIBE, topic)

    def unsubscribe(self):
        for topic in range(self.sub_topics):
            self.sub_socket.setsockopt(zmq.UNSUBSCRIBE, topic)

    def get(self):
        self.sub_socket.recv(zmq.DONTWAIT)

    def put(self, message):
        pass


def _main():
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5555")

    #  Do 10 requests, waiting each time for a response
    for request in range(10):
        print("Sending request %s …" % request)
        socket.send(b"Hello")

        #  Get the reply.
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))


if __name__ == "__main__":
    _main()
