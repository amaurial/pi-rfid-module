import logging
from opc import *
import yaml
import sys
from shutil import copyfile
import binascii

#cbus memory data
class NodeConfig:

    def __init__(self, config_file_name):
        logging.debug("Initiate config class")
        # self.manufacturer_id = b'\x00'
        # self.minor_code_version = 0
        # self.major_code_version = 0
        # self.module_id = b'\x00'
        # self.number_of_events = 0
        # self.event_variables_per_event = 0
        # self.number_of_node_variables = 0
        # self.consumer = False
        # self.producer = True
        # self.mode = FLIM
        # self.name = "7digits" # this has to be seven digits
        # self.events = {}
        # self.node_variables = b"\x00"
        self.config_file_name = config_file_name
        self.load_config()
        self.cbusconfig = "cbus_config"

    def load_config(self):
        try:
            config_file = open (self.config_file_name, 'r+')
            self.__config_dictionary = yaml.load(config_file)
            config_file.close()
        except:
            logging.error(sys.exc_info()[0])
            raise

    def save_config(self):
        try:
            config_file = open ('temp.yaml', 'w+')
            yaml.dump(self.config_dictionary, config_file,  default_flow_style=False)
            config_file.close()
            copyfile('temp.yaml' , self.config_file_name)
        except:
            logging.error(sys.exc_info()[0])
            raise

    def getFlags(self):
        flag = 0x04 #always FLIM and not support bootloading
        if self.consumer:
            flag = flag | 0x01
        if self.producer:
            flag = flag | 0x02

        logging.debug("Config flag is %d" % flag)

        return flag


    def convertStringToArrayInt(self,variables):
        #the variables format is "0xaa,0xbb,123"
        #the function returns and array of integers

        if len(variables) == 0:
            return None

        list = variables.split(',')
        r = []
        for v in list:
            r.append(int(v, 0))
        return r

    def convertArrayIntToString(self,variables):
        #the variables is an array of int

        if len(variables) == 0:
            return ''
        s=''
        for v in variables:
           s = s + "0x%02X," % v

        return s[:len(s)-1]

    #getters and setters
    @property
    def config_dictionary(self):
        return self.__config_dictionary

    @config_dictionary.setter
    def config_dictionary(self,val):
        self.__config_dictionary = val

    @property
    def manufacturer_id(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["manufacturer_id"])
            return val
        except:
            return 0

    @manufacturer_id.setter
    def manufacturer_id(self,val):
        self.config_dictionary[self.cbusconfig]["manufacturer_id"] = val

    @property
    def minor_code_version(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["minor_code_version"])
            return val
        except:
            return 0

    @minor_code_version.setter
    def minor_code_version(self,val):
        self.config_dictionary[self.cbusconfig]["minor_code_version"] = val

    @property
    def major_code_version(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["major_code_version"])
            return val
        except:
            return 0

    @major_code_version.setter
    def major_code_version(self,val):
        self.config_dictionary[self.cbusconfig]["major_code_version"] = val

    @property
    def module_id(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["module_id"])
            return val
        except:
            return 0

    @module_id.setter
    def module_id(self,val):
        self.config_dictionary[self.cbusconfig]["module_id"] = val

    @property
    def number_of_events(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["number_events"])
            return val
        except:
            return 0

    @number_of_events.setter
    def number_of_events(self,val):
        self.config_dictionary[self.cbusconfig]["number_events"] = val

    @property
    def event_variables_per_event(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["variables_per_event"])
            return val
        except:
            return 0

    @event_variables_per_event.setter
    def event_variables_per_event(self,val):
        self.config_dictionary[self.cbusconfig]["variables_per_event"] = val

    @property
    def number_of_node_variables(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["number_of_node_variables"])
            return val
        except:
            return 0

    @number_of_node_variables.setter
    def number_of_node_variables(self,val):
        self.config_dictionary[self.cbusconfig]["number_of_node_variables"] = val

    @property
    def consumer(self):
        return self.config_dictionary[self.cbusconfig]["consumer"]

    @consumer.setter
    def consumer(self,val):
        self.config_dictionary[self.cbusconfig]["consumer"] = val

    @property
    def producer(self):
        return self.config_dictionary[self.cbusconfig]["producer"]

    @producer.setter
    def producer(self,val):
        self.config_dictionary[self.cbusconfig]["producer"] = val

    @property
    def mode(self):
        return self.config_dictionary[self.cbusconfig]["mode"]

    @mode.setter
    def mode(self,val):
        if (val in [SLIM, FLIM]):
            self.config_dictionary[self.cbusconfig]["mode"] = val
        else:
            self.config_dictionary[self.cbusconfig]["mode"] = FLIM

    @property
    def name(self):
        return self.config_dictionary[self.cbusconfig]["name"]

    @name.setter
    def name(self, val):
        if (len(val) > 7):
            self.config_dictionary[self.cbusconfig]["name"] = val[:7]
        else:
            self.config_dictionary[self.cbusconfig]["name"] = val

    @property
    def events(self):
        return self.__config_dictionary[self.cbusconfig]["events"]

    @events.setter
    def events(self, val):
        self.config_dictionary[self.cbusconfig]["events"] = val

    @property
    def canid(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["canid"])
            return val
        except:
            return 0

    @canid.setter
    def canid(self,val):
        self.config_dictionary[self.cbusconfig]["canid"] = val

    @property
    def node_variables(self):
        #return binascii.hexlify(self.config_dictionary[self.cbusconfig]["node_variables"].encode('ascii'))
        return self.convertStringToArrayInt(self.config_dictionary[self.cbusconfig]["node_variables"])

    @node_variables.setter
    def node_variables(self, val):
        #val is an array of int
        #this convert it to hexa

        self.config_dictionary[self.cbusconfig]["node_variables"] = self.convertArrayIntToString(val)

    @property
    def node_number(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["node_number"])
            return val
        except:
            return 0

    @node_number.setter
    def node_number(self, val):
        self.config_dictionary[self.cbusconfig]["node_number"] = val

    @property
    def number_of_parameters(self):
        try:
            val = int(self.config_dictionary[self.cbusconfig]["number_of_parameters"])
            return val
        except:
            return 0

    @number_of_parameters.setter
    def number_of_parameters(self, val):
        self.config_dictionary[self.cbusconfig]["number_of_parameters"] = val
