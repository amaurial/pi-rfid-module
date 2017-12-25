from opc import *
import logging
from cbus_node import CBUSNode
from threading import Thread
import binascii


class RfidNode(CBUSNode):

    def __init__(self,rfid_queue, incoming_cbus_queue, outgoing_cbus_queue, config, in_cbus_queue_condition, out_cbus_queue_condition, in_rfid_queue_condition):
        self.rfid_queue = rfid_queue
        self.config = config
        self.running = True
        self.out_cbus_queue_condition = out_cbus_queue_condition
        self.in_cbus_queue_condition = in_cbus_queue_condition
        self.in_rfid_queue_condition = in_rfid_queue_condition
        super().__init__(incoming_cbus_queue, outgoing_cbus_queue, config, in_cbus_queue_condition, out_cbus_queue_condition )
        self.rfid_thread = Thread(target=self.consumeRFIDQueue, name="rfid_thread")
        self.name = "RfidNode"

    def run(self):
        logging.info("RfidNode started")

        self.rfid_thread.start()

        while self.running:
            #consume CBUS messages
            self.consumeCBUSQueue()

    #consume all items from the queue
    def consumeRFIDQueue(self):
        # queue is in the format
        # <sensor_id>;<rfid>
        while self.running:

            while self.rfid_queue.empty() == True:
                self.in_rfid_queue_condition.acquire()
                self.in_rfid_queue_condition.wait()

            if self.rfid_queue.empty() == False:
                logging.debug("Queue has %d items" % (self.rfid_queue.qsize()))

            try:

                while self.rfid_queue.empty() == False:
                    item = self.rfid_queue.get()

                    if item is None:
                        break

                    data = item.split(";")
                    message = self.createGridMessage(OPC_ASON2, data[0], data[1])

                    with self.out_cbus_queue_condition:
                        self.out_cbus_queue_condition.acquire()
                        self.cbus_out_queue.put(message)
                        self.out_cbus_queue_condition.release()
                        self.out_cbus_queue_condition.notify_all()

            except Exception as e:
                logging.debug("Exception while processing the queue\n%s" %(e))
            finally:
                self.in_rfid_queue_condition.release()

    # build a grid message to send
    def createGridMessage(self, opc, sensor_id, rfid):

        # The GridConnect protocol encodes messages as an ASCII string of up to 24 characters of the form:
        # :ShhhhNd0d1d2d3d4d5d6d7;
        # standard frame
        CAN_SFF_MASK = 0x000007ff
        frametype = "N"
        c = 5 #priority 0101
        d = c << 8
        tempcanid = d | int(self.config.canid & CAN_SFF_MASK)

        h2 = int(tempcanid << 5) & 0xff
        h1 = int(tempcanid >> 3) & 0xff
        opchex = binascii.hexlify(opc)

        message = ":S%02X%02X%s%02X%04X%04X;" % (h1, h2, frametype, int(opchex, 16), int(rfid), int(sensor_id))
        return message

    def nodeLogic(self, message):
        logging.debug("Node received message from CBUS %s" % message)