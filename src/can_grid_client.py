
import logging
import threading
import select
import time
import sys
import socket
import binascii
from threading import Thread
from opc import *
import queue

#class that deals with the can grid messages, basically this class holds the client socket and the major code


class CanGridClient(threading.Thread):

    def __init__(self, host, port, incoming_cbus_queue, outgoing_cbus_queue, config, in_cbus_queue_condition, out_cbus_queue_condition):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.config = config
        self.connection = socket.socket()
        self.cbus_out_queue = outgoing_cbus_queue
        self.cbus_in_queue = incoming_cbus_queue
        self.running = True
        self.connected = False
        self.in_cbus_queue_condition = in_cbus_queue_condition
        self.out_cbus_queue_condition = out_cbus_queue_condition
        self.thread_cbus = Thread(target = self.consumeOutCBUSQueue, name="thread_cbus")
        self.name = "CanGridClient"

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
        logging.info("CanGridClient started")

        #start the queue threads
        self.thread_cbus.start()

        size = 1024
        while self.running:
            try:
                if self.connected == False:
                    self.connect()
                #get input messages

                ready = select.select([self.connection], [], [])
                if ready[0]:
                    data = self.connection.recv(size)
                    if len(data) > 0:
                        logging.debug("Received grid data %s " % data)

                        response = data.decode('ascii').split(";:") #:ShhhhNd0d1d2d3d4d5d6d7;

                        for message in response:
                            if (message[0] == ":"):
                                message = message[1:]

                            L = len(message)
                            if (message[L -1] == ";"):
                                message = message[:(L - 1)]
                            with self.in_cbus_queue_condition:
                                self.in_cbus_queue_condition.acquire()
                                self.cbus_in_queue.put(message)
                                self.in_cbus_queue_condition.release()
                                self.in_cbus_queue_condition.notify_all()

                    else:
                        #raise Exception('Client disconnected')
                        logging.debug("Exception in client processing. Closing connection")
                        self.running = False
            except socket.timeout:
                logging.debug("Socket error.")
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
        with self.out_cbus_queue_condition:
            self.out_cbus_queue_condition.acquire()
            self.cbus_out_queue.put(message)
            self.out_cbus_queue_condition.release()
            self.out_cbus_queue_condition.notify_all()

    def consumeOutCBUSQueue(self):
        logging.info("Cangrid thread for outgoing CBUS messages started")
        while self.running:

            while self.cbus_out_queue.empty() == True:
                self.out_cbus_queue_condition.acquire()
                self.out_cbus_queue_condition.wait()

            if (self.cbus_out_queue.empty() == False):
                self.out_cbus_queue_condition.acquire()
                message = self.cbus_out_queue.get()
                self.out_cbus_queue_condition.release()
                logging.debug("Sending grid message %s" % (message))
                self.connection.send(message.encode('ascii'))

