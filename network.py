#importing modules
import socket
import pickle

#main class
class Network:
    #init self . 
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #serverIP and port Should match the server
        self.server = "192.168.1.12"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()


    def getP(self):
        return self.p

    def connect(self):
        try:
            #allowing the client to connect to the server 
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

