import pygame as pg
import numpy as np
import sys
import time
from Chess_Engine import Board, Piece
from PIeces import *

pg.init()
clock = pg.time.Clock()
np.set_printoptions(threshold=sys.maxsize)

#screen
res_x = res_y = 512
screen = pg.display.set_mode((res_x,res_y))


#board
board = Board(res_x)
board.preload_images()

#for i in board.COORDINATES.keys():
    #print(i)



#pieces
piece = Piece(res_x)
piece_classes = {"B":Bishop(res_x), "N":Knight(res_x), "R":Rook(res_x), "K":King(res_x), "Q": Queen(res_x), "p":Pawn(res_x)}

def move_handler(piece_classes, Piece, Board, event, screen):
        if (event.button, Board.game_state) == (1,1):
                cur_pos = Piece.sqr_select(pg.mouse.get_pos())
                print(cur_pos)
                if Piece.check_if_turn(cur_pos, screen, Board):
                    pass
                else:
                    return

                if cur_pos in Board.COORDINATES.keys():
                    Piece.current_piece = Board.COORDINATES[cur_pos]
                    Board.game_state = 0
                    Piece.prev_pos = cur_pos
                    prev_piece = Piece.piece_type_color(Piece.prev_pos, Board)

                    Piece.allowed = piece_classes[prev_piece[0][1]].allowed_moves(cur_pos, prev_piece[1], Board)
                else:
                    Board.error(cur_pos, screen)
                    #pg.display.update()
                    time.sleep(0.2)
        elif event.button == 1:
            new_pos = Piece.sqr_select(pg.mouse.get_pos())

            if Piece.prev_pos == new_pos:
                Board.game_state = 1
                return
                
            if new_pos in Piece.allowed:
                Piece.mov_piece(new_pos, Board)
            else:
                Board.error(new_pos, screen)
            Board.game_state = 1
    

while True:
    screen.fill((0,0,0))
    board.draw_board(screen)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            move_handler(piece_classes, piece, board, event, screen)
    if not board.game_state:
        piece
    (piece.allowed, screen)

    board.load_pieces(screen)    
    pg.display.update()
    clock.tick(15)
    