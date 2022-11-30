import pygame
from sys import exit
import ChessBoard


class GUIChessGame:
    def __init__(self, l_pixels, h_pixels):
        self.table = ChessBoard.backgroundBoard()
        self.pieces = pieces = ("wC", "wH", "wB", "wK",
                                "wQ", "wP", "bC", "bH", "bB", "bK", "bQ", "bP")
        pygame.init()  # dam o cheie
        self.l_pixels = l_pixels
        self.h_pixels = h_pixels
        self.l_SQUARE = l_pixels // 8
        self.h_SQUARE = h_pixels // 8
        self.screen = pygame.display.set_mode((l_pixels, h_pixels))
        self.image_piece = dict()
        for piece in pieces:
            self.image_piece[piece] = pygame.image.load(
                "ChessPieces/" + piece + ".png").convert_alpha()
            self.image_piece[piece] = pygame.transform.smoothscale(self.image_piece[piece], (self.l_SQUARE, self.h_SQUARE))
        pygame.display.set_caption('Chess Game')
        self.clock = pygame.time.Clock()

    def start_game(self):
        first_time = True
        while True:
            if not first_time :
                locked = True
                while locked : 
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.handle_click(event)
                            locked = False
            
            self.draw_table()
            self.draw_pieces()
            print("Ajung sa redesenez")
            pygame.display.update()
            first_time = False
           

    def draw_table(self):
        for row in range(0, 8):
            for col in range(0, 8):
                square_table = pygame.Surface((self.l_SQUARE, self.h_SQUARE))
                if (row + col) % 2 == 0:
                    square_table.fill('white')
                else:
                    square_table.fill('gray')
                self.screen.blit(square_table, (row*self.l_SQUARE, col*self.h_SQUARE))
    
    def draw_pieces(self):
        pieces = self.table.possible_basic_piece[0] + self.table.possible_basic_piece[1]
        for col in range(0,8):
            for row in range(0,8):
                if self.table.board[row][col] in pieces:
                    self.screen.blit(self.image_piece[self.table.board[row][col]],(col * self.l_SQUARE, row * self.h_SQUARE))

    def draw_positions_available(self):
        for (row,column) in self.table.possible_current_moves:
            x_coordinate = self.l_SQUARE * (column + 1/2)
            y_coordinate = self.h_SQUARE * (row + 1/2)
            pygame.draw.circle(self.screen,'blue',(x_coordinate,y_coordinate),self.l_SQUARE//7)

    def handle_click(self,event):
        print("THE FIRST CLICK : ")
        f_row,f_col = self.get_click_coords(event)
        if self.validate_first_click((f_row,f_col)): # I can make the second choice if the first one was good
            locked = True
            while locked :
                for event_second in pygame.event.get():
                    if event_second.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    if event_second.type == pygame.MOUSEBUTTONDOWN:
                        print("THE SECOND CLICK")
                        s_row,s_col = self.get_click_coords(event_second)
                        self.validate_second_click((f_row,f_col),(s_row,s_col)) # modify the table
                        locked = False
                self.draw_positions_available()
                pygame.display.update()
    
    def validate_first_click(self,coords):
        f_row,f_col = coords
        print("We have the Square : (",f_row,",",f_col,")")
        if self.table.valid_first_selection((f_row,f_col)):
            return True
    
    # if is good modify the table, otherwise no
    def validate_second_click(self,coords,coords_2):
        f_row,f_col = coords
        print("We have the Square : (",f_row,",",f_col,")")
        self.table.valid_second_selection((f_row,f_col),coords_2)

    def get_click_coords(self,event):
        return event.pos[1] // self.l_SQUARE,event.pos[0] // self.h_SQUARE



            

def main():
    print("Here we are going to try to make this bullshit")
    game = GUIChessGame(600, 600)
    game.start_game()


if __name__ == "__main__":
    main()

    
