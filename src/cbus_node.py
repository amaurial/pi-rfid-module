from opc import *
import queue
import threading
import logging
import binascii

class CBUSNode(threading.Thread):

    def __init__(self, incoming_cbus_queue, outgoing_cbus_queue, config, in_cbus_queue_condition, out_cbus_queue_condition):
        threading.Thread.__init__(self)
        self.config = config
        self.cbus_out_queue = outgoing_cbus_queue
        self.cbus_in_queue = incoming_cbus_queue
        self.running = True
        self.cbus_stopped = False
        self.setup_mode = False
        self.out_cbus_queue_condition = out_cbus_queue_condition
        self.in_cbus_queue_condition = in_cbus_queue_condition
        self.name = "CBUSNode"

    def run(self):
        logging.info("CBUSNode started")
        while self.running:
            #consume cbus messages
            self.consumeCBUSQueue()
            logging.info("4444444")


    def consumeCBUSQueue(self):

        while self.cbus_in_queue.empty() == True:
            self.in_cbus_queue_condition.acquire()
            self.in_cbus_queue_condition.wait()

        if self.cbus_in_queue.empty() == False:
            self.in_cbus_queue_condition.acquire()
            message = self.cbus_in_queue.get()
            self.in_cbus_queue_condition.release()
            data = self.parseCBUSMessage(message)
            if len(data) == 0:
                logging.debug("Empty data. Not processing")
                return
            logging.debug("Received CBUS message %s" % message)
            if (data[0] in [OPC_QNN, OPC_RQMN, OPC_RQNP, OPC_RQEVN, OPC_SNN, OPC_ENUM, OPC_HLT,
                        OPC_BON, OPC_BOOT, OPC_ARST, OPC_CANID, OPC_NVSET, OPC_RQNPN,
                        OPC_NVRD]):
                        self.handleCBUSMessages(data)
            else:
                self.nodeLogic(data)

    def stop(self):
        self.running = False

    def parseCBUSMessage(self, message):

        # The GridConnect protocol encodes messages as an ASCII string of up to 24 characters of the form:
        # :ShhhhNd0d1d2d3d4d5d6d7;
        # The S indicates a standard CAN frame
        # :XhhhhhhhhNd0d1d2d3d4d5d6d7;
        # The X indicates an extended CAN frame hhhh is the two byte header N or R indicates a normal
        # or remote frame, in position 6 or 10 d0 - d7 are the (up to) 8 data bytes

        cdata = []
        for i in range(8):
            cdata.insert(i, 0)

        #ignore extended events
        if ("X" in message or "x" in message):
            logging.debug("Extended frames. Skipping")
            return cdata

        spos = message.find("N")
        if (spos < 0):
            spos = message.find("n")
            if (spos < 0):
                logging.debug("Message is not standard frame. Skipping")
                return cdata

        data = message[spos + 1:].encode("ascii")
        datahex = binascii.unhexlify(data)
        for i in range(len(datahex)):
            cdata[i] = datahex[i]

        return cdata


    # build a grid message to send
    def createGridMessage(self, b1, b2, b3, b4, b5, b6, b7, b8):

        # The GridConnect protocol encodes messages as an ASCII string of up to 24 characters of the form:
        # :ShhhhNd0d1d2d3d4d5d6d7;
        # standard frame

        frametype = "N"
        c = 5 #priority 0101
        d = c << 8
        tempcanid = d | int(self.config.canid & CAN_SFF_MASK)

        h2 = int(tempcanid << 5) & 0xff
        h1 = int(tempcanid >> 3) & 0xff

        #message = ":S%02X%02X%s%02X%04X%04X;" % (h1, h2, frametype, int(opchex, 16), int(rfid), int(sensor_id))

        message = ":S%02X%02X%s%" % (h1, h2, frametype)
        if (b1 != None):
            message = "%s%02X" % (message, b1)
        else:return message + ";"

        if (b2 != None):
            message = "%s%02X" % (message, b2)
        else:return message + ";"

        if (b3 != None):
            message = "%s%02X" % (message, b3)
        else:return message + ";"

        if (b4 != None):
            message = "%s%02X" % (message, b4)
        else:return message + ";"

        if (b5 != None):
            message = "%s%02X" % (message, b5)
        else:return message + ";"

        if (b6 != None):
            message = "%s%02X" % (message, b6)
        else:return message + ";"

        if (b7 != None):
            message = "%s%02X" % (message, b7)
        else:return message + ";"

        if (b8 != None):
            message = "%s%02X;" % (message, b8)

        return message

    #function to be override
    def nodeLogic(self, message):
        pass

    def putGridMessageInQueue(self, message):
        if self.cbus_stopped:
            logging.debug("CBUS stopped. Dropping the message")
            return

        with self.out_cbus_queue_condition:
            self.cbus_out_queue.put(message)
            self.out_cbus_queue_condition.notify_all()

    #receive all the can message
    def handleCBUSMessages(self, message):
        logging.debug("Handling CBUS message: %s" % message)

        opc = message[0]

        if opc == OPC_QNN:
            self.handleQNN(message)

        if opc == OPC_RQNP:
            self.handleRQNP(message)

        if opc == OPC_RQEVN:
            self.handleRQEVN(message)

        if opc == OPC_RQMN:
            self.handleRQMN(message)

        if opc == OPC_RQNPN:
            self.handleRQNPN(message)

        if opc == OPC_NVRD:
            self.handleNVRD(message)

        if opc == OPC_SNN:
            self.handleSNN(message)

        if opc == OPC_ENUM:
            self.handleENUM(message)

        if opc == OPC_HLT:
            self.handleHLT(message)

        if opc == OPC_BON:
            self.handleBON(message)

        if opc == OPC_BOOT:
            self.handleBOOT(message)

        if opc == OPC_ARST:
            self.handleARST(message)

        if opc == OPC_CANID:
            self.handleCANID(message)

        if opc == OPC_NVSET:
            self.handleNVSET(message)


    def handleQNN(self, message):

        if self.setup_mode:
            return

        Lb = self.config.node_number & 0xff
        Hb = (self.config.node_number >> 8) & 0xff
        logging.debug("Sending response for QNN.")
        gridmsg = self.createGridMessage(OPC_PNN, Hb, Lb, self.node_config.manufacturer_id, self.node_config.module_id, self.node_config.getFlags())
        self.putGridMessageInQueue(gridmsg)

    def handleRQNP(self, message):

        if not self.setup_mode:
            return

        Lb = message[2]
        Hb = message[1]

        logging.debug("Sending response for RQNP.")
        gridmsg = self.createGridMessage(OPC_PARAMS, self.node_config.manufacturer_id, self.node_config.minor_code_version,
                                         self.node_config.module_id, self.node_config.number_of_events, self.node_config.event_variables_per_event,
                                         self.node_config.number_of_node_variables, self.node_config.major_code_version)
        self.putGridMessageInQueue(gridmsg)

    def handleRQEVN(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        if tnn != self.node_config.node_number:
            logging.debug("RQEVN is for another node. My nn: %d received nn: %d" % (self.node_config.node_number, tnn))
            return

        Lb = self.config.node_number & 0xff
        Hb = (self.config.node_number >> 8) & 0xff
        logging.debug("Sending response for RQEVN.")

        gridmsg = self.createGridMessage(OPC_NUMEV, Hb, Lb, len(self.node_config.events))
        self.putGridMessageInQueue(gridmsg)

    def handleRQMN(self, message):

        if not self.setup_mode:
            return
        logging.debug("Sending response for NAME.")
        gridmsg = self.createGridMessage(OPC_NAME, self.node_config.name[0],
                                         self.node_config.name[1],
                                         self.node_config.name[2],
                                         self.node_config.name[3],
                                         self.node_config.name[4],
                                         self.node_config.name[5],
                                         self.node_config.name[6])
        self.putGridMessageInQueue(gridmsg)

    def handleRQNPN(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        if tnn != self.node_config.node_number:
            logging.debug("RQNPN is for another node. My nn: %d received nn: %d" % self.node_config.node_number, tnn)
            return

        if message[3] > self.node_config.number_of_node_variables:
            #index invalid
            gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INV_PARAM_IDX)
            self.putGridMessageInQueue(gridmsg)
            return

        p = self.node_config.node_variables[message[3]]
        if message[3] == 0:
            p = self.node_config.number_of_node_variables

        gridmsg = self.createGridMessage(OPC_PARAN, Hb, Lb, message[3], p)
        self.putGridMessageInQueue(gridmsg)

    def handelNVRD(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb
        if tnn != self.node_config.node_number:
            logging.debug("NVRD is for another node. My nn: %d received nn: %d" % self.node_config.node_number, tnn)
            return

        if (message[3] > self.node_config.number_of_node_variables or message[3] == 0):
            #index invalid
            gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INV_PARAM_IDX)
            self.putGridMessageInQueue(gridmsg)
            logging.debug("NVRD Invalid index %d" % message[3])
            return

        gridmsg = self.createGridMessage(OPC_NVANS, Hb, Lb, message[3], self.node_config.node_variables[message[3]])
        self.putGridMessageInQueue(gridmsg)
        logging.debug("NVRD processed. Sent NVANS")

    def handleNVSET(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb
        if tnn != self.node_config.node_number:
            logging.debug("NVSET is for another node. My nn: %d received nn: %d" % self.node_config.node_number, tnn)
            return

        if (message[3] > self.node_config.number_of_node_variables() or message[3] == 0):
            #index invalid
            gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INV_PARAM_IDX)
            self.putGridMessageInQueue(gridmsg)
            logging.debug("NVSET Invalid index %d" % message[3])
            return

        #1 error, 2 reconfigure , 3 restart the service
        idx = message[3]
        data = message[4]
        self.node_config.node_variables[idx] = data

        gridmsg = self.createGridMessage(OPC_WRACK, Hb, Lb)
        self.putGridMessageInQueue(gridmsg)
        logging.debug("NVSET ok. Sent wrack")

    def handleSNN(self, message):

        if not self.setup_mode:
            return

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        logging.debug("Saving node number %d." % tnn)
        self.node_config.node_number = tnn

        logging.debug("Save node number success.")

        Lb = self.node_config.node_number & 0xff
        Hb = (self.node_config.node_number >> 8) & 0xff

        gridmsg = self.createGridMessage(OPC_NNACK, Hb, Lb)
        self.putGridMessageInQueue(gridmsg)
        self.setup_mode = False

    def handleCANID(self, message):

        if self.setup_mode:
            return

        logging.debug("Received set CANID.")
        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb
        if tnn != self.node_config.node_number:
            logging.debug("Set CANID is for another node. My nn: %d received nn: %d" % self.node_config.node_number, tnn)
            return

        logging.debug("Virtual node does not have canid. Sending error")
        Lb = self.node_config.node_number & 0xff
        Hb = (self.node_config.node_number >> 8) & 0xff
        gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INVALID_EVENT)
        self.putGridMessageInQueue(gridmsg)

    def handleENUM(self, message):

        logging.debug("Virtual node does not have canid.")
        return

    def handleHLT(self, message):

        if self.setup_mode:
            return

        logging.info("Stopping CBUS")
        self.cbus_stopped = True

    def handleBON(self, message):

        if self.setup_mode:
            return

        logging.info("Enabling CBUS")
        self.cbus_stopped = False

    def handleARST(self, message):

        if self.setup_mode:
            return

        logging.info("Enabling CBUS")
        self.cbus_stopped = False

    def handleBOOT(self, message):

        if self.setup_mode:
            return

        logging.info("BOOT received. Do nothing")

