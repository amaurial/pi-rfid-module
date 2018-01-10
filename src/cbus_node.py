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
                        OPC_NVRD, OPC_NNLRN, OPC_NNULN, OPC_EVLRN, OPC_NNCLR, OPC_NNEVN]):
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

        if opc == OPC_NNLRN:
            self.handleNNLRN(message)

        if opc == OPC_EVLRN:
            self.handleEVLRN(message)

        if opc == OPC_NNULN:
            self.handleNNULN(message)

        if opc == OPC_NNCLR:
            self.handleNNCLR(message)

        if opc == OPC_NNEVN:
            self.handleNNEVN(message)

    #clear all events from a node
    def handleNNCLR(self,message):
        if self.learn_mode == False:
            return

        logging.debug("Deleting all stored events")
        self.config.events = ''

    #Allows a read of available event space left
    def handleNNEVN(self,message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        if tnn != self.config.node_number:
            logging.debug("RQEVN is for another node. My nn: %d received nn: %d" % (self.config.node_number, tnn))
            return

        nevents = len(self.config.events)
        Lb = self.config.node_number & 0xff
        Hb = (self.config.node_number >> 8) & 0xff
        logging.debug("Sending response for NNEVN.")

        gridmsg = self.createGridMessage(OPC_EVNLF, Hb, Lb, self.config.number_of_events - nevents)
        self.putGridMessageInQueue(gridmsg)

    #query node number
    def handleQNN(self, message):

        if self.setup_mode:
            return

        Lb = self.config.node_number & 0xff
        Hb = (self.config.node_number >> 8) & 0xff
        logging.debug("Sending response for QNN.")
        gridmsg = self.createGridMessage(OPC_PNN, Hb, Lb, self.config.manufacturer_id, self.config.module_id, self.config.getFlags())
        self.putGridMessageInQueue(gridmsg)
    
    #request node parameter
    def handleRQNP(self, message):

        if not self.setup_mode:
            return

        Lb = message[2]
        Hb = message[1]

        logging.debug("Sending response for RQNP.")
        gridmsg = self.createGridMessage(OPC_PARAMS, self.config.manufacturer_id, self.config.minor_code_version,
                                         self.config.module_id, self.config.number_of_events, self.config.event_variables_per_event,
                                         self.config.number_of_node_variables, self.config.major_code_version)
        self.putGridMessageInQueue(gridmsg)
    
    #request number of stored events
    def handleRQEVN(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        if tnn != self.config.node_number:
            logging.debug("RQEVN is for another node. My nn: %d received nn: %d" % (self.config.node_number, tnn))
            return

        Lb = self.config.node_number & 0xff
        Hb = (self.config.node_number >> 8) & 0xff
        logging.debug("Sending response for RQEVN.")

        gridmsg = self.createGridMessage(OPC_NUMEV, Hb, Lb, len(self.config.events))
        self.putGridMessageInQueue(gridmsg)

    #request module name
    def handleRQMN(self, message):

        if not self.setup_mode:
            return
        logging.debug("Sending response for NAME.")
        gridmsg = self.createGridMessage(OPC_NAME, self.config.name[0],
                                         self.config.name[1],
                                         self.config.name[2],
                                         self.config.name[3],
                                         self.config.name[4],
                                         self.config.name[5],
                                         self.config.name[6])
        self.putGridMessageInQueue(gridmsg)

    #Request read of a node parameter by index
    def handleRQNPN(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        if tnn != self.config.node_number:
            logging.debug("RQNPN is for another node. My nn: %d received nn: %d" % self.config.node_number, tnn)
            return

        if message[3] > self.config.number_of_node_variables:
            #index invalid
            gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INV_NV_IDX)
            self.putGridMessageInQueue(gridmsg)
            return

        p = self.config.node_variables[message[3]]
        if message[3] == 0:
            p = self.config.number_of_node_variables

        gridmsg = self.createGridMessage(OPC_PARAN, Hb, Lb, message[3], p)
        self.putGridMessageInQueue(gridmsg)

    #put the node in learn mode
    def handleNNLRN(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        if tnn != self.config.node_number:
            logging.debug("NNLRN is for another node. My nn: %d received nn: %d" % self.config.node_number, tnn)
            return

        self.learn_mode = True

    #finish the learn mode
    def handleNNULN(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        if tnn != self.config.node_number:
            logging.debug("NNULN is for another node. My nn: %d received nn: %d" % self.config.node_number, tnn)
            return

        logging.debug("Saving config")
        self.config.save_config()
        self.learn_mode = False

    #teach an event or a device
    def handleEVLRN(self, message):

        Lb = message[2]
        Hb = message[1]

        if Lb == 0x00 and Hb == 0x00:
            logging.debug("EVLRN teaching a device")
            #TODO
            gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INV_CMD)
            self.putGridMessageInQueue(gridmsg)
            return

        logging.debug("EVLRN teaching an event")
        event = "%02X%02X%02X%02X" % (message[1], message[2], message[3], message[4])

        if varindex > self.config.event_variables_per_event:
            #send error
            gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INV_EV_IDX)
            self.putGridMessageInQueue(gridmsg)
            return

        events = self.config.events
        nevents = len(events)
        evindex = -1
        evexist = False

        for i in range(0, nevents):
            if event in events[i]:
                evindex = i
                evexist = True

        #update variables

        hasvar = False
        if len(message > 5):
            varindex = message[5]
            var = message[6]
            hasvar = True

        if evexist:
            vars = events[evindex][event]['variables']
            if hasvar:
                tempvars = binascii.unhexlify(vars.encode('ascii'))
                tempvars[varindex-1] = var
                vars = binascii.hexlify(tempvars)
                vars=''.join(chr(i) for i in vars)

        #insert new value
        else:
            vars = bytearray([0] * self.config.event_variables_per_event)
            if hasvar:
                vars[varindex] = var
                vars = binascii.hexlify(vars)
                vars=''.join(chr(i) for i in vars)

        events[evindex][event]['variables'] = vars

        #send the ack
        gridmsg = self.createGridMessage(OPC_WRACK)
        self.putGridMessageInQueue(gridmsg)

    #read a node variable
    def handelNVRD(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb
        if tnn != self.config.node_number:
            logging.debug("NVRD is for another node. My nn: %d received nn: %d" % self.config.node_number, tnn)
            return

        if (message[3] > self.config.number_of_node_variables or message[3] == 0):
            #index invalid
            gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INV_PARAM_IDX)
            self.putGridMessageInQueue(gridmsg)
            logging.debug("NVRD Invalid index %d" % message[3])
            return

        gridmsg = self.createGridMessage(OPC_NVANS, Hb, Lb, message[3], self.config.node_variables[message[3]])
        self.putGridMessageInQueue(gridmsg)
        logging.debug("NVRD processed. Sent NVANS")

    #set a node variable
    def handleNVSET(self, message):

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb
        if tnn != self.config.node_number:
            logging.debug("NVSET is for another node. My nn: %d received nn: %d" % self.config.node_number, tnn)
            return

        if (message[3] > self.config.number_of_node_variables() or message[3] == 0):
            #index invalid
            gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INV_PARAM_IDX)
            self.putGridMessageInQueue(gridmsg)
            logging.debug("NVSET Invalid index %d" % message[3])
            return

        #1 error, 2 reconfigure , 3 restart the service
        idx = message[3]
        data = message[4]
        self.config.node_variables[idx] = data

        gridmsg = self.createGridMessage(OPC_WRACK, Hb, Lb)
        self.putGridMessageInQueue(gridmsg)
        logging.debug("NVSET ok. Sent wrack")

    #save node number
    def handleSNN(self, message):

        if not self.setup_mode:
            return

        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb

        logging.debug("Saving node number %d." % tnn)
        self.config.node_number = tnn

        logging.debug("Save node number success.")

        Lb = self.config.node_number & 0xff
        Hb = (self.config.node_number >> 8) & 0xff

        gridmsg = self.createGridMessage(OPC_NNACK, Hb, Lb)
        self.putGridMessageInQueue(gridmsg)
        self.setup_mode = False

    #set a canid
    def handleCANID(self, message):

        if self.setup_mode:
            return

        logging.debug("Received set CANID.")
        Lb = message[2]
        Hb = message[1]
        tnn = Hb
        tnn = (tnn << 8) | Lb
        if tnn != self.config.node_number:
            logging.debug("Set CANID is for another node. My nn: %d received nn: %d" % self.config.node_number, tnn)
            return

        logging.debug("Virtual node does not have canid. Sending error")
        Lb = self.config.node_number & 0xff
        Hb = (self.config.node_number >> 8) & 0xff
        gridmsg = self.createGridMessage(OPC_CMDERR, Hb, Lb, CMDERR_INVALID_EVENT)
        self.putGridMessageInQueue(gridmsg)

    #do self enum
    def handleENUM(self, message):

        logging.debug("Virtual node does not have canid.")
        return

    #halt the node
    def handleHLT(self, message):

        if self.setup_mode:
            return

        logging.info("Stopping CBUS")
        self.cbus_stopped = True

    #resume the node
    def handleBON(self, message):

        if self.setup_mode:
            return

        logging.info("Enabling CBUS")
        self.cbus_stopped = False

    #reset the node
    def handleARST(self, message):

        if self.setup_mode:
            return

        logging.info("Enabling CBUS")
        self.cbus_stopped = False

    #boot the node
    def handleBOOT(self, message):

        if self.setup_mode:
            return

        logging.info("BOOT received. Do nothing")

