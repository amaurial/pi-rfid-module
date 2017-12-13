import logging
import os
import signal
import time
import yaml
import queue
from node_config import *

import rfid_server
from rfid_utils import *
from src import can_grid_client

# load config
default_port = 7777

config_file = open ('config.yaml', 'r+')
config = yaml.load(config_file)
#print(yaml.dump(config))

###### set the logger #######

#logging.basicConfig(filename="rfid.log", filemode="w",level=logging.DEBUG, format='%(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s')
logFormater = logging.Formatter("%(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s")
rootLogger = logging.getLogger()
level = config['config']['log_level']

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
global rfidcode
rfidcode = queue.Queue()

# signal handling function
def receive_signal(signum,stack):
    logging.debug('Signal received. Stopping.')
    global running

    running = False

signal.signal(signal.SIGINT,receive_signal)
signal.signal(signal.SIGTERM,receive_signal)

# add node configuration

node_config = NodeConfig()
node_config.consumer = False
node_config.event_variables_per_event = 0
node_config.major_code_version = 0
node_config.minor_code_version = 1
node_config.manufacturer_id = 55
node_config.mode = FLIM
node_config.producer = True
node_config.number_of_node_variables = 0
node_config.number_of_events = 0
node_config.module_id = 72 #arbitrary?
node_config.name = "PIRFID"

# initialise the main threads
logging.info('Starting RFID Server')

#create the tcp server. can be more than one. each server can handle several clients
try:
    service_port = config['config']['service_port']
except KeyError:
    service_port = default_port

if is_integer(service_port) != True :
    service_port = default_port

#start the server on all ips
tcpServer = rfid_server.RfidServer(host ="0.0.0.0",
                                   port = service_port,
                                   rfid_queue = rfidcode,
                                   config = config,
                                   node_config = config)

# start grid client
gridClient = can_grid_client.CanGridClient(host = config["config"]["cangrid_host"],
                                           port = config["config"]["cangrid_port"],
                                           rfid_queue = rfidcode,
                                           config = config,
                                           node_config = node_config)

# start the tcp server
tcpServer.start()

# start grid client
gridClient.start()

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
