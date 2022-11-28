class backgroundBoard:
    def __init__(self):
        #pretty self explanatory I believe
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
        (x_coord,y_coord) = pos_tuple
        valid_click = True
        return valid_click
    
    def valid_second_selection(self,pos_tuple):
        #here we are going to validate the second click if is alright, at the moment returns true
        (x_coord,y_coord) = pos_tuple
        valid_click = True

    def verify_good_turn_color(self,pos_tuple):
        row,col = pos_tuple
        if self.board[row][col] == "--":
            return False # we first clicked a wrong pos
        

                    