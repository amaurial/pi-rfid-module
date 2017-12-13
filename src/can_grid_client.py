
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


    def __init__(self, host, port, rfid_queue, config, node_config):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.rfid_queue = rfid_queue
        self.config = config
        self.connection = socket.socket()
        self.cbus_out_queue = queue.Queue()
        self.cbus_in_queue = queue.Queue()
        self.running = True
        self.connected = False
        self.node_config = node_config

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

                #consume the output queue
                if self.connected:
                    self.consumeRFIDQueue()

                #get input messages

                ready = select.select([self.connection], [], [], 1)
                if ready[0]:
                    data = self.connection.recv(size)
                    if data:
                        response = data
                        self.handleMessages(data.decode("utf-8"))
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

    #consume all items from the queue
    def consumeRFIDQueue(self):
        # queue is in the format
        # <sensor_id>;<rfid>

        if self.rfid_queue.empty() == False:
            logging.debug("Queue has %d items" % (self.rfid_queue.qsize()))

        try:

            while self.rfid_queue.empty() == False:
                item = self.rfid_queue.get()

                if item is None:
                    break

                data = item.split(";")
                message = self.createGridMessage(OPC_ASON2, data[0], data[1])
                self.cbus_out_queue.add(message)
        except Exception as e:
            logging.debug("Exception while processing the queue\n%s" %(e))

    # build a grid message to send
    def createGridMessage(self, opc, sensor_id, rfid):

        # The GridConnect protocol encodes messages as an ASCII string of up to 24 characters of the form:
        # :ShhhhNd0d1d2d3d4d5d6d7;
        # standard frame
        CAN_SFF_MASK = 0x000007ff
        frametype = "N"
        c = 5 #priority 0101
        d = c << 8
        tempcanid = d | int(self.config["config"]["canid"] & CAN_SFF_MASK)

        h2 = int(tempcanid << 5) & 0xff
        h1 = int(tempcanid >> 3) & 0xff
        opchex = binascii.hexlify(opc)

        message = ":S%02X%02X%s%02X%04X%04X;" % (h1, h2, frametype, int(opchex, 16), int(rfid), int(sensor_id))
        return message

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


# Input CBUS message Thread
    def __consumeInCBUSQueue(self):

        while self.running:
            if (self.cbus_in_queue.empty() == False):
                message = self.cbus_in_queue.pop()
                logging.debug("Received CBUS message %s" % (message))
                self.handleCBUSMessages(message)


    def consumeInCBUSQueue(self):
        threading.Thread(target=self.__consumeInCBUSQueue()).start()


    #receive all the can message
    def handleCBUSMessages(self, message):
        logging.debug("Handling CBUS message: %s" % message)




