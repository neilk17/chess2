import pygame
from Chess import ChessEngine

# from chess import ChessEngine 

WIDTH, HEIGHT = 512, 512
DIMENSIONS = 8 #8x8 chess board 
SQ_SIZE = WIDTH//8
MAX_FPS = 15
IMAGES = {}
pygame.init()

# green = rgb(42,128,0)
def load_images():
    '''
    initialize global dictionary of images from image file
    '''
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load("images/{}.png".format(piece)), (SQ_SIZE, SQ_SIZE))
    
    return IMAGES

def main():
    '''
    handle user input and updating graphics
    '''
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill((255, 255, 255))
    gs = ChessEngine.GameState()
    load_images() 
    run=True
    sq_selected = () # (row, col) nothing selected initially, keep track of last click of user 
    player_clicks = [] # keep track of player clicks (two touples) [(6, 4), (8, 3)] 
    while run:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                run = False
            elif i.type == pygame.MOUSEBUTTONDOWN:
                location = pygame.mouse.get_pos() #x and y location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sq_selected == (row, col):
                    sq_selected = ()
                    player_clicks  = []
                else:
                    sq_selected = (row, col)
                    player_clicks.append(sq_selected)
                
                if len(player_clicks) == 2:
                    # print(player_clicks)
                    move = ChessEngine.Move(player_clicks[0], player_clicks[1], gs.board)
                    print(move.get_chess_notation())
                    gs.make_move(move)
                    sq_selected = () 
                    # reset the user click
                    player_clicks = []

        draw_game_state(screen, gs.board)
        clock.tick(MAX_FPS)
        pygame.display.flip()


def draw_game_state(screen, game_state):
    '''
    responsible for all graphics within the current game state
    '''
    draw_board(screen)
    draw_pieces(screen, game_state) # will draw piece on top of squares

# top left square is light
def draw_board(screen):
    # white and green
    colors = [(255, 255, 255, 255), (0, 128, 42, 0)]
    for row in range(DIMENSIONS):
        for col in range(DIMENSIONS):
            color = colors[(row+col)%2]
            rect = pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE)
            pygame.draw.rect(screen, color, rect)

def draw_pieces(screen, board):
    '''
    draw pieces on the board using the current game state 
    '''
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece != "==":
                screen.blit(IMAGES[piece], pygame.Rect(col*SQ_SIZE, row*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == '__main__':
    main()