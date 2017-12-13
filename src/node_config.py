import logging
from opc import *

class NodeConfig:

    def __init__(self, config, logger):
        logging.debug("Initiate config class")
        self.manufacturer_id = b'\x00'
        self.minor_code_version = 0
        self.major_code_version = 0
        self.module_id = b'\x00'
        self.number_of_events = 0
        self.event_variables_per_event = 0
        self.number_of_node_variables = 0
        self.consumer = False
        self.producer = True
        self.mode = FLIM
        self.name = "7digits" # this has to be seven digits

    #getters and setters

    @property
    def manufacturer_id(self):
        return self.__manufacturer_id

    @manufacturer_id.setter
    def manufacturer_id(self,val):
        self.__manufacturer_id = val

    @property
    def minor_code_version(self):
        return self.__minor_code_version

    @minor_code_version.setter
    def minor_code_version(self,val):
        self.__minor_code_version = val

    @property
    def major_code_version(self):
        return self.__major_code_version

    @major_code_version.setter
    def major_code_version(self,val):
        self.__major_code_version = val

    @property
    def module_id(self):
        return self.__module_id

    @module_id.setter
    def module_id(self,val):
        self.__module_id = val

    @property
    def number_of_events(self):
        return self.__number_of_events

    @number_of_events.setter
    def number_of_events(self,val):
        self.__number_of_events = val

    @property
    def event_variables_per_event(self):
        return self.__event_variables_per_event

    @event_variables_per_event.setter
    def event_variables_per_event(self,val):
        self.__event_variables_per_event = val

    @property
    def number_of_node_variables(self):
        return self.__number_of_node_variables

    @number_of_node_variables.setter
    def number_of_node_variables(self,val):
        self.__number_of_node_variables = val

    @property
    def consumer(self):
        return self.__consumer

    @consumer.setter
    def consumer(self,val):
        self.__consumer = val

    @property
    def producer(self):
        return self.__producer

    @producer.setter
    def producer(self,val):
        self.__producer = val

    @property
    def mode(self):
        return self.__mode

    @mode.setter
    def mode(self,val):
        if (val in [SLIM, FLIM]):
            self.__mode = val
        else:
            self.__mode = FLIM

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self,val):
        if (len(val) > 7):
            self.__name = val[:7]
        else:
            self.__mode = val