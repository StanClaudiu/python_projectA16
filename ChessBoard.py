class backgroundBoard:
    def __init__(self):
        # pretty self explanatory I believe
        self.possible_basic_piece = [["wC", "wH", "wB", "wK", "wQ", "wP"], [
            "bC", "bH", "bB", "bK", "bQ", "bP"]]
        self.change_event_going_on = False
        self.possible_current_moves = []
        self.check_resulting_situations_for_me = []
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

    def find_pos_basic_moves_pioneer(self, f_pos_tuple): 
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

    def find_pos_basic_moves_king(self, f_pos_tuple):
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

    def find_pos_basic_moves_horse(self, f_pos_tuple):
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

    def find_special_moves(self, f_pos_tuple):
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
                    if self.board[click_row][click_col - 1] not in self.possible_basic_piece[0] +self.possible_basic_piece[1]: # there's nobody between us
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
                        if self.board[7][click_col - 1] in enemy_pieces:
                            possible_special_moves = True
                            move_change_piece = (7,click_col -1 )
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")
                        if self.board[7][click_col + 1] in enemy_pieces:
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
                        if self.board[0][click_col - 1] in enemy_pieces:
                            possible_special_moves = True
                            move_change_piece = (0,click_col -1 )
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")
                        if self.board[0][click_col + 1] in enemy_pieces:
                            possible_special_moves = True
                            move_change_piece = (0,click_col + 1 )
                            self.possible_current_moves.append(move_change_piece)
                            self.special_moves_list.append((move_change_piece,"CHANGE"))
                            print("We may change this piece")

                return possible_special_moves
        
       

    def clean_enpassant_remains(self):
        print('Cleaning')
        for line in range(0,8):
            for column in range(0,8):
                if self.board[line][column][1:] == "ENPASSANT":
                    self.board[line][column] = "--" ## we clean it!

    def recalculate_castelling_possibility(self,f_pos_tuple):
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


    def valid_first_selection(self, pos_tuple):
        # here we are going to validate the first click if is alright, at the moment returns true
        self.possible_current_moves = []
        self.special_moves_list = []
        (f_row, f_col) = pos_tuple
        valid_click = True  # we believe everything good
        valid_click = self.verify_good_turn_color(pos_tuple)
        valid_click = valid_click and self.verify_possible_move(pos_tuple)
        print("Primul click este valid : ", valid_click)

        #I will verify which cases are not good because they result in chess, I will still let the click so we can see it on the board
        if not valid_click :
            return valid_click
        else :
            # here I will verify the cases that result in check for me!

            return valid_click

    def special_move_handler(self,f_pos_tuple,s_pos_tuple):
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
 

    def make_second_selection(self, f_pos_tuple, s_pos_tuple):
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
            # a normal move

    # we will need to verify special situations
    def verify_possible_move(self, f_pos_tuple):
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

    def verify_good_turn_color(self, pos_tuple):
        row, col = pos_tuple
        if self.board[row][col] == "--":
            return False  # we first clicked a wrong pos
        if self.board[row][col][0] == "b" and self.turn == 0:
            return False  # you are white, pick white!
        if self.board[row][col][0] == "w" and self.turn == 1:
            return False  # you are white, pick white!
        return True
