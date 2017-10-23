
import socket
import threading
import logging
import random
import string
import select
import errno
import rfid_client_handler

class RfidServer(threading.Thread):
    def __init__(self, host, port, rfid_queue, config):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.rfid_queue = rfid_queue
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self.sock.bind((self.host, self.port))
        self.running = True
        self.clients = {}
        self.config = config

    def id_generator(self,size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    def stop(self):
        self.running = False
        logging.info("Tcp server stopping")
        self.sock.close()

    def run(self):
        logging.info('Starting tcp server on %s port = %d ' % (self.host, self.port))
        self.sock.listen(5)
        while self.running:
            client, address = self.sock.accept()
            client.settimeout(60)
            logging.debug("New tcp client")
            id = self.id_generator()
            clientHandler = rfid_client_handler.RfidClient(client, address, self.rfid_queue, self, id, self.config)
            self.clients[id]=clientHandler
            clientHandler.start()

        #close all clients
        logging.debug("Tcp server closing clients")
        for k, c in self.clients.items():
            c.stop()
        logging.debug("Tcp server closing main socket")
        self.sock.close()

    def removeClient(self,id):
        logging.debug("Removing ED client %s" % id)
        del self.clients[id]
        logging.debug("Sessions active %s" % self.clients)
    # def listenToClient(self, client, address):
    #     logging.debug("serving the tcp client")
    #     size = 1024
    #     while self.running:
    #         try:
    #             ready = select.select([client],[],[],1)
    #             if ready[0]:
    #                 data = client.recv(size)
    #                 if data:
    #                     response = data
    #                     client.send(response)
    #                 else:
    #                     raise Exception('Client disconnected')
    #         except:
    #             logging.debug("exception")
    #             self.clients.remove(client)
    #             client.close()
    #             raise
    #             return False
    #     logging.debug("Tcp server closing client socket")
    #     client.close()

    def getName(self):
        return self.host + self.port