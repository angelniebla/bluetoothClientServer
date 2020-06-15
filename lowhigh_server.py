#!/usr/bin/python3
'''
Subclasses BluetoothSocket to serve messages "LOW" and "HIGH" based on values received from
client

Copyright Simon D. Levy 2018

MIT License
'''

from bluetooth_server import BluetoothServer
from bluetooth_client import BluetoothClient


class LowHighServer(BluetoothServer):

    def __init__(self):

        BluetoothServer.__init__(self)

    def handleMessage(self, message):
        print(message)

        self.send(message)
        
    def handleRedirect(self):

        BluetoothServer.send("D4:3B:04:76:E7:55")
        
    def change(self, client_info):
        print('CAMBIANDO A MODO CLIENTE')
        BluetoothClient.__init__(self)
        client_addr = BluetoothClient.start(self, client_info)
        if client_addr is None:
                return "0"
        return client_addr

if __name__ == '__main__':

    server = LowHighServer()

    server.start()
