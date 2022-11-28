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


    def valid_first_selection(self,pos_tuple):
        #here we are going to validate the first click if is alright, at the moment returns true
        self.possible_current_moves = []
        (f_row,f_col) = pos_tuple
        valid_click = True # we believe everything good
        valid_click = self.verify_good_turn_color(pos_tuple) 
        valid_click = self.verify_possible_move(pos_tuple)
        print(valid_click)
        return valid_click
    
    def valid_second_selection(self,f_pos_tuple,s_pos_tuple):
        #here we are going to validate the second click if is alright, at the moment returns true
        s_row,s_col = s_pos_tuple
        f_row,f_col = f_pos_tuple
        valid_click = True

        if valid_click:
            print("I did smth")
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
                print("King")
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
                print("Queen")
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
        

                    