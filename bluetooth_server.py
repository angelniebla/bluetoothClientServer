'''
Bluetooth socket support

Copyright 2018  Gunnar Bowman, Emily Boyes, Trip Calihan, Simon D. Levy, Shepherd Sims

MIT License
'''

import os

import bluetooth as bt
import time

class BluetoothServer(object):
    '''
    Provides an abstract class for serving sockets over Bluetooth.  You call the constructor and the start()
    method.  You must implement the method handleMessage(self, message) to handle messages from the client.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        print("INIT SERVER")
        
        # Arbitrary service UUID to advertise
        self.uuid = "7be1fcb3-5776-42fb-91fd-2ee7b5bbb86d"

        self.client_sock = None
        
        self.data={"94:87:E0:AD:E9:5C":"111"}

    def start(self):
        '''
        Serves a socket on the default port, listening for clients.  Upon client connection, runs a loop to 
        that receives period-delimited messages from the client and calls the sub-class's 
        handleMessage(self, message) method.   Sub-class can call send(self, message) to send a 
        message back to the client.   Begins listening again after client disconnects.
        '''

        # Make device visible
        os.system("hciconfig hci0 piscan")

        # Create a new server socket using RFCOMM protocol
        server_sock = bt.BluetoothSocket(bt.RFCOMM)

        # Bind to any port
        server_sock.bind(("", bt.PORT_ANY))

        # Start listening
        server_sock.listen(1)
        
        #server_sock.settimeout(100.0)

        # Get the port the server socket is listening
        port = server_sock.getsockname()[1]

        # Start advertising the service
        bt.advertise_service(server_sock, "RaspiBtSrv",
                           service_id=self.uuid,
                           service_classes=[self.uuid, bt.SERIAL_PORT_CLASS],
                           profiles=[bt.SERIAL_PORT_PROFILE])

        # Outer loop: listen for connections from client
        
        #timeout = time.time() + 20   # [seconds]

        
        while True:

            print("Waiting for connection on RFCOMM channel %d" % port)
            
            #if time.time() > timeout:
                #if self.client_sock is not None:
                    #self.client_sock.close()

                #server_sock.close()

                #print("Server going down")
                #self.change()
                #break
                
            
            #print(time.time())
            

            try:

                # This will block until we get a new connection
                self.client_sock, client_info = server_sock.accept()
                print("Accepted connection from " +  str(client_info))

                # Track strings delimited by '.'
                s = ''

                while True:
                    
                    #if time.time() > timeout:
                        #break
            
                    #print(time.time())

                    c = self.client_sock.recv(1).decode('utf-8')
                    
                    

                    if c == '.' and len(s) > 0:
                        
                        client_addr = self.change(str(client_info[0]))
                        self.handleMessage(client_addr)
                        
                        s = ''
                        if self.client_sock is not None:
                            self.client_sock.close()

                        #server_sock.close()

                        print("Server going down")
                        #break
                        
                        
                    
                    elif c == '#' and len(s) > 0:
                        #self.handleMessage(s)
                        print("message: "+s)
                        self.data[s]="111"
                        s = ''
                        if self.client_sock is not None:
                            self.client_sock.close()

                        #server_sock.close()

                        #print("Server going down")
                        #self.change()
                        #break
                    elif c == '$' and len(s) > 0:
                        #test = dict(self.data)
                        print("LIST" + list(self.data))
                        for key in list(self.data):
                            if key == str(client_info[0]):
                                self.handleMessage(self.data[key])
                                self.data.pop(key)
                        s = ''
                        if self.client_sock is not None:
                            self.client_sock.close()

                        #server_sock.close()

                        #print("Server going down")
                        #self.change()
                        #break
                    else:
                        s += c

            except IOError:
                pass
            

            except KeyboardInterrupt:

                if self.client_sock is not None:
                    self.client_sock.close()

                server_sock.close()

                print("Server going down")
                break

    def send(self, message):
        '''
        Appends a period to your message and sends the message back to the client.
        '''
        self.client_sock.send((message+'.').encode('utf-8'))
        #print(message)
