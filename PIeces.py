from hashlib import new
import pygame as pg
import numpy as np
import sys
import time
from Chess_Engine import Piece


class Pawn(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)

    def allowed_moves(self, cur_pos, cur_piece_clr, Board):
        k = 1 if cur_piece_clr == "w" else -1
        allowed = [cur_pos]
        new_x = cur_pos[0]
        new_y = cur_pos[1] - self.sqr_size * k

        for i in range(2):
            new_pos = (new_x, new_y)
            print(new_pos, self.cur_turn)
            if new_pos not in Board.COORDINATES.keys():
                if cur_pos[1] // self.sqr_size != 6 and cur_pos[1] // self.sqr_size != 1: 
                    allowed.append(new_pos)
                    break
                allowed.append(new_pos)
                
                new_y = new_y - self.sqr_size * k

        #Check if current pawn can take any other piece   
        #-
        #-
        #-
        new_y = cur_pos[1] - self.sqr_size * k
        check_edible = [(new_x + self.sqr_size, new_y), (new_x - self.sqr_size, new_y)]
        for i in check_edible:
            if self.piece_type_color(i, Board)[1] not in (cur_piece_clr, "-"):
                allowed.append(i)
        print(allowed)
        return allowed
        
        
class Knight(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
        
    def allowed_moves(self, cur_pos, cur_piece):
        pass
        
class Bishop(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
        
    def allowed_moves(self, cur_pos, cur_piece):
        pass
        
class Rook(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
        
    def allowed_moves(self, cur_pos, cur_piece):
        pass
        
class King(Piece):

    def __init__(self, window_length) -> None:
        super().__init__(window_length)
        
    def allowed_moves(self, cur_pos, cur_piece):
        pass
        
class Queen(Piece):

    def __init__(self, window_length) -> None:
        super().__init__(window_length)
    def allowed_moves(self, cur_pos, cur_piece):
        pass
        