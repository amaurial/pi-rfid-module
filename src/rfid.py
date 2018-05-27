# this is the main file that starts all threads
# the most important is that it instantiates the cbus node
# each node extends the cbus_node

import os
import signal
import time
from facilities import *
from node_config import *
import facilities

import rfid_server
from rfid_utils import *
import can_grid_client
from rfid_node import RfidNode

# load config
default_port = 7777

config = NodeConfig('config.yaml')
facility = Facility(config)
facility.start_logging()

# signal handling function
def receive_signal(signum, stack):
    if signum == signal.SIGBUS:
        logging.debug("Received SIGBUS")
        return
    logging.debug('Signal received. Stopping.')
    global running
    running = False

signal.signal(signal.SIGINT, receive_signal)
signal.signal(signal.SIGTERM, receive_signal)

#create the tcp server. can be more than one. each server can handle several clients
try:
    service_port = config.config_dictionary['node_config']['service_port']
except KeyError:
    service_port = default_port

if is_integer(service_port) != True :
    service_port = default_port

# start the server on all ips
# receives the rfid from esps and put in the cangrid
# the communication among the threads are made through queues
# the esp messages are in rfid_queue
tcpServer = rfid_server.RfidServer(host ="0.0.0.0",
                                   port = service_port,
                                   rfid_queue = rfid_queue,
                                   in_rfid_queue_condition = facilities.in_rfid_queue_condition,
                                   config = config)

# start grid client
# this is the cbus. all config messages comes through here
# all rfid messages goes through here
# cbus_in_queue has the incoming can messages
# outgoing_cbus_queue are the outgoing messages
# it populates incoming_cbus_queue
# it consumes outgoing_cbus_queue
gridClient = can_grid_client.CanGridClient(host = config.config_dictionary["node_config"]["cangrid_host"],
                                           port = config.config_dictionary["node_config"]["cangrid_port"],
                                           incoming_cbus_queue = facilities.incoming_cbus_queue,
                                           in_cbus_queue_condition = facilities.in_cbus_queue_condition,
                                           outgoing_cbus_queue = facilities.outgoing_cbus_queue,
                                           out_cbus_queue_condition = facilities.out_cbus_queue_condition,
                                           config = config)

# cbus_in_queue has the incoming can messages
# outgoing_cbus_queue are the outgoing messages
# the module consume rfid_queue and put in outgoing_cbus_queue
# the module extends the CBUSNode and consumes incoming_cbus_queue
# and put the response in outgoing_cbus_queue
rfidNode = RfidNode(rfid_queue = rfid_queue,
                    incoming_cbus_queue = facilities.incoming_cbus_queue,
                    in_cbus_queue_condition = facilities.in_cbus_queue_condition,
                    outgoing_cbus_queue = facilities.outgoing_cbus_queue,
                    out_cbus_queue_condition = facilities.out_cbus_queue_condition,
                    in_rfid_queue_condition = facilities.in_rfid_queue_condition,
                    config = config)

# node setup function to be triggered by signal
# the signal is triggered by kill command in the command line
# kill -7
def doNodeSetup(signum, stack):
    if signum == signal.SIGBUS:
        #send RQNN
        if rfidNode.setup_mode:
            logging.debug("Quitting setup mode")
            rfidNode.setup_mode = False
        else:
            rfidNode.sendRQNN()

#set node setup signal
signal.signal(signal.SIGBUS, doNodeSetup)

# initialise the main threads
logging.info('Starting RFID Server')
# start the tcp server
tcpServer.start()

# start grid client
logging.info('Starting grid client')
gridClient.start()

#start the main node logic
logging.info('Starting node logic')
rfidNode.start()

# loop until the threads dies
while running:
    #do nothing
    time.sleep(3)

logging.info("Stoping components")
#stop all the components
tcpServer.stop()
gridClient.stop()
rfidNode.stop()

logging.info("Finishing %i" %os.getpid())
logging.shutdown()
#for some reason the tcp server is not dying gracefully. so we kill it
os.kill(os.getpid(), 9)
#sys.exit()
