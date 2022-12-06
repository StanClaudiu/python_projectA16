import random
import time
class backgroundBoard:
    def __init__(self):
        # pretty self explanatory I believe
        self.possible_basic_piece = [["wC", "wH", "wB", "wK", "wQ", "wP"], [
            "bC", "bH", "bB", "bK", "bQ", "bP"]]
        self.check_mate_flag = False
        self.change_event_going_on = False
        self.possible_current_moves = []
        self.bad_moves = []
        self.casteling = [[True,True],[True,True]]
        self.special_moves_list = []
        self.board = [["wC", "wH", "wB", "wK", "wQ", "wB", "wH", "wC"],
                      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                      ["bC", "bH", "bB", "bK", "bQ", "bB", "bH", "bC"]]
        self.turn = 0  # meaning first one, easy to to 1-self.turn
        self.turn_color = ["w","b"]
    stack_all_transformations = list()

    def find_my_king(self,turn):
        king_I_want = self.turn_color[turn] + "K"
        for row in range(0,8):
            for col in range(0,8):
                if (self.board[row][col] == king_I_want) : 
                    return (col,row)

    def make_copy(self): # creates a shallow copy of the calling board
        copy_game = backgroundBoard()
        copy_game.board = [line[:] for line in self.board]
        copy_game.possible_current_moves = self.possible_current_moves.copy()
        copy_game.bad_moves = self.bad_moves.copy()
        copy_game.casteling = [ casteling[:] for casteling in self.casteling]
        copy_game.special_moves_list = self.special_moves_list.copy()
        copy_game.turn = self.turn
        copy_game.check_mate_flag = self.check_mate_flag
        return copy_game

    def valid_first_selection(self, pos_tuple): # we verify the color + if there are possible locations to move zero_check
        (f_row, f_col) = pos_tuple
        valid_click = self.verify_good_turn_color(pos_tuple) and self.verify_possible_move(pos_tuple)
        print("Primul click este valid : ", valid_click)
        self.possible_current_moves,self.bad_moves= self.check_good_positions(pos_tuple)
        if self.check_mate_function():
            self.check_mate_flag = True
            valid_click = False # there's nothig  we can do
        return valid_click

    def verify_good_turn_color(self, pos_tuple): # we verify the color used
        row, col = pos_tuple
        if self.board[row][col] == "--":
            return False  # we first clicked a wrong pos
        if self.board[row][col][0] == "b" and self.turn == 0:
            return False  # you are white, pick white!
        if self.board[row][col][0] == "w" and self.turn == 1:
            return False  # you are white, pick white!
        return True

    def verify_possible_move(self, f_pos_tuple): # verify if there are good moves, evidently uses self.board
        possible_zero_check_move = self.search_for_possible_moves_zero_check(f_pos_tuple)
        return possible_zero_check_move

    def search_for_possible_moves_zero_check(self,f_pos_tuple): # verify if there are possible moves, resets poss and special without the check functions, uses the self.board
        self.possible_current_moves = []
        self.special_moves_list = []
        f_row, f_col = f_pos_tuple
        piece_to_move = self.board[f_row][f_col]
        valid_move = True
        match piece_to_move[1]:
           case "K":
               valid_move = self.find_pos_basic_moves_king(f_pos_tuple)
               valid_move_special =  self.find_special_moves(f_pos_tuple)
               valid_move = valid_move_special or valid_move
           case "Q":
               valid_moves_Ox_Oy = self.find_pos_colision_Oy_Ox(f_pos_tuple)
               valid_moves_diagonally = self.find_pos_collision_diagonally(
                   f_pos_tuple)
               valid_move = valid_moves_Ox_Oy or valid_moves_diagonally
               if valid_move:
                   print("I can make the following moves : ",
                         self.possible_current_moves)
           case "P":
               valid_move = self.find_pos_basic_moves_pioneer(f_pos_tuple)
               valid_move_special = self.find_special_moves(f_pos_tuple)
               valid_move = valid_move_special or valid_move
           case "C":
               valid_moves_Ox_Oy = self.find_pos_colision_Oy_Ox(f_pos_tuple)
               valid_move = valid_moves_Ox_Oy
           case "B":
               valid_moves_diagonally = self.find_pos_collision_diagonally(
                   f_pos_tuple)
               valid_move = valid_moves_diagonally
           case "H":
               valid_moves_basic = self.find_pos_basic_moves_horse(
                   f_pos_tuple)
               valid_move = valid_moves_basic
        return valid_move
   
    # check_functions

    def simple_check_function(self,board,turn): # verify if the turn's king is in danger RIGHT-NOW!
        wanted_king = self.turn_color[turn] + "K"
        r_king,c_king = 0,0
        for king_row in range(0,8):
            for king_col in range(0,8):
                if wanted_king == board[king_row][king_col]:
                    r_king,c_king = king_row,king_col
                    break
        
        for line in range(0,8):
            for col in range(0,8):
                if board[line][col][0] == self.turn_color[1-turn]:
                    temporary_game = self.make_copy()
                    temporary_game.turn = 1 - turn # the enemy
                    temporary_game.board = board.copy()
                    temporary_game.search_for_possible_moves_zero_check((line,col))
                    basic_moves_enemy = temporary_game.basic_moves_finder() 
                    if (r_king,c_king) in  basic_moves_enemy :
                        return True # we are in check
        return False

    def check_good_positions(self,f_pos_tuple): # verify the good position in a given state, does not modify self.possible_states
        f_line,f_col = f_pos_tuple
        temporary_game = self.make_copy()
        temporary_game.search_for_possible_moves_zero_check(f_pos_tuple)

        basic_moves = temporary_game.basic_moves_finder()
        special_moves = temporary_game.special_moves_list.copy()

        special_moves_pos = list(map(lambda x : x[0],special_moves))
        basic_moves = list(filter(lambda x : x not in special_moves_pos,basic_moves))

        good_basic_move =[]
        good_special_move =[]
        bad_moves =[]

        piece = temporary_game.board[f_line][f_col]
        for basic_move in basic_moves:
            new_game = temporary_game.make_copy()
            move_line,move_column = basic_move
            new_game.board[move_line][move_column] = piece
            new_game.board[f_line][f_col] = "--"
            if new_game.simple_check_function(new_game.board,new_game.turn):
                bad_moves.append(basic_move)
            else:
                good_basic_move.append(basic_move)
       
        for special_move in special_moves:
            #special case king in check
            if special_move[1] in ["casteling-right","casteling-left"]: # we have a king sit
                print('Caz special rege, la castelare ')
                new_game = temporary_game.make_copy()
                if new_game.simple_check_function(new_game.board,new_game.turn): # regele este in check
                    bad_moves.append(special_move[0])
                    continue
                else: # init pos for king not in check
                    move_line,move_column = special_move[0]
                    #now we go for the when we are in check along the way
                    if special_move[1] == "casteling-right": # checking right-castelling if we get checked along or checked after
                        new_game = temporary_game.make_copy()
                        new_game.board[f_line][f_col] = "--"
                        new_game.board[move_line][4] = self.turn_color[self.turn] + "K"
                        if new_game.simple_check_function(new_game.board,self.turn):
                            bad_moves.append(special_move[0])
                        else:
                            print("last check")
                            new_game = temporary_game.make_copy()
                            move_line,move_column = special_move[0]
                            #we make the second move, but special
                            new_game.special_moves_list = [special_move]
                            new_game.possible_basic_piece = [(move_line,move_column)]
                            new_game.make_second_selection(f_pos_tuple,(move_line,move_column))
                            if new_game.simple_check_function(new_game.board,1 - new_game.turn):
                                bad_moves.append((move_line,move_column))
                            else:
                                good_special_move.append((move_line,move_column))
                    if special_move[1] == "casteling-left": # cheking left- castelling if we get checked along
                        new_game = temporary_game.make_copy()
                        new_game.board[f_line][f_col] = "--"
                        new_game.board[move_line][2] = self.turn_color[self.turn] + "K"
                        if new_game.simple_check_function(new_game.board,self.turn):
                            bad_moves.append(special_move[0])
                        else:
                            new_game = temporary_game.make_copy()
                            move_line,move_column = special_move[0]
                            #we make the second move, but special
                            new_game.special_moves_list = [special_move]
                            new_game.possible_basic_piece = [(move_line,move_column)]
                            new_game.make_second_selection(f_pos_tuple,(move_line,move_column))
                            if new_game.simple_check_function(new_game.board,1 - new_game.turn):
                                bad_moves.append((move_line,move_column))
                            else:
                                good_special_move.append((move_line,move_column))
                    
            else: 
                new_game = temporary_game.make_copy()
                move_line,move_column = special_move[0]
                #we make the second move, but special
                new_game.special_moves_list = [special_move]
                new_game.possible_basic_piece = [(move_line,move_column)]
                new_game.make_second_selection(f_pos_tuple,(move_line,move_column))
                if new_game.simple_check_function(new_game.board,1 - new_game.turn):
                    bad_moves.append((move_line,move_column))
                else:
                    good_special_move.append((move_line,move_column))
        
        return (list(set(good_special_move + good_basic_move)),bad_moves)

    def check_mate_function(self):
        my_disponible_pieces = []
        for row in range(0,8):
            for col in range(0,8):
                if self.board[row][col][0]== self.turn_color[self.turn]:
                    my_disponible_pieces.append((row,col))
        for (p_line,p_col) in my_disponible_pieces:
            good,bad = self.check_good_positions((p_line,p_col))
            if len(good)!= 0:
                return False
        return True
                    
    # check_functions

    def basic_moves_finder(self):
        special_moves = set(map(lambda el : el[0:2],self.special_moves_list))
        return list(set(self.possible_current_moves) - special_moves)

    # used by search_for_possible_moves_zero_check

    def find_pos_colision_Oy_Ox(self, f_pos_tuple):
        f_row, f_col = f_pos_tuple
        # let's go up
        current_row = f_row - 1
        while current_row >= 0:
            if self.board[current_row][f_col] in self.possible_basic_piece[self.turn]:
                break
            if self.board[current_row][f_col] in self.possible_basic_piece[1 - self.turn]:
                self.possible_current_moves.append((current_row, f_col))
                break
            self.possible_current_moves.append((current_row, f_col))
            current_row -= 1
        # let's go down
        current_row = f_row + 1
        while current_row <= 7:
            if self.board[current_row][f_col] in self.possible_basic_piece[self.turn]:
                break
            if self.board[current_row][f_col] in self.possible_basic_piece[1 - self.turn]:
                self.possible_current_moves.append((current_row, f_col))
                break
            self.possible_current_moves.append((current_row, f_col))
            current_row += 1
        # let's go right
        current_col = f_col + 1
        while current_col <= 7:
            if self.board[f_row][current_col] in self.possible_basic_piece[self.turn]:
                break
            if self.board[f_row][current_col] in self.possible_basic_piece[1 - self.turn]:
                self.possible_current_moves.append((f_row, current_col))
                break
            self.possible_current_moves.append((f_row, current_col))
            current_col += 1
        # let's go left
        current_col = f_col - 1
        while current_col >= 0:
            if self.board[f_row][current_col] in self.possible_basic_piece[self.turn]:
                break
            if self.board[f_row][current_col] in self.possible_basic_piece[1 - self.turn]:
                self.possible_current_moves.append((f_row, current_col))
                break
            self.possible_current_moves.append((f_row, current_col))
            current_col -= 1
        # 0 mutari, atunci nu avem ce muta
        return len(self.possible_current_moves) != 0

    def find_pos_collision_diagonally(self, f_pos_tuple):
        f_row, f_col = f_pos_tuple
        # let's go right-top
        c_row, c_col = f_row - 1, f_col + 1
        while c_row >= 0 and c_col <= 7:
            if self.board[c_row][c_col] in self.possible_basic_piece[self.turn]:
                break
            if self.board[c_row][c_col] in self.possible_basic_piece[1 - self.turn]:
                self.possible_current_moves.append((c_row, c_col))
                break
            self.possible_current_moves.append((c_row, c_col))
            c_col += 1
            c_row -= 1
        # let's go left-bottom
        c_row, c_col = f_row + 1, f_col - 1
        while c_row <= 7 and c_col >= 0:
            if self.board[c_row][c_col] in self.possible_basic_piece[self.turn]:
                break
            if self.board[c_row][c_col] in self.possible_basic_piece[1 - self.turn]:
                self.possible_current_moves.append((c_row, c_col))
                break
            self.possible_current_moves.append((c_row, c_col))
            c_col -= 1
            c_row += 1
        # let's go left-top
        c_row, c_col = f_row - 1, f_col - 1
        while c_row >= 0 and c_col >= 0:
            if self.board[c_row][c_col] in self.possible_basic_piece[self.turn]:
                break
            if self.board[c_row][c_col] in self.possible_basic_piece[1 - self.turn]:
                self.possible_current_moves.append((c_row, c_col))
                break
            self.possible_current_moves.append((c_row, c_col))
            c_col -= 1
            c_row -= 1
        # let's go right-bottom
        c_row, c_col = f_row + 1, f_col + 1
        while c_row <= 7 and c_col <= 7:
            if self.board[c_row][c_col] in self.possible_basic_piece[self.turn]:
                break
            if self.board[c_row][c_col] in self.possible_basic_piece[1 - self.turn]:
                self.possible_current_moves.append((c_row, c_col))
                break
            self.possible_current_moves.append((c_row, c_col))
            c_col += 1
            c_row += 1
        return len(self.possible_current_moves) != 0

    def find_pos_basic_moves_pioneer(self, f_pos_tuple): #not special moves!
        f_row, f_col = f_pos_tuple
        # the white pioneer goes down
        if self.turn == 0:
            if f_row < 6:
                enemy_pieces = self.possible_basic_piece[1 - self.turn].copy()
                if self.board[f_row + 1][f_col] == "--":  # pos is free
                    self.possible_current_moves.append((f_row+1, f_col))
                # enemy can be taken right_bottom
                if f_col < 7 and self.board[f_row + 1][f_col + 1] in enemy_pieces:
                    self.possible_current_moves.append((f_row + 1, f_col + 1))
                # enemy can be taken left_bottom
                if f_col > 0 and self.board[f_row + 1][f_col - 1] in self.possible_basic_piece[1 - self.turn]:
                    self.possible_current_moves.append((f_row + 1, f_col - 1))
        else:
            # the black pionner goes up
            if f_row > 1:
                enemy_pieces = self.possible_basic_piece[1 - self.turn].copy()
                if self.board[f_row - 1][f_col] == "--":  # pos is free
                    self.possible_current_moves.append((f_row - 1, f_col))
                # enemy can be taken right_bottom
                if f_col < 7 and self.board[f_row - 1][f_col + 1] in enemy_pieces:
                    self.possible_current_moves.append((f_row - 1, f_col + 1))
                # enemy can be taken left_bottom
                if f_col > 0 and self.board[f_row - 1][f_col - 1] in enemy_pieces:
                    self.possible_current_moves.append((f_row - 1, f_col - 1))

        return len(self.possible_current_moves) != 0

    def find_pos_basic_moves_king(self, f_pos_tuple): # not special moves!
        f_row, f_col = f_pos_tuple
        for d_line in range(-1, 2):
            for d_column in range(-1, 2):
                if d_line == 0 and d_column == 0:
                    continue
                current_line = f_row + d_line
                current_col = f_col + d_column
                if 7 >= current_line >= 0 and 7 >= current_col >= 0:  # valid position
                    if self.board[current_line][current_col] == "--":
                        self.possible_current_moves.append(
                            (current_line, current_col))
                    if self.board[current_line][current_col][0] == self.turn_color[1 - self.turn]:
                        self.possible_current_moves.append(
                            (current_line, current_col))
        return len(self.possible_current_moves) != 0

    def find_pos_basic_moves_horse(self, f_pos_tuple): #not special moves!
        if self.turn == 0:
            who_moves = "w"
            who_stays = "b"
        else:
            who_moves = "b"
            who_stays = "w"
        f_row, f_col = f_pos_tuple
        moves_row = [-2, -1, 1, 2]
        moves_col = [-2, -1, 1, 2]
        d_row_col = [(d_row, d_col) for d_row in moves_row for d_col in moves_col if (
            abs(d_row) + abs(d_col)) == 3]  # possible differntial
        possible_row_col = [(f_row + d_r, f_col + d_c) for (d_r, d_c) in d_row_col if 7 >= (
            f_row + d_r) >= 0 and 7 >= (f_col + d_c) >= 0]  # possible raw moves
        possible_row_col = [(current_row, current_col) for (current_row, current_col) in possible_row_col if self.board[current_row]
                            [current_col] == "--" or self.board[current_row][current_col][0] == who_stays]
        self.possible_current_moves = possible_row_col
        return len(possible_row_col) != 0

    def find_special_moves(self, f_pos_tuple): # only the special moves
        # cases : king - castles , pioneer last pos, 2MovesPioneer
        pieces = self.possible_basic_piece[0] + self.possible_basic_piece[1]

        click_row,click_col = f_pos_tuple
        if self.board[click_row][click_col] not in ["wP","bP","wK","bK"]:
            return False
        piece_name = self.board[click_row][click_col]
        match piece_name[1]:
            case 'K':
                #!!!!WE HAVE TO VERIFY THAT THE King is not in check this time
                print('Castling case try ')
                left_castle,right_castle = self.casteling[self.turn]
                if not left_castle and not right_castle : # we can't make any casteling
                    return False
                if left_castle:
                    if self.board[click_row][click_col - 1] not in self.possible_basic_piece[0] + self.possible_basic_piece[1] and \
                       self.board[click_row][click_col - 2] not in self.possible_basic_piece[0] + self.possible_basic_piece[1]: # there's nobody between us
                        king_pos = (click_row,(click_col + 0)//2)
                        self.possible_current_moves.append(king_pos)
                        self.special_moves_list.append((king_pos,"casteling-left"))
                if right_castle:
                    if self.board[click_row][click_col + 1] not in self.possible_basic_piece[0] +self.possible_basic_piece[1] and \
                       self.board[click_row][click_col + 2] not in self.possible_basic_piece[0] +self.possible_basic_piece[1] and \
                       self.board[click_row][click_col + 3] not in self.possible_basic_piece[0] +self.possible_basic_piece[1]: # there's nobody between us
                        king_pos =  (click_row,(click_col + 7)//2)
                        self.possible_current_moves.append(king_pos)
                        self.special_moves_list.append((king_pos,"casteling-right"))
                if right_castle or left_castle:
                    return True
            case 'P':
                possible_special_moves = False
                if self.turn == 0 :
                    enemy_pieces = self.possible_basic_piece[1-self.turn].copy()
                    if click_row == 1 and self.board[click_row + 2][click_col] not in pieces and self.board[click_row + 1][click_col] not in pieces: # 2MoveWhite
                        print("2MovesPossibility")
                        move_2_pos_loc = (click_row + 2 , click_col)
                        self.possible_current_moves.append((move_2_pos_loc))
                        self.special_moves_list.append((move_2_pos_loc,"2MovesPossibility"))
                        possible_special_moves = True
                    #Enpassant case
                    if click_col > 0 and self.board[click_row + 1][click_col - 1] == "bENPASSANT":
                        move_enp_pos = (click_row + 1, click_col - 1)
                        self.possible_current_moves.append((move_enp_pos))
                        self.special_moves_list.append((move_enp_pos,"ENPASSANT"))
                        possible_special_moves = True
                    if click_col < 7 and self.board[click_row + 1][click_col + 1] == "bENPASSANT":
                        move_enp_pos = (click_row + 1, click_col + 1)
                        self.possible_current_moves.append((move_enp_pos))
                        self.special_moves_list.append((move_enp_pos,"ENPASSANT"))
                        possible_special_moves = True
                    if click_row == 6 : # Last position as a white
                        if self.board[7][click_col] not in pieces:
                            possible_special_moves = True
                            move_change_piece = (7,click_col)
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")
                        if click_col > 0 and self.board[7][click_col - 1] in enemy_pieces:
                            possible_special_moves = True
                            move_change_piece = (7,click_col -1 )
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")
                        if click_col < 7 and self.board[7][click_col + 1] in enemy_pieces:
                            possible_special_moves = True
                            move_change_piece = (7,click_col + 1 )
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")
                else:
                    enemy_pieces = self.possible_basic_piece[1-self.turn].copy()
                    if click_row == 6 and self.board[click_row - 2][click_col] not in pieces and self.board[click_row - 1][click_col] not in pieces: # 2Move
                        move_2_pos_loc = (click_row - 2 , click_col)
                        print("2MovesPossibility")
                        self.possible_current_moves.append((move_2_pos_loc))
                        self.special_moves_list.append((move_2_pos_loc,"2MovesPossibility"))
                        possible_special_moves = True
                    #Enpassant case
                    if click_col < 7 and self.board[click_row - 1][click_col + 1] == "wENPASSANT":
                        move_enp_pos = (click_row - 1, click_col + 1)
                        self.possible_current_moves.append((move_enp_pos))
                        self.special_moves_list.append((move_enp_pos,"ENPASSANT"))
                        possible_special_moves = True
                    if click_col > 0 and self.board[click_row - 1][click_col - 1] == "wENPASSANT":
                        move_enp_pos = (click_row - 1, click_col - 1)
                        self.possible_current_moves.append((move_enp_pos))
                        self.special_moves_list.append((move_enp_pos,"ENPASSANT"))
                        possible_special_moves = True
                    
                    if click_row == 1 : # last position black
                        if self.board[0][click_col] not in pieces:
                            possible_special_moves = True
                            move_change_piece = (0,click_col)
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")
                        if click_col > 0 and self.board[0][click_col - 1] in enemy_pieces:
                            possible_special_moves = True
                            move_change_piece = (0,click_col -1 )
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")
                        if click_col < 7 and self.board[0][click_col + 1] in enemy_pieces:
                            possible_special_moves = True
                            move_change_piece = (0,click_col + 1 )
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")

                return possible_special_moves
        
     # used by search_for_possible_moves_zero_check   all uses self.board

    def make_second_selection(self, f_pos_tuple, s_pos_tuple):  # here we come with the self.possible_moves made only! with good options, the special_moves also need to be formated
        # here we are going to validate the second click if is alright, at the moment returns true
        s_row, s_col = s_pos_tuple
        f_row, f_col = f_pos_tuple
        print(self.possible_current_moves)

        valid_click = (s_row, s_col) in self.possible_current_moves # aici sunt pozitiile fizic! Posibile, adica e neaparat bine
        if not valid_click:
            return # not a possible do able choice

        if self.special_move_handler(f_pos_tuple,s_pos_tuple) :
            return # we made a special move
        
        self.clean_enpassant_remains()
        self.recalculate_castelling_possibility(f_pos_tuple)
        self.board[s_row][s_col] = self.board[f_row][f_col]
        self.board[f_row][f_col] = "--"
        self.turn = 1 - self.turn

    def clean_enpassant_remains(self): # cleans the remains of Enpassant from the previous round
        print('Cleaning')
        for line in range(0,8):
            for column in range(0,8):
                if self.board[line][column][1:] == "ENPASSANT":
                    self.board[line][column] = "--" ## we clean it!

    def recalculate_castelling_possibility(self,f_pos_tuple): # reconsiders if the casteling is possible after a normal round! when castelling is being performed we its made in the special_case 
        f_row,f_col = f_pos_tuple
        #castelling case
        piece = self.board[f_row][f_col]
        match piece[1]:
            case "K":
                self.casteling[self.turn] = [False,False]
            case "C":
                if f_col == 0 :
                    self.casteling[self.turn][0] = False
                else:
                    self.casteling[self.turn][1] = False

    def special_move_handler(self,f_pos_tuple,s_pos_tuple): # if the player performs a special move, it makes it, otherwise lets the make_second_selection make the normal move
        s_row, s_col = s_pos_tuple
        f_row, f_col = f_pos_tuple
        made_special_move = False
        for tuple_special_move in self.special_moves_list:
            name = tuple_special_move[1] # we have the name
            row_move,col_move = tuple_special_move[0]
            if row_move == s_row and col_move == s_col : 
                made_special_move = True
                self.clean_enpassant_remains() # if we make a special move clean the enpassant!
                if name == "casteling-left":
                    king = self.board[f_row][f_col]
                    castle = self.board[row_move][0]
                    self.board[row_move][col_move] = king
                    self.board[f_row][f_col] = "--"
                    self.board[row_move][0] = "--"
                    self.board[row_move][col_move + 1] = castle
                    self.casteling[self.turn] = [False,False] # no more casteling
                elif name == "casteling-right":
                    king = self.board[f_row][f_col]
                    castle = self.board[row_move][7]
                    self.board[row_move][col_move] = king
                    self.board[f_row][f_col] = "--"
                    self.board[row_move][7] = "--"
                    self.board[row_move][col_move - 1] = castle
                    self.casteling[self.turn] = [False,False] # no more casteling
                elif name == "2MovesPossibility":
                    print('2 moves is happening')
                    pioneer = self.board[f_row][f_col]
                    self.board[f_row][f_col] = "--"
                    self.board[row_move][col_move] = pioneer
                    between_pos = (f_row + row_move)//2
                    self.board[between_pos][f_col] = self.turn_color[self.turn] + "ENPASSANT"
                elif name == "ENPASSANT":
                    print('Enpassant going on : ')
                    if self.turn == 0 :
                        pioneer = self.board[f_row][f_col]
                        self.board[row_move - 1][col_move] = "--"
                        self.board[row_move][col_move] = pioneer
                    else :
                        pioneer = self.board[f_row][f_col]
                        self.board[row_move + 1][col_move] = "--"
                        self.board[row_move][col_move] = pioneer
                    self.board[f_row][f_col] = "--"
                elif name == "CHANGE":
                    self.change_event_going_on = True
                    self.board[row_move][col_move] = self.board[f_row][f_col]
                    self.board[f_row][f_col] = "--"
                self.turn = 1 - self.turn
        return made_special_move
 
    # for the bot

    def get_all_possible_pieces_that_can_move(self): # for the current table returns all the pieces that can be moved
        pieces_available = []
        for row in range(0,8):
           for col in range(0,8):
               able_to_be_moved = len(self.check_good_positions((row,col))[0])!=0
               if self.board[row][col] in self.possible_basic_piece[self.turn] and able_to_be_moved:
                   pieces_available.append((row,col))
        return pieces_available

    def bot_move_handler(self): # we will be called only when is our turn
       pieces_able_to_be_moved = self.get_all_possible_pieces_that_can_move()
       print(pieces_able_to_be_moved)
       nr_pieces = len(pieces_able_to_be_moved)
       index_rand = random.randint(0,nr_pieces-1)
       selected_piece = pieces_able_to_be_moved[index_rand]
       print(selected_piece)
       
       self.search_for_possible_moves_zero_check(selected_piece) # now we update our self.poss and special
       good_moves,bad_moves = self.check_good_positions(selected_piece)
       self.possible_current_moves = good_moves
       
       nr_poss_moves = len(good_moves)
       index_rand = random.randint(0,nr_poss_moves-1)

       moved_pos = good_moves[index_rand]
       waiting_time = random.randint(0,4)
       time.sleep(waiting_time*0.25)
       self.make_second_selection(selected_piece,moved_pos)
       return moved_pos