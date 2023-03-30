
from tracemalloc import start
import pygame as pg
import numpy as np
#from PIeces import Bishop, Knight, Rook, King, Queen, Pawn



from pygame import color


pg.init()
clock = pg.time.Clock()
res_x =512


class Board:
    
    COLORS = {0 : (138,102,66), 1 : (244,226,198)}
    COORDINATES = {}
    piece_img = ["bR", "bN", "bB", "bQ", "bK", "bp", "wR", "wN", "wB", "wQ", "wK", "wp"]
    sqr_algebra = ["a", "b", "c", "d", "e", "f", "g", "h"]

    
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
        self.board_algebra = np.array([["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"],
                                        ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"],
                                        ["a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6"],
                                        ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"],
                                        ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"],
                                        ["a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3"],
                                        ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"],
                                        ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]])
        self.IMAGES = {piece : pg.image.load(f"images/{piece}.png") for piece in self.piece_img}
        self.piece_algebra = {}
        self.cur_piece = 0
        self.cur_turn = "w"         
        self.game_state = 1
        self.dimension = 8
        self.sqr_size = int(window_length // self.dimension)

    def algebra_dict(self):
        for letr in self.sqr_algebra:
            self.piece_algebra[letr]

        pass
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

            





    
    
   
