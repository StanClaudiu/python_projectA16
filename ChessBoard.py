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
        while c_row >=0 and c_col <=7 :
            if self.board[c_row][c_col][0] == who_moves :
                break
            if self.board[c_row][c_col][0] == who_stays :
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
                all_the_same = True
                for d_row in range(-1,2):
                    print(d_row)
                    for d_col in range(-1,2):
                       neigh_row = f_row + d_row
                       neigh_col = f_col + d_col
                       if neigh_row >=0 and neigh_col >=0:
                         if self.board[neigh_row][neigh_col][0] != who_moves: # possible moves
                             self.possible_current_moves.append((neigh_row,neigh_col))
                             all_the_same = False
                valid_move = not all_the_same
            case "Q":
                print("Queen -----------")
                valid_move = self.find_pos_colision_Oy_Ox((f_row,f_col)) or self.find_pos_collision_diagonally((f_row,f_col)) # let's see if we can move the queen
                if valid_move :
                    print("I can make the following moves : ",self.possible_current_moves)
            case "P":
                print("Pioneer")
            case "C":
                print("Castle")
            case "B":
                print("Bishop")
            case "H":
                print("Horse")
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
        

                    