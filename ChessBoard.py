class backgroundBoard:
    def __init__(self):
        #pretty self explanatory I believe
        self.possible_current_moves = []
        self.board = [["wC","wH","wB","wK","wQ","wB","wH","wC"],
                      ["wP","wP","wP","wP","wP","wP","wP","wP"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["--","--","--","--","--","--","--","--"],
                      ["bP","bP","bP","bP","bP","bP","bP","bP"],
                      ["bC","bH","bB","bK","bQ","bB","bH","bC"]]
        self.turn = 0 # meaning first one, easy to to 1-self.turn
    stack_all_transformations = list()

    def find_pos_colision_Oy_Ox(self,f_pos_tuple):
            if self.turn == 0 :
                who_moves = "w"
                who_stays = "b"
            else :
                who_moves = "b"
                who_stays = "w"
            f_row,f_col = f_pos_tuple
            print(f_row,f_col)
            # let's go up
            current_row = f_row -1
            while current_row >= 0 :
                if self.board[current_row][f_col][0] == who_moves:
                    break
                if self.board[current_row][f_col][0] == who_stays:
                    self.possible_current_moves.append((current_row,f_col))
                    break
                self.possible_current_moves.append((current_row,f_col))
                current_row -= 1
            # let's go down
            current_row = f_row +1
            while current_row <= 7 :
                if self.board[current_row][f_col][0] == who_moves:
                    break
                if self.board[current_row][f_col][0] == who_stays:
                    self.possible_current_moves.append((current_row,f_col))    
                    break
                self.possible_current_moves.append((current_row,f_col))
                current_row += 1
            # let's go right
            current_col = f_col + 1
            while current_col <= 7 :
                if self.board[f_row][current_col][0] == who_moves:
                    break
                if self.board[f_row][current_col][0] == who_stays:
                    self.possible_current_moves.append((f_row,current_col))
                    break
                self.possible_current_moves.append((f_row,current_col))
                current_col += 1
            # let's go left
            current_col = f_col - 1
            while current_col >= 0 :
                if self.board[f_row][current_col][0] == who_moves:
                    break
                if self.board[f_row][current_col][0] == who_stays:
                    self.possible_current_moves.append((f_row,current_col))
                    break
                self.possible_current_moves.append((f_row,current_col))
                current_col -= 1
            return len(self.possible_current_moves)!=0 # 0 mutari, atunci nu avem ce muta
   
    def find_pos_collision_diagonally(self,f_pos_tuple):
        if self.turn == 0 :
                who_moves = "w"
                who_stays = "b"
        else :
                who_moves = "b"
                who_stays = "w"
        f_row,f_col = f_pos_tuple  
        # let's go right-top
        c_row,c_col = f_row - 1,f_col + 1
        print(self.board[c_row][c_col])
        while c_row >=0 and c_col <=7 :
            if self.board[c_row][c_col][0] == who_moves :
                break
            if self.board[c_row][c_col][0] == who_stays :
                print("Hit")
                self.possible_current_moves.append((c_row,c_col))
                break
            self.possible_current_moves.append((c_row,c_col))
            c_col += 1
            c_row -= 1
        # let's go left-bottom
        c_row,c_col = f_row + 1,f_col - 1
        while c_row <=7 and c_col >=0 :
            if self.board[c_row][c_col][0] == who_moves :
                break
            if self.board[c_row][c_col][0] == who_stays :
                self.possible_current_moves.append((c_row,c_col))
                break
            self.possible_current_moves.append((c_row,c_col))
            c_col -= 1
            c_row += 1
        # let's go left-top
        c_row,c_col = f_row - 1,f_col - 1
        while c_row >=0 and c_col >= 0 :
            if self.board[c_row][c_col][0] == who_moves :
                break
            if self.board[c_row][c_col][0] == who_stays :
                self.possible_current_moves.append((c_row,c_col))    
                break
            self.possible_current_moves.append((c_row,c_col))
            c_col -= 1
            c_row -= 1
        # let's go right-bottom
        c_row,c_col = f_row + 1,f_col + 1
        while c_row <=7 and c_col <= 7 :
            if self.board[c_row][c_col][0] == who_moves :
                break
            if self.board[c_row][c_col][0] == who_stays :
                self.possible_current_moves.append((c_row,c_col))
                break
            self.possible_current_moves.append((c_row,c_col))
            c_col += 1
            c_row += 1
        return len(self.possible_current_moves) != 0
            
    def find_pos_basic_moves_pioneer(self,f_pos_tuple):
        f_row,f_col = f_pos_tuple
        if self.turn == 0 :
            who_moves = "w"
            who_stays = "b"
        else :
            who_moves = "b"
            who_stays = "w"

        # the white pioneer goes down
        if who_moves == "w" :
            if f_row < 7:
                if  self.board[f_row + 1][f_col] == "--": #pos is free
                    self.possible_current_moves.append((f_row+1,f_col))
                if f_col < 7 and self.board[f_row + 1][f_col + 1][0] == who_stays: # enemy can be taken right_bottom
                    self.possible_current_moves.append((f_row +1 , f_col + 1))
                if f_col > 0 and self.board[f_row + 1][f_col - 1][0] == who_stays: # enemy can be taken left_bottom
                    self.possible_current_moves.append((f_row +1 , f_col -1 ))
        else:
        # the black pionner goes up
            if f_row > 0 :
                if self.board[f_row -1][f_col] == "--": #pos is free
                    self.possible_current_moves.append((f_row - 1,f_col))
                if f_col < 7 and self.board[f_row - 1][f_col + 1][0] == who_stays: # enemy can be taken right_bottom
                    self.possible_current_moves.append((f_row - 1 , f_col + 1))
                if f_col > 0 and self.board[f_row -1][f_col - 1][0] == who_stays: # enemy can be taken left_bottom
                    self.possible_current_moves.append((f_row - 1 , f_col -1 ))

        return len(self.board)!=0
        
    def find_pos_basic_moves_king(self,f_pos_tuple):
        if self.turn == 0 :
            who_moves = "w"
            who_stays = "b"
        else :
            who_moves = "b"
            who_stays = "w"
        f_row,f_col = f_pos_tuple
        for d_line in range(-1,2):
            for d_column in range(-1,2):
                if d_line == 0 and d_column == 0 :
                    continue
                current_line = f_row + d_line
                current_col = f_col + d_column
                if 7>= current_line >= 0 and 7>= current_col >= 0 : # valid position
                    if self.board[current_line][current_col] == "--":
                        self.possible_current_moves.append((current_line,current_col))
                    if self.board[current_line][current_col][0] == who_stays:
                        self.possible_current_moves.append((current_line,current_col))
        return len(self.possible_current_moves)!=0
    
    def find_pos_basic_moves_horse(self,f_pos_tuple):
        if self.turn == 0 :
            who_moves = "w"
            who_stays = "b"
        else :
            who_moves = "b"
            who_stays = "w"
        f_row,f_col = f_pos_tuple
        moves_row = [-2,-1,1,2]
        moves_col = [-2,-1,1,2]
        d_row_col = [(d_row,d_col) for d_row in moves_row for d_col in moves_col if (abs(d_row) + abs(d_col)) == 3] # possible differntial
        possible_row_col = [(f_row + d_r,f_col +d_c) for (d_r,d_c) in d_row_col if 7>=(f_row + d_r) >= 0 and 7>=(f_col +d_c) >=0]  #possible raw moves
        possible_row_col = [(current_row,current_col) for (current_row,current_col) in possible_row_col if self.board[current_row][current_col] == "--" or self.board[current_row][current_col][0] == who_stays]
        print(possible_row_col) 
        self.possible_current_moves = possible_row_col
        return len(possible_row_col)!=0

        
        
        

    def valid_first_selection(self,pos_tuple):
        #here we are going to validate the first click if is alright, at the moment returns true
        self.possible_current_moves = []
        (f_row,f_col) = pos_tuple
        valid_click = True # we believe everything good
        valid_click = self.verify_good_turn_color(pos_tuple) 
        valid_click = valid_click and self.verify_possible_move(pos_tuple)
        print("Primul click este valid : ",valid_click)
        return valid_click
    
    def valid_second_selection(self,f_pos_tuple,s_pos_tuple):
        #here we are going to validate the second click if is alright, at the moment returns true
        s_row,s_col = s_pos_tuple
        f_row,f_col = f_pos_tuple
        valid_click = True

        #is the now pos good?, wihthout veryfing the chess condition

        valid_click = (s_row,s_col) in self.possible_current_moves

        if valid_click:
            self.board[s_row][s_col] = self.board[f_row][f_col]
            self.board[f_row][f_col] = "--"
            self.turn = 1 - self.turn

    def verify_possible_move(self,f_pos_tuple): # we will need to verify special situations
        f_row,f_col = f_pos_tuple
        piece_to_move = self.board[f_row][f_col]
        valid_move = True
        if self.turn == 0 :
            who_moves = "w"
        else :
            who_moves = "b"

        match piece_to_move[1]:
            case "K":
                print("King -------------- ")
                valid_move = self.find_pos_basic_moves_king(f_pos_tuple)
                if valid_move:
                    print("King can move : ",self.possible_current_moves)
            case "Q":
                print("Queen -----------")
                valid_moves_Ox_Oy = self.find_pos_colision_Oy_Ox(f_pos_tuple)
                valid_moves_diagonally = self.find_pos_collision_diagonally(f_pos_tuple)
                valid_move = valid_moves_Ox_Oy or valid_moves_diagonally
                if valid_move :
                    print("I can make the following moves : ",self.possible_current_moves)
            case "P":
                print("Pioneer")
                valid_move_ = self.find_pos_basic_moves_pioneer(f_pos_tuple)
            case "C":
                print("Castle ---------")
                valid_moves_Ox_Oy = self.find_pos_colision_Oy_Ox(f_pos_tuple)
                valid_move = valid_moves_Ox_Oy
                if valid_move:
                    print("the moves : ",self.possible_current_moves)
            case "B":
                print("Bishop")
                valid_moves_diagonally = self.find_pos_collision_diagonally(f_pos_tuple)
                valid_move = valid_moves_diagonally
                if valid_move:
                    print("the moves : ",self.possible_current_moves)
            case "H":
                print("Horse")
                valid_moves_basic = self.find_pos_basic_moves_horse(f_pos_tuple)
        return valid_move

    def verify_good_turn_color(self,pos_tuple):
        row,col = pos_tuple
        if self.board[row][col] == "--":
            return False # we first clicked a wrong pos
        if self.board[row][col][0] == "b" and self.turn == 0 :
            return False # you are white, pick white!
        if self.board[row][col][0] == "w" and self.turn == 1 :
            return False # you are white, pick white!
        return True
        

                    