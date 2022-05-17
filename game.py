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


def play():
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0
    #Calling function draw_board again
    draw_board(board)
    pygame.display.update()
    
    myfont = pygame.font.SysFont("monospace", 75)
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
    
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(SCREEN, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(SCREEN, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(SCREEN, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(SCREEN, BLACK, (0,0, width, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
    
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 1)
    
                        if winning_move(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            SCREEN.blit(label, (40,10))
                            game_over = True
    
    
                # # Ask for Player 2 Input
                else:               
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))
    
                    if is_valid_location(board, col):
                        row = get_next_open_row(board, col)
                        drop_piece(board, row, col, 2)
    
                        if winning_move(board, 2):
                            label = myfont.render("Player 2 wins!!", 1, YELLOW)
                            SCREEN.blit(label, (40,10))
                            game_over = True
    
                print_board(board)
                draw_board(board)
    
                turn += 1
                turn = turn % 2
    
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
        MENU_TEXT = pygame.font.SysFont(None, 45).render("Waiting for Other Player...", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(350, 300))
        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            c, addr = s.accept()    
            print ('Got connection from', addr )
    
            # send a thank you message to the client. encoding to send byte type.
            c.send('Thank you for connecting'.encode())
    
             #initialize the game
            play()
            # Close the connection with the client
            c.close()

        pygame.display.update()      

def joinGame():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        OPTIONS_TEXT = pygame.font.SysFont(None, 75).render("This is the OPTIONS SCREEN.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(350, 260))
        SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(350, 460), 
                            text_input="BACK", font=pygame.font.SysFont(None, 75), base_color="Black", hovering_color="Green")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

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