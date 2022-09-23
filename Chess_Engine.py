from cmath import pi
from tracemalloc import start
import pygame as pg
import numpy as np
import time
import sys

from pygame import color


pg.init()
clock = pg.time.Clock()



class Board:
    
    COLORS = {0 : (138,102,66), 1 : (244,226,198)}
    COORDINATES = {}
    piece_img = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]

    
    def __init__(self, window_length) -> None:
        self.board = np.array( [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                               ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                               ["-", "-", "-", "-", "-", "-", "-", "-"],
                               ["-", "-", "-", "-", "-", "-", "-", "-"],
                               ["-", "-", "-", "-", "-", "-", "-", "-"],
                               ["-", "-", "-", "-", "-", "-", "-", "-"],
                               ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                               ["wR", "wN", "wB", "wQ", "wK", "wB", 
                               "wN", "wR"]] )
        self.IMAGES = {piece : pg.image.load(f"images/{piece}.png") for piece in self.piece_img}
        self.cur_piece = 0
        self.move_log = []
        self.cur_turn = "w"
        self.game_state = 1
        self.dimension = 8
        self.sqr_size = int(window_length // self.dimension)

    def draw_board(self, screen):
        for row in range(self.dimension):
            for column in range(self.dimension):
                color = self.COLORS[(row+column)%2]
                pg.draw.rect(screen, color, pg.Rect(column * self.sqr_size, row * self.sqr_size, self.sqr_size , self.sqr_size))
                #(column * self.sqr_size, "-----", row*self.sqr_size)

    def preload_images(self):
        for row in range(self.dimension):
            for column in range(self.dimension):
                x,y = self.sqr_size * column, self.sqr_size * row
                piece = self.board[row, column]
                if piece != "-":
                    self.COORDINATES[(x,y)] = pg.transform.scale(self.IMAGES[piece], (self.sqr_size, self.sqr_size))
                
    
    def load_pieces(self, screen):
        for coordinate, piece in self.COORDINATES.items():
            screen.blit(piece, coordinate)

    def error(self, pos, screen):
        red = (170, 1, 20)
        pg.draw.rect(screen, red, pg.Rect(pos[0], pos[1], self.sqr_size, self.sqr_size))

            

class Piece:
    
    #piece_name = {"bR", "bN", "bB", "bQ", "bK", "bp",}
    #COORDINATES = {}
    
    def __init__(self, window_length) -> None:
        #super().__init__(window_length)
        self.dimension = 8
        self.sqr_size = window_length//8
        self.cur_turn = 'w'
        self.current_piece = 0
        self.prev_pos = 0
        self.allowed = []


    
    def sqr_select(self, pos):
        s_x = s_y = 0
        s_x = pos[0] - pos[0] % self.sqr_size
        s_y = pos[1] - pos[1] % self.sqr_size

        return (s_x, s_y)

    def piece_type_color(self, pos, Board):
        ctr = 0
        new_x = int(pos[0] // self.sqr_size) 
        new_y = int(pos[1] // self.sqr_size)
        if new_x == 8:
            cur_piece = Board.board[new_y, 7]
        else:
          cur_piece = Board.board[new_y, new_x] 
        cur_piece_color = cur_piece[0] if cur_piece[0] != "-" else "-"
        piece_n_color = [cur_piece, cur_piece_color]
        
        #if type(piece_n_color[0]) == int:
            #for i in piece_n_color[0]:
                #if i < 0 or i > 448:
                    #ctr += 1
        return piece_n_color

    def check_if_turn(self, pos, screen, Board):
        piece_n_color = self.piece_type_color(pos, Board)
        if piece_n_color[1] == self.cur_turn:
                return True
        else:
            Board.error(pos, screen)
            return False

    def highlight_valid(self, allowed, screen, half_sqr):
        color = {0 : (72,209,204) , 1 : (175, 238, 255)}
        for pos in allowed:
            center = (pos[0] + half_sqr, pos[1] + half_sqr)
            sqr_color = color[((pos[0]+pos[1]) // self.sqr_size) % 2]
            pg.draw.rect(screen, sqr_color, pg.Rect(pos[0], pos[1], self.sqr_size, self.sqr_size))
        pass
    
    def mov_piece(self, cur_pos, Board):
        new_x = int(cur_pos[0] // Board.sqr_size)
        new_y = int(cur_pos[1] // Board.sqr_size)
        prev_x = int(self.prev_pos[0] // Board.sqr_size)
        prev_y = int(self.prev_pos[1] // Board.sqr_size)

        Board.board[new_y, new_x] = Board.board[prev_y, prev_x]   
            
        if cur_pos != self.prev_pos :
            Board.board[prev_y, prev_x] = "-"
            Board.COORDINATES.pop(self.prev_pos)

        Board.COORDINATES[cur_pos] = self.current_piece 
        #self.current_piece = 0
        self.cur_turn = "b" if self.cur_turn == "w" else "w"


    def compute_sliding_piece_movs(self, start_sqr, cur_dir, piece_type):
        dir_index = {0 : (0,-1), 1 : (1,0), 2 : (0,1), 3 : (-1,0), 4 : (-1,-1), 5 : (1, -1), 6 : (1,1), 7 : (-1,1)}
        temp_dir = dir_index[cur_dir]
        temp_moves = []

        for x in range(self.sqr_size, 512, self.sqr_size):
                limit_check = 0
                temp_x = (x * temp_dir[0]) + start_sqr[0]
                temp_y = (x * temp_dir[1]) + start_sqr[1]
                x_y = (temp_x, temp_y)

                #func = lambda x : max(x) <= 448 and min(x) >= 0
                if max(x_y) <= 448 and min(x_y) >= 0:
                    temp_moves.append(x_y)
                
                if piece_type == "K":
                            break #add only one block for each direction
        #temp_moves = list(filter(func, (x_y for x_y in temp_moves)))
        print(temp_moves)
        return temp_moves


    def sliding_pieces_movs(self, piece_type, start_sqr, Board):
        start_dir = 4 if piece_type == "B" else 0
        end_dir = 4 if piece_type == "R" else 8

        legal_movs = [start_sqr]
        piece = self.piece_type_color(start_sqr, Board)

        for dir in range(start_dir, end_dir):
            temp_moves = self.compute_sliding_piece_movs(start_sqr, dir, piece_type)

            for moves in temp_moves:
                color = self.piece_type_color(moves, Board)[1]
                if color != piece[1] and color != "-":
                    legal_movs.append(moves)
                    break
                elif color == piece[1]:
                    break
                print(piece[1])
                legal_movs.append(moves)
        return legal_movs
    
    def check_enemy_attacks(self):
        
        pass



    
    
   
