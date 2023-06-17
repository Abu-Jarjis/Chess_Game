import pygame as pg
import numpy as np
import sys
import time
from PIeces import *
from Chess_Engine import Board

pg.init()
clock = pg.time.Clock()
np.set_printoptions(threshold=sys.maxsize)

#SCREEN
res_x = res_y = 512
SCREEN = pg.display.set_mode((res_x,res_y), pg.RESIZABLE)

#BOARD
BOARD = Board(res_x)
BOARD.preload_images()

#pieces
PIECE = Piece(res_x)


def if_check(king_allowed_movs, king_square, cur_pos, enemy_attack_squares):
    if "King_Checked" in king_allowed_movs:
            ("CHECKED_KING")
            if cur_pos == king_square:
                ("SELECT_KING")
                #cur_pos = king_square
                #PIECE.current_piece = BOARD.COORDINATES[cur_pos]
                PIECE.prev_pos = cur_pos
                prev_piece = PIECE.piece_type_color(PIECE.prev_pos, BOARD)
                PIECE.allowed = PIECE_CLASSES[prev_piece[0][1]].allowed_moves(cur_pos, prev_piece[1], BOARD, PIECE, sqr_attacks = enemy_attack_squares[0][::])[1]
                
            else:
                ("ERROR")
                BOARD.error(cur_pos, SCREEN)
                return False
    return True

def still_check(cur_piece, new_pos):
    PIECE.mov_piece(new_pos, BOARD, test_if_check=True)
    

    pass
    

def castle_rook(new_pos):
    castle_left =  PIECE_CLASSES["K"].queen_side_castle_movs[1]
    castle_right = PIECE_CLASSES["K"].king_side_castle_movs[-1]

    if new_pos[0] == castle_right:
        new_castle_pos = new_pos[0] - PIECE.sqr_size
        PIECE.prev_pos = (castle_right + PIECE.sqr_size, new_pos[1])
        PIECE.mov_piece(( new_castle_pos, new_pos[1]), BOARD, test_if_check=True)

    elif new_pos[0] == castle_left:
        new_castle_pos = new_pos[0] + PIECE.sqr_size
        PIECE.prev_pos = (castle_left - 2*PIECE.sqr_size, new_pos
        [1])
        PIECE.mov_piece((new_castle_pos, new_pos[1]), BOARD, test_if_check=True)
    pass


def move_handler(event):
        if (event.button, BOARD.game_state) == (1,3):
            BOARD.game_state = 0
            return
            pass
        if (event.button, BOARD.game_state) == (1,1):
            
                cur_pos = PIECE.sqr_select(pg.mouse.get_pos())

                if not PIECE.check_if_turn(cur_pos, SCREEN, BOARD):
                    return

                if cur_pos in BOARD.COORDINATES.keys():
                    #§§§PIECE.current_piece = BOARD.COORDINATES[cur_pos]
                    
                    PIECE.prev_pos = cur_pos
                    prev_piece = PIECE.piece_type_color(PIECE.prev_pos, BOARD)
                    enemy_attack_squares = PIECE.check_enemy_attacks(BOARD, PIECE)
                    king_square, king_color = enemy_attack_squares[1], enemy_attack_squares[2]
                    king_allowed_movs = PIECE_CLASSES["K"].allowed_moves(king_square, king_color, BOARD, PIECE, check_attack_sqr = False, sqr_attacks = enemy_attack_squares[0][::])
                    
                    if prev_piece[0][1] == "K":
                        PIECE.allowed[::] = king_allowed_movs[::]
                    else:
                        PIECE.allowed = PIECE_CLASSES[prev_piece[0][1]].allowed_moves(cur_pos, prev_piece[1], BOARD, PIECE)
                    
                    #Checks if king is in check
                    #and runs function
                    #
                    #
                    if not if_check(king_allowed_movs, king_square, cur_pos, enemy_attack_squares):
                        return
                            
                        

                    BOARD.game_state = 0




                else:
                    BOARD.error(cur_pos, SCREEN)
                    #pg.display.update()
                    time.sleep(0.5)

        elif event.button == 1:
            new_pos = PIECE.sqr_select(pg.mouse.get_pos())


            if PIECE.prev_pos == new_pos:
                BOARD.game_state = 1
                return

            if PIECE.piece_type_color(new_pos, BOARD)[0][0] == PIECE.cur_turn:
                BOARD.game_state = 1
                return True
                
            if new_pos in PIECE.allowed:
                cur_piece = PIECE.piece_type_color(PIECE.prev_pos, BOARD)[0]
                PIECE.mov_piece(new_pos, BOARD, test_if_check=True)
                prev_sqr, after_sqr = PIECE.move_logging(new_pos, BOARD)

                if PIECE.cur_turn == "w":
                    PIECE.W_moves.append((cur_piece, prev_sqr, after_sqr))
                    print("STORED WHITE")
                if PIECE.cur_turn == "b":
                    PIECE.B_moves.append((cur_piece, prev_sqr, after_sqr))
                    print("STORED BLACK")
                
                
            
                (cur_piece)
                if cur_piece[1] == "K":
                    ("WORKS")
                    if PIECE_CLASSES["K"].W_King_startsqr == PIECE.prev_pos or PIECE_CLASSES["K"].B_King_startsqr == PIECE.prev_pos:
                        ("WORKS")
                        castle_rook(new_pos)
                    
                PIECE.cur_turn = "b" if PIECE.cur_turn == "w" else "w"
                    

            else:
                BOARD.error(new_pos, SCREEN)
                
            BOARD.game_state = 1


def Run_Chess():
    

    while True:
        SCREEN.fill((0,0,0))
        BOARD.draw_board(SCREEN)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if move_handler(event):
                    move_handler(event)
            if event.type == pg.VIDEORESIZE:
                pass
        #PIECE.highlight_valid(PIECE.check_enemy_attacks(BOARD,PIECE)[0], SCREEN, int(res_x // 16))
        if not BOARD.game_state:
            PIECE.highlight_valid(PIECE.allowed, SCREEN, int(res_x // 16))
        #(BOARD.move_log)
        #PIECE.highlight_valid(PIECE.check_enemy_attacks(BOARD, PIECE)[0], SCREEN, int(res_x // 16))
        #PIECE.highlight_valid([[128,448]], SCREEN, int(res_x//16))
        BOARD.load_pieces(SCREEN)    
        pg.display.update()
        clock.tick(30)

Run_Chess()
    
