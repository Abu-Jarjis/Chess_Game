import pygame as pg
import numpy as np
from Chess_Engine import Board



class Piece(Board):
    
    
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
        self.W_moves = []
        self.B_moves = []
        


    
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
    def unnamed_func(self, new_pos, Board, test_if_check):
        pass

    def mov_piece(self, new_pos, Board, test_if_check):
        
        self.current_piece = Board.COORDINATES[self.prev_pos]
        new_x = int(new_pos[0] // Board.sqr_size)
        new_y = int(new_pos[1] // Board.sqr_size)
        prev_x = int(self.prev_pos[0] // Board.sqr_size)
        prev_y = int(self.prev_pos[1] // Board.sqr_size)
        (prev_x, prev_y,new_x, new_y)
        piece_type = self.piece_type_color(self.prev_pos, Board)[0]
        Board.board[new_y, new_x] = Board.board[prev_y, prev_x]  
            
        if new_pos != self.prev_pos and not test_if_check :
            Board.board_static[prev_y, prev_x] = "-"
            Board.COORDINATES.pop(self.prev_pos)
        if new_pos != self.prev_pos and  test_if_check :
            Board.board[prev_y, prev_x] = "-"
            Board.COORDINATES.pop(self.prev_pos)

        Board.COORDINATES[new_pos] = self.current_piece
        (Board.board)

        #(PIECE_CLASSES[piece_type[1]].move_ctr_B, PIECE_CLASSES[piece_type[1]].move_ctr_W)
        #self.current_piece = 0

    def move_logging(self, new_pos, Board):
        new_x = int(new_pos[0] // Board.sqr_size)
        new_y = int(new_pos[1] // Board.sqr_size)
        prev_x = int(self.prev_pos[0] // Board.sqr_size)
        prev_y = int(self.prev_pos[1] // Board.sqr_size)
        return Board.board_algebra[prev_y, prev_x], Board.board[new_y, new_x]

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

        return temp_moves


    def sliding_pieces_movs(self, piece_type, start_sqr, Board, check_attack_sqr):
        start_dir = 4 if piece_type == "B" else 0
        end_dir = 4 if piece_type == "R" else 8

        legal_movs = [start_sqr]
        piece = self.piece_type_color(start_sqr, Board)
        
        for dir in range(start_dir, end_dir):
            temp_moves = self.compute_sliding_piece_movs(start_sqr, dir, piece_type)

            for move in temp_moves:
                color = self.piece_type_color(move, Board)[1]
                if color != piece[1] and color != "-":
                    legal_movs.append(move)
                    break
                if color == piece[1] and check_attack_sqr:
                    legal_movs.append(move)
                    break
                if color == piece[1]:
                    break

                legal_movs.append(move)
        return legal_movs

    def check_enemy_attacks(self, Board, Piece):
        king_color = ""
        king_square = 0
        squares = []
        for rank in range(0, self.sqr_size*8, self.sqr_size):
            for file in range(0, self.sqr_size*8,  self.sqr_size):
                cur_pos = (file, rank)
                cur_color = self.piece_type_color(cur_pos, Board)[1]

                if cur_pos in Board.COORDINATES.keys() and  cur_color == Piece.cur_turn:
                    cur_piece = self.piece_type_color(cur_pos, Board)[0]
                    if cur_piece == f"{self.cur_turn}K":
                        king_square, king_color = cur_pos, cur_piece[0]

                if cur_pos in Board.COORDINATES.keys() and cur_color != Piece.cur_turn:
                    cur_piece = self.piece_type_color(cur_pos, Board)[0][1]

                    if cur_piece == "p":
                        pawn = PIECE_CLASSES[cur_piece]
                        pawn.allowed_moves(cur_pos, cur_color, Board, Piece)
                        squares.extend(pawn.check_edible(pawn.new_y, pawn.new_x))
                        continue
                    

                    squares.extend(PIECE_CLASSES[cur_piece].allowed_moves(cur_pos, cur_color, Board, Piece, check_attack_sqr = True)[1:])

                


        return squares, king_square, king_color
    

class Pawn(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
        self.new_y = 0
        self.new_x = 0
        self.cur_piece_clr = 0


    def check_edible(self, new_y, new_x):
        legal_movs = []
        check_edible = [(new_x + self.sqr_size, new_y), (new_x - self.sqr_size, new_y)]
        return check_edible

      

    def allowed_moves(self, cur_pos, cur_piece_clr, Board, Piece, check_attack_sqr = False):
        k = 1 if cur_piece_clr == "w" else -1
        legal_mov = [cur_pos]
        new_x = cur_pos[0]
        new_y = cur_pos[1] - self.sqr_size * k

        for _ in range(2):
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

        self.new_y = new_y
        self.new_x = new_x
        self.cur_piece_clr = cur_piece_clr
        check_edible = [(new_x + self.sqr_size, new_y), (new_x - self.sqr_size, new_y)]
        for move in check_edible:
            if self.piece_type_color(move, Board)[1] not in (cur_piece_clr, "-"):
                legal_mov.append(move)
        return legal_mov
        
    
class Knight(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
    
    

    def allowed_moves(self, cur_pos, cur_piece_clr, Board, Piece, check_attack_sqr = False):
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

            if max(xy) <= 448 and min(xy) >= 0:
                if check_attack_sqr:
                    legal_mov.append(xy)
                elif  self.piece_type_color(xy, Board)[1] != cur_piece_clr:
                    legal_mov.append(xy)
            
            

                
        #for ctr, xy in enumerate(legal_mov):
            #if self.piece_type_color(xy, Board)[1] in (cur_piece_clr):
                #legal_mov.pop(ctr)
        ##Check if current knight can take any other piece   
        #-
        #-
        #-
        if check_attack_sqr:
            return legal_mov[1:]
        return legal_mov
        
class Bishop(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
    
        
    def allowed_moves(self, cur_pos, cur_piece_clr, Board, Piece, check_attack_sqr = False):
        legal_mov = self.sliding_pieces_movs("B", cur_pos, Board, check_attack_sqr)
                
        return legal_mov       
        
        
class Rook(Piece):

    def __init__(self, window_length ) -> None:
        super().__init__(window_length)
    
        
    def allowed_moves(self, cur_pos, cur_piece_clr, Board, Piece, check_attack_sqr = False):
        legal_mov = self.sliding_pieces_movs("R", cur_pos, Board, check_attack_sqr)
                
        return legal_mov       


class King(Piece):

    def __init__(self, window_length) -> None:
        super().__init__(window_length)
        self.W_King_startsqr = (self.sqr_size * 4, self.sqr_size * 7)
        self.B_King_startsqr = (self.sqr_size * 4, 0)
        self.king_side_castle_movs = [self.sqr_size * n for n in range(5, 7)]
        self.queen_side_castle_movs = [self.sqr_size * n for n in range(1,4)]
            
    def still_in_check(self):
        pass
    def if_castle(self, cur_pos, cur_piece_clr, Board, logger):
        ("runnning")
        castle_movs = []
        rook_right = self.piece_type_color((self.sqr_size * 7 , cur_pos[1]), Board)[0]
        rook_left = self.piece_type_color((0, cur_pos[1]), Board)[0]
        print(logger)
        for mov in logger:
            if f"{cur_piece_clr}K" in  mov:
                return castle_movs

        castle_movs.extend(self.king_side_castle(cur_pos, logger, rook_right))
        castle_movs.extend(self.queen_side_castle(cur_pos, logger, rook_left))


        
            
        return castle_movs

    def king_side_castle(self, cur_pos, logger, rook_right):
        rook = f"{self.cur_turn}R"
        castle_movs = []
        flag = 0
        #if rook_right == rook:
            #for mov in logger:
                #if "h8" in mov or "h1" in mov:
                    #return []

        for x in self.king_side_castle_movs:
            if (x, cur_pos[1]) not in Board.COORDINATES.keys():
                flag += 1
        if flag == 2:
            ("FLAG 2")
            castle_movs.append((self.king_side_castle_movs[-1], cur_pos[1]))

        return castle_movs
    
    def queen_side_castle(self, cur_pos, logger, rook_left):
        rook = f"{self.cur_turn}R"
        castle_movs = []
        flag = 0
        #if rook_left == rook:
            #for mov in logger:
                #if "a8" in mov or "a1" in mov:
                    #return []

        for x in self.queen_side_castle_movs:
            if (x, cur_pos[1]) not in Board.COORDINATES.keys():
                flag += 1
        if flag == 3:
            
            castle_movs.append((self.queen_side_castle_movs[1], cur_pos[1]))
        return castle_movs

    def allowed_moves(self, cur_pos, cur_piece_clr, Board, Piece, check_attack_sqr = False, sqr_attacks = []):
        piece_log = {"w": Piece.W_moves, "b": Piece.B_moves}
        legal_mov = self.sliding_pieces_movs("K", cur_pos, Board, check_attack_sqr)
        legal_mov.append(cur_pos)
        legal_mov_2 = list(filter(lambda move: move not in sqr_attacks, legal_mov))

        castle_movs_temp  = self.if_castle(cur_pos, cur_piece_clr, Board, piece_log[Piece.cur_turn])
        print(Piece.cur_turn)
        (castle_movs_temp)
        #(list(filter(lambda mov: mov in sqr_attacks, castle_movs_temp)))
        castle_movs = [] if list(filter(lambda mov: mov in sqr_attacks, castle_movs_temp)) else castle_movs_temp[:]
        (castle_movs)
        if castle_movs:
            legal_mov_2.extend(castle_movs)
        
        if cur_pos in sqr_attacks:
            return ("King_Checked", legal_mov_2)
        return legal_mov_2




        
class Queen(Piece):

    def __init__(self, window_length) -> None:
        super().__init__(window_length)
    

    def allowed_moves(self, cur_pos, cur_piece_clr, Board, Piece, check_attack_sqr = False):
        legal_mov = self.sliding_pieces_movs("Q", cur_pos, Board, check_attack_sqr)
                
        return legal_mov       

RES_X = 512
PIECE_CLASSES = {"B":Bishop(RES_X), "N":Knight(RES_X), "R":Rook(RES_X), "K":King(RES_X), "Q": Queen(RES_X), "p":Pawn(RES_X)}



        
