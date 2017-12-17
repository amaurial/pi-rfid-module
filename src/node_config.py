import logging
from opc import *
import yaml
import sys
from shutil import copyfile

#cbus memory data
class NodeConfig:

    def __init__(self, config_file):
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
        self.cbusconfig = "cbus_config"
        self.node_number = 1234
        self.config_dictionary = {}
        self.config_file_name = config_file
        self.load_config()

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

    #getters and setters
    #def getFlags(self):

    @property
    def config_dictionary(self):
        return self.__config_dictionary

    @config_dictionary.setter
    def config_dictionary(self,val):
        self.__config_dictionary = val

    @property
    def manufacturer_id(self):
        return self.config_dictionary[self.cbusconfig]["manufacturer_id"]

    @manufacturer_id.setter
    def manufacturer_id(self,val):
        self.config_dictionary[self.cbusconfig]["manufacturer_id"] = val

    @property
    def minor_code_version(self):
        return self.config_dictionary[self.cbusconfig]["minor_code_version"]

    @minor_code_version.setter
    def minor_code_version(self,val):
        self.config_dictionary[self.cbusconfig]["minor_code_version"] = val

    @property
    def major_code_version(self):
        return self.config_dictionary[self.cbusconfig]["major_code_version"]

    @major_code_version.setter
    def major_code_version(self,val):
        self.config_dictionary[self.cbusconfig]["major_code_version"] = val

    @property
    def module_id(self):
        return self.config_dictionary[self.cbusconfig]["module_id"]

    @module_id.setter
    def module_id(self,val):
        self.config_dictionary[self.cbusconfig]["module_id"] = val

    @property
    def number_of_events(self):
        return self.config_dictionary[self.cbusconfig]["number_events"]

    @number_of_events.setter
    def number_of_events(self,val):
        self.config_dictionary[self.cbusconfig]["number_events"] = val

    @property
    def event_variables_per_event(self):
        return self.config_dictionary[self.cbusconfig]["variables_per_event"]

    @event_variables_per_event.setter
    def event_variables_per_event(self,val):
        self.config_dictionary[self.cbusconfig]["variables_per_event"] = val

    @property
    def number_of_node_variables(self):
        return self.config_dictionary[self.cbusconfig]["number_of_node_variables"]

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
    def name(self,val):
        if (len(val) > 7):
            self.config_dictionary[self.cbusconfig]["name"] = val[:7]
        else:
            self.config_dictionary[self.cbusconfig]["name"] = val

    @property
    def events(self):
        return self.config_dictionary[self.cbusconfig]["events"]

    @producer.setter
    def events(self,val):
        self.config_dictionary[self.cbusconfig]["events"] = val

    @property
    def canid(self):
        return self.config_dictionary[self.cbusconfig]["canid"]

    @canid.setter
    def canid(self,val):
        self.config_dictionary[self.cbusconfig]["canid"] = val

    @property
    def node_number(self):
        return self.config_dictionary[self.cbusconfig]["node_number"]

    @node_number.setter
    def node_number(self,val):
        self.config_dictionary[self.cbusconfig]["node_number"] = val