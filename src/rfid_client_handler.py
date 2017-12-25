
import logging
import threading
import select
import re
import time
import sys


class RfidClient(threading.Thread):



    def __init__(self, client, address, rfid_queue, server, id, config, in_rfid_queue_condition):
        threading.Thread.__init__(self)
        self.client = client
        self.address = address
        self.running = True
        self.server = server
        self.id = id
        self.rfid_queue = rfid_queue
        self.config = config
        self.in_rfid_queue_condition = in_rfid_queue_condition
        self.name = "RfidClient-" + self.name
        # constants
        self.RFIDS = "rfids"
        self.ackmessage = "OK\n".encode('utf-8')

    def stop(self):
        self.running = False

    #main loop thread function
    def run(self):
        logging.info("Serving the tcp client %s" % self.address[0])

        size = 1024
        while self.running:
            try:
                ready = select.select([self.client], [], [], 1)
                if ready[0]:
                    data = self.client.recv(size)
                    logging.debug("data: %s" % data)
                    if data:
                        response = data
                        if data[0] == 0xff and len(data) == 1:
                            logging.debug("Empty string")
                        else:
                            self.handleMessages(data.decode("ascii"))
                            self.client.send(self.ackmessage)
                    else:
                        #raise Exception('Client disconnected')
                        logging.debug("Exception in client processing. Closing connection")
                        self.running = False

            except BaseException as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logging.info("Exception in client processing in line %d\n %s" % (exc_tb.tb_lineno, str(e)))
                self.running = False

        logging.debug("Tcp server closing client socket for %s " % self.address[0])

        self.client.close()
        self.stop()
        self.server.removeClient(self.id)

    def handleMessages(self, message):

        logging.debug("Received message %s from client %s"%(message, self.address))
        sensor , rfid = self.parseMessage(message)

        logging.debug("Parsed message %s %s"%(sensor, rfid))
        logging.debug("Doing rfid translation")

        rfid_code = ""
        rfid_int = int(rfid)

        if rfid_int in self.config.config_dictionary[self.RFIDS]:
            rfid_code = self.config.config_dictionary[self.RFIDS][rfid_int]
            logging.debug("Value %s is present and code is %s" % (rfid, rfid_code))
        else:
            rfid_code = rfid[:4]
            logging.debug("%s not in the config. Extracting the first 4 digits %s" % (rfid, rfid_code))
        msg = "%s;%s" % (sensor, rfid_code)

        with self.in_rfid_queue_condition:
            self.in_rfid_queue_condition.acquire()
            self.rfid_queue.put(msg)
            self.in_rfid_queue_condition.release()
            self.in_rfid_queue_condition.notify_all()

    def parseMessage(self, message):
        #message format is "sensor_id;rfid"
        sensor_rfid = message.split(";")
        val = sensor_rfid[1]
        if val[len(val)] == '\n':
            val = val[:len(val) - 1]
        return sensor_rfid[0], val



