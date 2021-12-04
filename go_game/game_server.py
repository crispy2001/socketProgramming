#!/usr/bin/python3
import socket, os, time, _thread, subprocess, pygame
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 9999

# create chessboard array
map=[]
for i in range(24):
    map.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

playerOne = 1
playerTwo = 2
win = 0

playerConn = list()
playerAddr = list()

# check is win or not
def check_winner(i, j):
    global win, map
    k = map[i][j]
    p=[]
    for a in range(20):
        p.append(0)
    for i3 in range(i-4,i+5):
        for j3 in range(j-4,j+5):
            if (map[i3][j3] == k and i3 - i == j3 - j and i3 <= i and j3 <= j):
                p[0]+=1
            if (map[i3][j3] == k and j3 == j and i3 <= i and j3 <= j):
                p[1]+=1
            if (map[i3][j3] == k and i3 == i and i3 <= i and j3 <= j):
                p[2]+=1
            if (map[i3][j3] == k and i3 - i == j3 - j and i3 >= i and j3 >= j):
                p[3]+=1
            if (map[i3][j3] == k and j3 == j and i3 >= i and j3 >= j):
                p[4]+=1
            if (map[i3][j3] == k and i3 == i and i3 >= i and j3 >= j):
                p[5]+=1
            if (map[i3][j3] == k and i - i3 == j3 - j and i3 <= i and j3 >= j):
                p[6]+=1
            if (map[i3][j3] == k and i3 - i == j - j3 and i3 >= i and j3 <= j):
                p[7]+=1
            if (map[i3][j3] == k and j - j3 == i - i3 and i3 <= i + 1  and  i3 >= i - 3  and  j3 <= j + 1  and  j3 >= j - 3):
                p[8]+=1
            if (map[i3][j3] == k and j == j3 and i3 <= i + 1  and  i3 >= i - 3  and  j3 <= j + 1  and  j3 >= j - 3):
                p[9]+=1
            if (map[i3][j3] == k and i == i3 and i3 <= i + 1  and  i3 >= i - 3  and  j3 <= j + 1  and  j3 >= j - 3):
                p[10]+=1
            if (map[i3][j3] == k and j - j3 == i - i3 and i3 >= i - 1  and  i3 <= i + 3  and  j3 >= j - 1  and  j3 <= j + 3):
                p[11]+=1
            if (map[i3][j3] == k and j == j3 and i3 >= i - 1  and  i3 <= i + 3  and  j3 >= j - 1  and  j3 <= j + 3):
                p[12]+=1
            if (map[i3][j3] == k and i == i3 and i3 >= i - 1  and  i3 <= i + 3  and  j3 >= j - 1  and  j3 <= j + 3):
                p[13]+=1
            if (map[i3][j3] == k and i - i3 == j3 - j and i3 <= i + 1  and  i3 >= i - 3  and  j3 >= j - 1  and  j3 <= j + 3):
                p[14]+=1
            if (map[i3][j3] == k and i3 - i == j - j3 and i3 >= i - 1  and  i3 <= i + 3  and  j3 <= j + 1  and  j3 >= j - 3):
                p[15]+=1
            if (map[i3][j3] == k and j - j3 == i - i3 and i3 <= i + 2  and  i3 >= i - 2  and  j3 <= j + 2  and  j3 >= j - 2):
                p[16]+=1
            if (map[i3][j3] == k and j == j3 and i3 <= i + 2  and  i3 >= i - 2  and  j3 <= j + 2  and  j3 >= j - 2):
                p[17]+=1
            if (map[i3][j3] == k and i == i3 and i3 <= i + 2  and  i3 >= i - 2  and  j3 <= j + 2  and  j3 >= j - 2):
                p[18]+=1
            if (map[i3][j3] == k and i - i3 == j3 - j and i3 <= i + 2  and  i3 >= i - 2  and  j3 <= j + 2  and  j3 >= j - 2):
                p[19]+=1
    for b in range(20):
        if p[b]==5:
            win = 1
    

def get_input(currentPlayer):
    global win, map
    if currentPlayer == playerOne:
        player = "Player One's Turn"
        currentPlayerConn = playerConn[0]
        nextPlayerConn = playerConn[1]
    else:
        player = "Player Two's Turn"
        currentPlayerConn = playerConn[1]
        nextPlayerConn = playerConn[0]
    print(player)
    try:
        data = currentPlayerConn.recv(2048 * 10)
        currentPlayerConn.settimeout(20)
        dataDecoded = data.decode().split(",")
        x = int(dataDecoded[0])
        y = int(dataDecoded[1])
        map[x][y] = currentPlayer
        check_winner(x, y)
        currentPlayerConn.send(str(win).encode())
        data = data.decode() + "," + str(win)
        nextPlayerConn.send(data.encode())
    except:
        conn.send("Error".encode())
        print("Error occured! Try again..")

# Accept player
# Send player number
def accept_players():
    try:
        for i in range(2):
            conn, addr = s.accept()
            conn.send(str(i + 1).encode())
            playerConn.append(conn)
            playerAddr.append(addr)
            print("Player {} - [{}:{}]".format(i+1, addr[0], str(addr[1])))
        start_game()
        s.close()
    except socket.error as e:
        print("Player connection error", e)
    except KeyboardInterrupt:
            print("\nKeyboard Interrupt")
            exit()
    except Exception as e:
        print("Error occurred:", e)

def start_server():
    try:
        s.bind((host, port))
        print("go server started \nBinding to port", port)
        s.listen(2) 
        accept_players()
    except socket.error as e:
        print("Server binding error:", e)
        
def start_game():
    global win
    i = 0
    while win == 0 and i < 361 :
        if (i % 2 == 0):
            get_input(playerOne)
        else:
            get_input(playerTwo)
        
        i = i + 1
        

    time.sleep(10)
    for conn in playerConn:
        conn.close()


start_server()