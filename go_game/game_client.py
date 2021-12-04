#!/usr/bin/python3
import socket, os, pygame, copy, sys
from pygame.locals import *
import numpy as np

s = socket.socket()
host = '127.0.0.1'
port = 9999

# init pygame
pygame.init()
pygame.mixer.init()

#顏色
background = (194, 157, 91)
checkerboard = (80, 80, 80)
button = ( 52, 53, 44)

currentPlayer = 0   # you
nextPlayer = 0      # the other player of the game
allow = False       # check is your turn or not
running = True        # check can u keep playing game or not

# draw the whoke chessboard
def Draw_a_chessboard(screen):  
    # fill background
    screen.fill(background)
    # draw chessboard
    for i in range(21):
        pygame.draw.line(screen, checkerboard, (40*i+3, 3), (40*i+3, 803)) 
        pygame.draw.line(screen, checkerboard, (3, 40*i+3), (803, 40*i+3))
    # draw lines
    pygame.draw.line(screen, checkerboard, (3, 3), (803, 3),5)   
    pygame.draw.line(screen, checkerboard, (3, 3), (3, 803),5)   
    pygame.draw.line(screen, checkerboard, (803, 3), (803, 803),5)   
    pygame.draw.line(screen, checkerboard, (3, 803), (803, 803),5) 
    
    # draw dots
    pygame.draw.circle(screen, checkerboard, (163, 163), 6) 
    pygame.draw.circle(screen, checkerboard, (163, 403), 6) 
    pygame.draw.circle(screen, checkerboard, (163, 643), 6) 
    pygame.draw.circle(screen, checkerboard, (643, 163), 6)  
    pygame.draw.circle(screen, checkerboard, (643, 403), 6)
    pygame.draw.circle(screen, checkerboard, (643, 643), 6) 
    pygame.draw.circle(screen, checkerboard, (403, 163), 6) 
    pygame.draw.circle(screen, checkerboard, (403, 403), 6) 
    pygame.draw.circle(screen, checkerboard, (403, 643), 6) 
    
    # set font
    s_font=pygame.font.Font('Anonymice Powerline Bold.ttf',28)

# draw chess
def Draw_a_chessman( x, y, screen, color):  
    print("x, y, color = ", x, y, screen, color)
    if color == 1:   
        Black_chess = pygame.image.load("Black_chess.png").convert_alpha()
        screen.blit(Black_chess,(40 * x + 3 - 15,40 * y + 3 - 15))
    if color == 2:
        White_chess = pygame.image.load("White_chess.png").convert_alpha()
        screen.blit(White_chess,(40 * x + 3 - 15, 40 * y + 3 - 15))

# create chessboard array
map=[]
for i in range(24):
    map.append([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

# init chessboard array
def clear():
    global map
    for i in range(24):
        for j in range(24):
            map[i][j]=0

# start client
def start_client():
    global currentPlayer, nextPlayer, allow
    try:
        s.connect((host, port))
        print("Connected to :", host, ":", port)
        playerNum = s.recv(2048 * 10).decode()
        # check is player one or player two
        if playerNum == '1':
            allow = True
            currentPlayer = 1
            nextPlayer = 2
        else:
            allow = False
            currentPlayer =2
            nextPlayer = 1
        start_game()
        s.close()
    except socket.error as e:
        print("Socket connection error:", e) 

# print end of msg
def end_of_game(screen):
    global allow, running
    # set screen background
    screen.fill(background)
    # set last msg
    if not allow:
        s = "you win!"
        allow = not(allow)
    else:
        s = "you lose"
        allow = not(allow)
    x = 30
    s_font=pygame.font.Font('Anonymice Powerline Bold.ttf',x)
    s_text=s_font.render(s,True,button)
    screen.blit(s_text,(340, 380))
    pygame.display.flip()
    # stop the game
    running=False 

def start_game():
    global map, running,maps, r, h, currentPlayer, nextPlayer, allow
    # init game
    clear()
    # u
    map2=copy.deepcopy(map)
    maps=[map2]

    # set screen
    screen = pygame.display.set_mode([806,806])
    # set screen name
    pygame.display.set_caption("五子棋")
    
    # draw chessboard
    Draw_a_chessboard(screen)
    pygame.display.flip()
    clock=pygame.time.Clock()

    while True:
        win = False
        for event in pygame.event.get():
            # exit
            if event.type ==pygame.QUIT:
                pygame.quit()
                sys.exit()

            # if its your turn 
            elif running and allow == 1 and event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    x,y=event.pos[0],event.pos[1]
                    for i in range(19):
                        for j in range(19):
                            # choose a place
                            if i*40+3+20<x<i*40+3+60 and j*40+3+20<y<j*40+3+60 and not map[i][j] and running:
                                coordinates = str(i) + "," + str(j)
                                # draw your chosen chess
                                Draw_a_chessman(i+1,j+1,screen,currentPlayer)
                                # record it into chessboard array
                                map[i][j]=currentPlayer

                                # u
                                map3=copy.deepcopy(map)
                                maps.append(map3)
                                # send the chosen place to server
                                s.send(coordinates.encode())
                                # check if current player win or not
                                win = s.recv(1024).decode()
                                pygame.display.flip()
                    # give the permission to another one
                    allow = not(allow)
            # if its not your turn
            elif running and not allow:
                data = s.recv(1024)
                dataDecoded = data.decode().split(",")
                # draw the chess of another player
                x = int(dataDecoded[0])
                y = int(dataDecoded[1])
                win = dataDecoded[2]
                Draw_a_chessman(x+1,y+1,screen,nextPlayer)
                # record it inot checkboard array
                map[x][y]=nextPlayer
                # u
                map3=copy.deepcopy(map)
                maps.append(map3)
                # get the permission
                allow = not(allow)
                pygame.display.flip()
            
            # check if win or not
            if win == "1":
                end_of_game(screen)
            
        clock.tick(60)

start_client()

