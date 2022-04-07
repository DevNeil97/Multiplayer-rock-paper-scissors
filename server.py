#we are going to use socket and thredding to handle incoming connctions
import socket
from _thread import *
import pickle
from game import Game

#ini port and IP 
server = "192.168.1.12"
port = 5555

#configering s to IPV4 and TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#binding the socket
try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#listing to upto qeaue of 2 cliants
s.listen(2)
print("Waiting for a connection, Server Started")

#ini
connected = set()
games = {}
idCount = 0

#using threded funtion to server. this will help to run mutiple clients along with
#while loop alowing both the fintion and while loop to run pallaral rather than while loop after the funtion after
# the while loop.
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        #try to rev data from the clinet and 
        #if unsuccsfull reset connction. 
        try:
            #decoding data along setting bite size. 
            data = conn.recv(4096).decode()
            
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    #if connction is lost closing the current game and redusing nuber of users by 1
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()



while True:
    #accenpting incoming connctins and string the in a var 
    conn, addr = s.accept()
    print("Connected to:", addr)
    
    
    idCount += 1
    p = 0
    gameId = (idCount - 1)//2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    
    start_new_thread(threaded_client, (conn, p, gameId))
