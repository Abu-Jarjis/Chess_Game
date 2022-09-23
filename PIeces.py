from hashlib import new
from tabnanny import check
from tkinter import VERTICAL
from click import password_option
import pygame as pg
import numpy as np
from Chess_Engine import Piece


class Pawn(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)

    def allowed_moves(self, cur_pos, cur_piece_clr, Board):
        k = 1 if cur_piece_clr == "w" else -1
        legal_mov = [cur_pos]
        new_x = cur_pos[0]
        new_y = cur_pos[1] - self.sqr_size * k

        for i in range(2):
            new_pos = (new_x, new_y)
            if new_pos not in Board.COORDINATES.keys():
                if cur_pos[1] // self.sqr_size != 6 and cur_pos[1] // self.sqr_size != 1: 
                    legal_mov.append(new_pos)
                    break
                legal_mov.append(new_pos)
                
                new_y = new_y - self.sqr_size * k

        #Check if current pawn can take any other piece   
        #-
        #-
        #-
        new_y = cur_pos[1] - self.sqr_size * k
        check_edible = [(new_x + self.sqr_size, new_y), (new_x - self.sqr_size, new_y)]
        for i in check_edible:
            if self.piece_type_color(i, Board)[1] not in (cur_piece_clr, "-"):
                legal_mov.append(i)

        return legal_mov
        
    
class Knight(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
        
    def allowed_moves(self, cur_pos, cur_piece_clr, Board):
        temp = [cur_pos]
        legal_mov = [cur_pos]
        new_x = cur_pos[0]
        new_y = cur_pos[1]
        
        for i in range(2):
            two_squares = 2 * self.sqr_size if i == 0 else -2 * self.sqr_size
            one_square = self.sqr_size if i == 0 else self.sqr_size * -1
            temp.append((new_x + two_squares, new_y + one_square))
            temp.append((new_x - two_squares, new_y + one_square))
            temp.append((new_x + one_square, new_y + two_squares))
            temp.append((new_x - one_square, new_y + two_squares))
        
        
        for xy in (temp):
            k = 0
            for i in xy:
                if i >= 0 and i <= 448:
                    k += 1
            if k == 2 and self.piece_type_color(xy, Board)[1] != cur_piece_clr:
                legal_mov.append(xy)
            

                
        #for ctr, xy in enumerate(legal_mov):
            #if self.piece_type_color(xy, Board)[1] in (cur_piece_clr):
                #legal_mov.pop(ctr)
        ##Check if current knight can take any other piece   
        #-
        #-
        #-
        return legal_mov
        
class Bishop(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
        
    def allowed_moves(self, cur_pos, cur_piece_clr, Board):
        legal_mov = self.sliding_pieces_movs("B", cur_pos, Board)
                
        return legal_mov       
        
        
class Rook(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
        
    def allowed_moves(self, cur_pos, cur_piece_clr, Board):
        legal_mov = self.sliding_pieces_movs("R", cur_pos, Board)
                
        return legal_mov       


class King(Piece):

    def __init__(self, window_length) -> None:
        super().__init__(window_length)
        
    def allowed_moves(self, cur_pos, cur_piece_clr, Board):
        legal_mov = self.sliding_pieces_movs("K", cur_pos, Board)
    
                
    def if_check(self, x):
        password_option




        
class Queen(Piece):

    def __init__(self, window_length) -> None:
        super().__init__(window_length)

    def allowed_moves(self, cur_pos, cur_piece_clr, Board):
        legal_mov = self.sliding_pieces_movs("Q", cur_pos, Board)
                
        return legal_mov       
        
