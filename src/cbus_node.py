from opc import *
import queue
import threading
import logging

class CBUSNode(threading.Thread):

    def __init__(self, incoming_cbus_queue, outgoing_cbus_queue, config):
        self.config = config
        self.cbus_out_queue = outgoing_cbus_queue
        self.cbus_in_queue = incoming_cbus_queue
        self.running = True

    def run(self):

        while self.running:
            #consume cbus messages
            self.consumeCBUSQueue()

    def stop(self):
        self.running = False


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

    def consumeCBUSQueue(self):
        data = self.parseCBUSMessage(message)
        if (len(data) == 0):
            logging.debug("Empty data. Not processing")
            continue

        if (data[0] in [OPC_QNN, OPC_RQMN, OPC_RQNP, OPC_SNN, OPC_ENUM, OPC_HLT,
                    OPC_BON, OPC_BOOT, OPC_ARST, OPC_CANID, OPC_NVSET, OPC_RQNPN,
                    OPC_NVRD]):
                    self.handleCBUSMessages(data)
        else:
            self.nodeLogic(data)

    #function to be override
    def nodeLogic(self,message):
        pass

    #receive all the can message
    def handleCBUSMessages(self, message):
        logging.debug("Handling CBUS message: %s" % message)

        opc = message[0]
        Lb = self.config.node_number & 0xff;
        Hb = (self.config.node_number >> 8) & 0xff;

        if (opc == OPC_QNN):
            if (setup_mode): return

            logger->debug("[canHandler] Sending response for QNN.");
            sendframe[0] = OPC_PNN;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            sendframe[3] = self.node_config.manufacturer_id
            sendframe[4] = self.node_config.module_id
            sendframe[5] = self.node_config.getFlags()
            put_to_out_queue(sendframe, 6, CLIENT_TYPE::CBUS);

    def parseCBUSMessage(self, message):

        # The GridConnect protocol encodes messages as an ASCII string of up to 24 characters of the form:
        # :ShhhhNd0d1d2d3d4d5d6d7;
        # The S indicates a standard CAN frame
        # :XhhhhhhhhNd0d1d2d3d4d5d6d7;
        # The X indicates an extended CAN frame hhhh is the two byte header N or R indicates a normal
        # or remote frame, in position 6 or 10 d0 - d7 are the (up to) 8 data bytes

        cdata = []
        for i in range(8):
            cdata[i] = 0

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
        for i in len(datahex):
            cdata[i] = datahex[i]

        return cdata


void canHandler::handleCBUSEvents(frameCAN canframe){

    char sendframe[CAN_MSG_SIZE];
    memset(sendframe,0,CAN_MSG_SIZE);
    byte Hb,Lb;
    int tnn;
    SCRIPT_ACTIONS status = NONE;
    struct can_frame frame = canframe.getFrame();
    print_frame(&frame,"[canHandler] Handling CBUS event");

    switch (frame.data[0]){
    case OPC_QNN:
    {


        break;
    }
    case OPC_RQNP:
    {
        if (!setup_mode) return;

        Lb = frame.data[2];
        Hb = frame.data[1];
        tnn = Hb;
        tnn = (tnn << 8) | Lb;

        logger->debug("[canHandler] Sending response for RQNP.");
        sendframe[0] = OPC_PARAMS;
        sendframe[1] = MANU_MERG;
        sendframe[2] = MSOFT_MIN_VERSION;
        sendframe[3] = MID;
        sendframe[4] = 0;
        sendframe[5] = 0;
        sendframe[6] = config->getNumberOfNVs();//TODO
        sendframe[7] = MSOFT_VERSION;
        put_to_out_queue(sendframe, 8, CLIENT_TYPE::CBUS);

        break;
    }
    case OPC_RQEVN:
    {
         Lb = frame.data[2];
         Hb = frame.data[1];
         tnn = Hb;
         tnn = (tnn << 8) | Lb;

         if (tnn != node_number){
             logger->debug("[canHandler] RQEVN is for another node. My nn: %d received nn: %d", node_number,tnn);
             return;
         }
        Lb = node_number & 0xff;
        Hb = (node_number >> 8) & 0xff;
        logger->debug("[canHandler] Sending response for RQEVN.");
        sendframe[0] = OPC_NUMEV;
        sendframe[1] = Hb;
        sendframe[2] = Lb;
        sendframe[3] = 0;
        put_to_out_queue(sendframe, 4, CLIENT_TYPE::CBUS);

        break;
    }
   case OPC_RQMN:
    {
        if (!setup_mode) return;
        logger->debug("[canHandler] Sending response for NAME.");
        sendframe[0] = OPC_NAME;
        sendframe[1] = 'P';
        sendframe[2] = 'i';
        sendframe[3] = 'W';
        sendframe[4] = 'i';
        sendframe[5] = ' ';
        sendframe[6] = ' ';
        sendframe[7] = ' ';
        put_to_out_queue(sendframe, 8, CLIENT_TYPE::CBUS);
        break;
    }
    case OPC_RQNPN:
    {
        Lb = frame.data[2];
        Hb = frame.data[1];
        tnn = Hb;
        tnn = (tnn << 8) | Lb;
        byte p;
        if (tnn != node_number){
            logger->debug("[canHandler] RQNPN is for another node. My nn: %d received nn: %d", node_number,tnn);
            return;
        }
        if (frame.data[3] > NODE_PARAMS_SIZE) {
            //index invalid
            sendframe[0] = OPC_CMDERR;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            sendframe[3] = CMDERR_INV_PARAM_IDX;
            put_to_out_queue(sendframe, 4, CLIENT_TYPE::CBUS);
            return;
        }
        p = config->getNodeParameter(frame.data[3]);
        if (frame.data[3] == 0){
            p = NODE_PARAMS_SIZE;
        }
        sendframe[0] = OPC_PARAN;
        sendframe[1] = Hb;
        sendframe[2] = Lb;
        sendframe[3] = frame.data[3];
        sendframe[4] = p;
        put_to_out_queue(sendframe, 5, CLIENT_TYPE::CBUS);
        break;
    }
    case OPC_NVRD:
    {
        Lb = frame.data[2];
        Hb = frame.data[1];
        tnn = Hb;
        tnn = (tnn << 8) | Lb;
        if (tnn != node_number){
            logger->debug("[canHandler] NVRD is for another node. My nn: %d received nn: %d", node_number,tnn);
            return;
        }
        if (frame.data[3] > config->getNumberOfNVs() || frame.data[3] == 0) {
            //index invalid
            sendframe[0] = OPC_CMDERR;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            sendframe[3] = CMDERR_INV_PARAM_IDX;
            put_to_out_queue(sendframe, 4, CLIENT_TYPE::CBUS);
            logger->debug("[canHandler] NVRD Invalid index %d", frame.data[3]);
            return;
        }
        sendframe[0] = OPC_NVANS;
        sendframe[1] = Hb;
        sendframe[2] = Lb;
        sendframe[3] = frame.data[3];
        sendframe[4] = config->getNV(frame.data[3]);
        put_to_out_queue(sendframe, 5, CLIENT_TYPE::CBUS);
        logger->debug("[canHandler] NVRD processed. Sent NVANS");
        break;
    }
    case OPC_NVSET:
    {
        Lb = frame.data[2];
        Hb = frame.data[1];
        tnn = Hb;
        tnn = (tnn << 8) | Lb;
        if (tnn != node_number){
            logger->debug("[canHandler] NVSET is for another node. My nn: %d received nn: %d", node_number,tnn);
            return;
        }
        if (frame.data[3] > config->getNumberOfNVs() || frame.data[3] == 0) {
            //index invalid
            sendframe[0] = OPC_CMDERR;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            sendframe[3] = CMDERR_INV_PARAM_IDX;
            put_to_out_queue(sendframe,4 , CLIENT_TYPE::CBUS);
            logger->debug("[canHandler] NVSET Invalid index %d", frame.data[3]);
            return;
        }

        //1 error, 2 reconfigure , 3 restart the service
        int st = config->setNV(frame.data[3],frame.data[4]);
        if (st == 1){
            sendframe[0] = OPC_CMDERR;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            sendframe[3] = CMDERR_INV_PARAM_IDX;
            put_to_out_queue(sendframe, 4, CLIENT_TYPE::CBUS);
            logger->debug("[canHandler] NVSET failed. Sent Err");
            status = NONE;
        }
        else{
            sendframe[0] = OPC_WRACK;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            put_to_out_queue(sendframe, 3, CLIENT_TYPE::CBUS);
            logger->debug("[canHandler] NVSET ok. Sent wrack");
        }

        if (st == 2 || st == 3){
            if (st == 2) status = CONFIGURE;
            if (st == 3) status = RESTART;
            restart_module(status);
        }

        break;
    }
    case OPC_SNN:
    {

        if (!setup_mode) return;

        Lb = frame.data[2];
        Hb = frame.data[1];
        tnn = Hb;
        tnn = (tnn << 8) | Lb;

        logger->debug("[canHandler] Saving node number %d.",tnn);
        if (config->setNodeNumber(tnn)){
            logger->debug("[canHandler] Save node number success.");
            node_number = tnn;
            Lb = node_number & 0xff;
            Hb = (node_number >> 8) & 0xff;
            sendframe[0] = OPC_NNACK;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            put_to_out_queue(sendframe, 3, CLIENT_TYPE::CBUS);
        }
        else{
            logger->error("[canHandler] Save node number failed. Maintaining the old one");
            Lb = node_number & 0xff;
            Hb = (node_number >> 8) & 0xff;
            sendframe[0] = OPC_CMDERR;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            sendframe[3] = 5;
            put_to_out_queue(sendframe, 4, CLIENT_TYPE::CBUS);
        }
        setup_mode = false;
        blinking = false;
        gl.setval_gpio("0");
        yl.setval_gpio("1");
        logger->info("Node was in SLIM. Setting to FLIM");
        config->setNodeMode(1); //FLIM
        logger->info("[canHandler] Finished setup. New node number is %d" , node_number);

        break;
    }
    case OPC_CANID:
    {
        if (setup_mode) return;
        logger->debug("[canHandler] Received set CANID.");
        Lb = frame.data[2];
        Hb = frame.data[1];
        tnn = Hb;
        tnn = (tnn << 8) | Lb;
        if (tnn != node_number){
            logger->debug("[canHandler] Set CANID is for another node. My nn: %d received nn: %d", node_number,tnn);
            return;
        }
        int tcanid;
        tcanid = frame.data[3];
        if (tcanid < 1 || tcanid > 99){
            logger->debug("[canHandler] CANID [%d] out of range 1-99. Sending error.", tcanid);
            Lb = node_number & 0xff;
            Hb = (node_number >> 8) & 0xff;
            sendframe[0] = OPC_CMDERR;
            sendframe[1] = Hb;
            sendframe[2] = Lb;
            sendframe[3] = CMDERR_INVALID_EVENT;
            put_to_out_queue(sendframe, 4, CLIENT_TYPE::CBUS);
            return;
        }
        canId = tcanid;
        logger->debug("[canHandler] Saving new CANID %d",canId);
        if (!config->setCanID(canId)){
            logger->error("[canHandler] Failed to save canid %d",canId);
        }

        break;
    }
    case OPC_ASON:
    {
        Lb = frame.data[4];
        Hb = frame.data[3];
        tnn = Hb;
        tnn = (tnn << 8) | Lb;
        logger->debug("[canHandler] Received set ASON %d", tnn);
        if (tnn == config->getShutdownCode()){
            logger->debug("[canHandler] Shuting down the node.");
            restart_module(SHUTDOWN);
            return;
        }

        break;
    }
    case OPC_ENUM:
    {
        if (setup_mode) return;
        //get node number
        int nn;
        nn = frame.data[1];
        nn = (nn << 8) | frame.data[2];
        logger->debug("[canHandler] OPC_ENUM for node number %d",nn);
        if (nn == node_number){
            soft_auto_enum = true;
            doSelfEnum();
        }
        break;
    }
    case OPC_HLT:
    {
        if (setup_mode) return;
        logger->info("[canHandler] Stopping CBUS");
        cbus_stopped = true;
        break;
    }
    case OPC_BON:
    {
        if (setup_mode) return;
        logger->info("[canHandler] Enabling CBUS");
        cbus_stopped = false;
        break;
    }
    case OPC_ARST:
    {
        if (setup_mode) return;
        logger->info("[canHandler] Enabling CBUS");
        cbus_stopped = false;
        break;
    }
    case OPC_BOOT:
    {
        if (setup_mode) return;
        logger->info("[canHandler] Rebooting");
        break;
    }
