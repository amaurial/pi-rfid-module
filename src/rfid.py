import logging
import os
import signal
import time
import queue
from node_config import *

import rfid_server
from rfid_utils import *
import can_grid_client
from rfid_node import RfidNode

# load config
default_port = 7777

config = NodeConfig('config.yaml')

###### set the logger #######

#logging.basicConfig(filename="rfid.log", filemode="w",level=logging.DEBUG, format='%(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s')
logFormater = logging.Formatter("%(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s")
rootLogger = logging.getLogger()
level = config.config_dictionary['node_config']['log_level']

if level not in ['INFO', 'WARNING', 'DEBUG', 'CRITICAL', 'ERROR']:
    loglevel = logging.DEBUG
else:
    loglevel = logging.getLevelName(level)

rootLogger.setLevel(loglevel)

fileHandler = logging.FileHandler("rfid.log")
fileHandler.setFormatter(logFormater)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormater)
rootLogger.addHandler(consoleHandler)

# flag used by threads in the run loop
running=True

# the queue containing the messages from the rfid readers
global rfid_queue
rfid_queue = queue.Queue()

#populated by the grid connect
global incoming_cbus_queue
incoming_cbus_queue = queue.Queue

#consumed by the grid connect
global outgoing_cbus_queue
outgoing_cbus_queue = queue.Queue

# signal handling function
def receive_signal(signum,stack):
    logging.debug('Signal received. Stopping.')
    global running

    running = False

signal.signal(signal.SIGINT,receive_signal)
signal.signal(signal.SIGTERM,receive_signal)

# initialise the main threads
logging.info('Starting RFID Server')

#create the tcp server. can be more than one. each server can handle several clients
try:
    service_port = config.config_dictionary['node_config']['service_port']
except KeyError:
    service_port = default_port

if is_integer(service_port) != True :
    service_port = default_port

#start the server on all ips
tcpServer = rfid_server.RfidServer(host ="0.0.0.0",
                                   port = service_port,
                                   rfid_queue = rfid_queue,
                                   config = config)

# start grid client
gridClient = can_grid_client.CanGridClient(host = config.config_dictionary["node_config"]["cangrid_host"],
                                           port = config.config_dictionary["node_config"]["cangrid_port"],
                                           incoming_cbus_queue = incoming_cbus_queue,
                                           outgoing_cbus_queue = outgoing_cbus_queue,
                                           config = config)

rfidNode = RfidNode(rfid_queue = rfid_queue,
                    incoming_cbus_queue = incoming_cbus_queue,
                    outgoing_cbus_queue = outgoing_cbus_queue,
                    config = config)

# start the tcp server
tcpServer.start()

# start grid client
gridClient.start()

#start the main node logic
rfidNode.start()

# loop until the threads dies
while running:
    #do nothing
    time.sleep(3)

#stop all the components
tcpServer.stop()

logging.info("Finishing %i" %os.getpid())
logging.shutdown()
#for some reason the tcp server is not dying gracefully. so we kill it
os.kill(os.getpid(), 9)
#sys.exit()
