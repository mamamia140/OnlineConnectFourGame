from base64 import decode
import numpy as np
import pygame
import sys
import math
from button import Button
import socket
 
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
 
ROW_COUNT = 6
COLUMN_COUNT = 7
 
def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board
 
def drop_piece(board, row, col, piece):
    board[row][col] = piece
 
def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0
 
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
 
def print_board(board):
    print(np.flip(board, 0))
 
def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True
 
    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True
 
    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
 
    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True
 
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(SCREEN, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(SCREEN, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):      
            if board[r][c] == 1:
                pygame.draw.circle(SCREEN, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(SCREEN, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()
 
def connectToTheServer(server_ip):
    port=12345
    mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    mysocket.connect((server_ip,port))
    print("connection established")
    return(mysocket)

#initalize pygame
pygame.init()

#define our SCREEN size
SQUARESIZE = 100

#define width and height of board
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

SCREEN = pygame.display.set_mode(size)


def play(gameSocket, playerNo):
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0
    #Calling function draw_board again
    draw_board(board)
    pygame.display.update()
    
    myfont = pygame.font.SysFont("monospace", 75)
    while not game_over:
        SCREEN.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, BLACK, (0,0, width, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if playerNo == 0:
                    if(turn==0):
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))
    
                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)
                            turn += 1
                            turn = turn % 2
                            coordinate = str(row) +'-'+ str(col)
                            gameSocket.send(coordinate.encode())

    
                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            SCREEN.blit(label, (40,10))
                            game_over = True
                    if(turn==1):
                        coordinate = gameSocket.recv(8192).decode()
                        coordinate = coordinate.partition("-")
                        print(int(coordinate[0]), int(coordinate[2]))
                        drop_piece(board, int(coordinate[0]), int(coordinate[2]), 1)
                        turn += 1
                        turn = turn % 2



                    
                    

    
    
                # # Ask for Player 2 Input
                else:
                    if(turn==0):
                        coordinate = gameSocket.recv(8192).decode()
                        coordinate = coordinate.partition("-")
                        print(int(coordinate[0]), int(coordinate[2]))
                        drop_piece(board, int(coordinate[0]), int(coordinate[2]), 0)
                        turn += 1
                        turn = turn % 2
                    if(turn==1):

                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))
    
                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 2)
                            turn += 1
                            turn = turn % 2
                            coordinate = str(row) +'-'+ str(col)
                            gameSocket.send(coordinate.encode())

    
                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            SCREEN.blit(label, (40,10))
                            game_over = True
                print_board(board)
                draw_board(board)
    
                if game_over:
                    pygame.time.wait(3000)

def createGame():
    s = socket.socket()        
    print ("Socket successfully created")
    port = 12345               
    s.bind(('', port))        
    print ("socket binded to %s" %(port))
    
    # put the socket into listening mode
    s.listen(2)    
    print ("socket is listening")

    while True:
        SCREEN.fill("black")
        OUTPUT_TEXT = pygame.font.SysFont(None, 45).render("Waiting for Other Player...", True, "#b68f40")
        OUTPUT_RECT = OUTPUT_TEXT.get_rect(center=(350, 300))
        SCREEN.blit(OUTPUT_TEXT, OUTPUT_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            c, addr = s.accept()
    
             #initialize the game
            play(c,0)
            # Close the connection with the client
            c.close()

        pygame.display.update()      

def joinGame():
    message="Enter an ip address"
    font = pygame.font.SysFont(None, 30)
    user_text = ''

    input_rect = pygame.Rect(245,300,180,32)
    color = pygame.Color('lightskyblue3')
    while True:
        SCREEN.fill("black")
        QUESTION_TEXT = pygame.font.SysFont(None, 45).render(message, True, "#b68f40")
        QUESTION_RECT = QUESTION_TEXT.get_rect(center=(350, 200))
        SCREEN.blit(QUESTION_TEXT, QUESTION_RECT)



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("hello")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[0:-1]
                elif event.key == pygame.K_RETURN:
                    c = connectToTheServer(user_text)
                    play(c,1)
                else:
                    user_text += event.unicode
        
        pygame.draw.rect(SCREEN,color,input_rect,2)
        text_surface = font.render(user_text,True,WHITE)
        SCREEN.blit(text_surface,(input_rect.x + 5,input_rect.y + 6))

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.fill("black")

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = pygame.font.SysFont(None, 100).render("Connect-Four", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 100))

        CREATE_BUTTON = Button(image=pygame.image.load("res/Rect.png"), pos=(350, 250), 
                            text_input="Create Game", font=pygame.font.SysFont(None, 75), base_color="#d7fcd4", hovering_color="White")
        JOIN_BUTTON = Button(image=pygame.image.load("res/Rect.png"), pos=(350, 400), 
                            text_input="Join Game", font=pygame.font.SysFont(None, 75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("res/Rect.png"), pos=(350, 550), 
                            text_input="Quit", font=pygame.font.SysFont(None, 75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [CREATE_BUTTON, JOIN_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CREATE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    createGame()
                if JOIN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    joinGame()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()