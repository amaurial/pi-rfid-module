import logging
import queue
import threading
import signal


class Facility:
    def __init__(self, config):
        self.rootLogger = logging.getLogger()
        self.config = config
        self.running = True
        self.rfid_queue = queue.Queue()
        self.in_rfid_queue_condition = threading.Condition()
        self.incoming_cbus_queue = queue.Queue()
        self.in_cbus_queue_condition = threading.Condition()
        self.outgoing_cbus_queue = queue.Queue()
        self.out_cbus_queue_condition = threading.Condition()

    def start_logging(self):
        #logging.basicConfig(filename="rfid.log", filemode="w",level=logging.DEBUG, format='%(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s')
        logFormater = logging.Formatter("%(levelname)s - %(asctime)s - %(filename)s - %(funcName)s - %(message)s")


        if (self.rootLogger.hasHandlers()):
            self.rootLogger.handlers.clear()

        level = self.config.config_dictionary['node_config']['log_level']

        if level not in ['INFO', 'WARNING', 'DEBUG', 'CRITICAL', 'ERROR']:
            loglevel = logging.DEBUG
        else:
            loglevel = logging.getLevelName(level)

        self.rootLogger.setLevel(loglevel)

        logname = self.config.config_dictionary['node_config']['log_file']
        fileHandler = logging.FileHandler(logname)
        fileHandler.setFormatter(logFormater)
        self.rootLogger.addHandler(fileHandler)

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormater)
        self.rootLogger.addHandler(consoleHandler)


    # signal handling function
    def receive_signal(self, signum, stack):
        if signum == signal.SIGBUS:
            logging.debug("Received SIGBUS")
            return
        logging.debug('Signal received. Stopping.')
        self.running = False

    def set_signals(self):
        signal.signal(signal.SIGINT, self.receive_signal)
        signal.signal(signal.SIGTERM, self.receive_signal)