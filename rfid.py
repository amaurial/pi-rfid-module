import sys
import os
import logging
import time
import signal
import rfid_server
import can_grid_client
import yaml
import queue
from rfid_utils import *

# load config
default_port = 7777

config_file = open ('config.yaml', 'r+')
config = yaml.load(config_file)
#print(yaml.dump(config))

# set the logger
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


running=True
global rfidcode

rfidcode = queue.Queue()

def receive_signal(signum,stack):
    logging.debug('Signal received. Stopping.')
    global running

    running = False

signal.signal(signal.SIGINT,receive_signal)
signal.signal(signal.SIGTERM,receive_signal)

logging.info('Starting RFID Server')

#create the tcp server. can be more than one. each server can handle several clients
try:
    service_port = config['config']['service_port']
except KeyError:
    service_port = default_port

if is_integer(service_port) != True :
    service_port = default_port

tcpServer = rfid_server.RfidServer(host = "0.0.0.0" ,port = service_port, rfid_queue = rfidcode, config = config)

# start grid client
gridClient = can_grid_client.CanGridClient(host = config["config"]["cangrid_host"],
                                           port = config["config"]["cangrid_port"],
                                           rfid_queue = rfidcode,
                                           config = config)

# start the tcp server
tcpServer.start()

# start grid client
gridClient.start()

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
