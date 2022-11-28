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

                    