
import logging
import threading
import select
import time
import sys
import socket
import binascii
from opc import *
import queue

#class that deals with the can grid messages, basically this class holds the client socket and the major code


class CanGridClient(threading.Thread):

    def __init__(self, host, port, incoming_cbus_queue, outgoing_cbus_queue, config):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.config = config
        self.connection = socket.socket()
        self.cbus_out_queue = outgoing_cbus_queue
        self.cbus_in_queue = incoming_cbus_queue
        self.running = True
        self.connected = False

    def stop(self):
        self.running = False

    def connect(self):
        tries = 20
        i = 1
        while(i < tries):
            try:
                logging.debug("Connecting to host %s port %s" % (self.host, self.port))
                result = self.connection.connect_ex((self.host, self.port))
                if result:
                    self.connected = True
                    logging.debug("Connected")
                    break
            except socket.timeout:
                logging.debug("Retrying %d of %d" % (i, tries))
                i += 1
                time.sleep(2)

    #main loop thread function
    def run(self):

        #start the queue threads
        self.consumeOutCBUSQueue()

        size = 1024
        while self.running:
            try:
                if not self.connected:
                    self.connect()
                #get input messages

                ready = select.select([self.connection], [], [], 1)
                if ready[0]:
                    data = self.connection.recv(size)
                    if data:
                        response = data.split(';:') #:ShhhhNd0d1d2d3d4d5d6d7;

                        for message in response:
                            if (message[0] == ":"):
                                message = message[1:]

                            L = len(message)
                            if (message[L -1] == ";"):
                                message = message[:(L - 1)]

                            self.cbus_in_queue.add(message)

                    else:
                        #raise Exception('Client disconnected')
                        logging.debug("Exception in client processing. Closing connection")
                        self.running = False
            except socket.timeout:
                self.connected = False
                continue
            except BaseException as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.info("Exception in client processing in line %d\n %s" % (exc_tb.tb_lineno, str(e)))
                self.running = False

        logging.debug("Closing can grid connection")

        self.connection.close()
        self.stop()


    # Output CBUS messages thread

    def sendGridMessage(self, message):
        logging.debug("Putting the message in the queue to CBUS: %s" % message)
        self.cbus_out_queue.add(message)

    def __consumeOutCBUSQueue(self):

        while self.running:
            if (self.cbus_out_queue.empty() == False):
                message = self.cbus_out_queue.pop()
                logging.debug("Sending grid message %s" % (message))
                self.connection.send(message.encode('ascii'))

    def consumeOutCBUSQueue(self):
        threading.Thread(target=self.__consumeOutCBUSQueue()).start()

