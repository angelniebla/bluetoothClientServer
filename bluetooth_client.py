'''
Bluetooth socket support

Copyright 2018  Gunnar Bowman, Emily Boyes, Trip Calihan, Simon D. Levy, Shepherd Sims

MIT License
'''

import os

import bluetooth as bt

class BluetoothClient(object):
    '''
    Provides an abstract class for serving sockets over Bluetooth.  You call the constructor and the start()
    method.  You must implement the method handleMessage(self, message) to handle messages from the client.
    '''

    def __init__(self):
        '''
        Constructor
        '''

        # Arbitrary service UUID to advertise
        print("INIT CLIENT")
        
        #self.uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"

        #self.client_sock = None

    def start(self, client_info):
        
        print("START CLIENT")

        # Make device visible
        os.system("hciconfig hci0 piscan")

        # Create a new server socket using RFCOMM protocol
        client_socket = bt.BluetoothSocket(bt.RFCOMM)
        
        #client_socket.settimeout(100.0)
        
        client_addr = "D4:3B:04:76:E7:55"
        
        try:
        
            client_socket.connect((client_addr, 1))
            
        except bt.btcommon.BluetoothError:
            return None
        


        # Bind to any port
        #server_sock.bind(("", bt.PORT_ANY))

        # Start listening
        #server_sock.listen(1)

        # Get the port the server socket is listening
        #port = server_sock.getsockname()[1]

        # Start advertising the service
        #bt.advertise_service(server_sock, "RaspiBtSrv",
                           #service_id=self.uuid,
                           #service_classes=[self.uuid, bt.SERIAL_PORT_CLASS],
                           #profiles=[bt.SERIAL_PORT_PROFILE])

        # Outer loop: listen for connections from client
        while True:

            #print("Waiting for connection on RFCOMM channel")

            try:

                # This will block until we get a new connection
                #self.client_sock, client_info = server_sock.accept()
                #print("Connected to " +  str(client_info))

                # Track strings delimited by '.'
                #s = ''

                while True:
                    
                    #message = raw_input('Send:')
                    #if not message : break
                    #self.send(client_info)
                    client_socket.send((client_info+'#').encode('utf-8'))
                    #s = client_socket.recv(1024).decode('utf-8')
                    #print('Received', s)
                    #self.handleMessage(s)
                    #self.handleRedirect()
                    client_socket.close()
                    print("Client going down")
                    
                    return client_addr
                
                break

            except IOError:
                pass

            except KeyboardInterrupt:

                if client_socket is not None:
                    client_socket.close()

                #server_sock.close()

                print("Client going down")
                break

    def send(self, message):
        '''
        Appends a period to your message and sends the message back to the client.
        '''
        print("SENDING " + message)
        self.client_sock.send((message+'#').encode('utf-8'))
        

