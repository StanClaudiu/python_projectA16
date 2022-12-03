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

    def start_game(self): # starts the game, it firstly paints the board and after waits for instr from players
        first_time = True
        while True:
            if not first_time :
                locked = True
                while locked : 
                    if self.table.check_mate_flag:
                        self.finish_game_handler()
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

    def handle_click(self,event): #handles the interaction after the first click
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
                        if self.table.change_event_going_on:
                           self.handle_change_event((s_row,s_col))
                        locked = False
                self.draw_positions_available()
                pygame.display.update()

    def finish_game_handler(self): # This function will say who won, and after a click will close the program
        
        pygame.quit()
        exit()

#used by handle_click

    def validate_first_click(self,coords): # sees if the first click has zero_check possible moves
        f_row,f_col = coords
        print("We have the Square : (",f_row,",",f_col,")")
        if self.table.valid_first_selection((f_row,f_col)):
            return True
    
    def validate_second_click(self,coords,coords_2): # makes/ not makes the changes to the table accordingly after the second click
        f_row,f_col = coords
        print("We have the Square : (",f_row,",",f_col,")")
        self.table.make_second_selection((f_row,f_col),coords_2)

    def draw_table(self): # draw white and black squares, red for when in check
        for row in range(0, 8):
            for col in range(0, 8):
                square_table = pygame.Surface((self.l_SQUARE, self.h_SQUARE))
                if (row + col) % 2 == 0:
                    square_table.fill('white')
                else:
                    square_table.fill('gray')
                self.screen.blit(square_table, (row*self.l_SQUARE, col*self.h_SQUARE))
        if self.table.simple_check_function(self.table.board,self.table.turn):
            king_row,king_col = self.table.find_my_king(self.table.turn)
            square_table = pygame.Surface((self.l_SQUARE, self.h_SQUARE))
            square_table.fill('red')
            self.screen.blit(square_table, (king_row*self.l_SQUARE, king_col*self.h_SQUARE))

            
    
    def draw_pieces(self): # draws only the pieces, mendatory after draw_table
        pieces = self.table.possible_basic_piece[0] + self.table.possible_basic_piece[1]
        for col in range(0,8):
            for row in range(0,8):
                if self.table.board[row][col] in pieces:
                    self.screen.blit(self.image_piece[self.table.board[row][col]],(col * self.l_SQUARE, row * self.h_SQUARE))

    def draw_positions_available(self): # used to draw the available positions, will be refactor to do much more with the not wanted pos
        for (row,column) in self.table.possible_current_moves:
            x_coordinate = self.l_SQUARE * (column + 1/2)
            y_coordinate = self.h_SQUARE * (row + 1/2)
            pygame.draw.circle(self.screen,'blue',(x_coordinate,y_coordinate),self.l_SQUARE//7)
        for (row,column) in self.table.bad_moves:
            x_coordinate = self.l_SQUARE * (column + 1/2)
            y_coordinate = self.h_SQUARE * (row + 1/2)
            pygame.draw.circle(self.screen,'red',(x_coordinate,y_coordinate),self.l_SQUARE//7)

    def handle_change_event(self,final_pos): # interface for selecting a Queen/Horse etc 
        print('We have a special change event')
        actual_turn = 1 - self.table.turn
        self.table.change_event_going_on = False # I will manage it right now
        minimize_rate = 0.8
        left_padding = 4 *  (1 - minimize_rate) * self.l_SQUARE
        l_modified_square = 2 * minimize_rate * self.l_SQUARE
        h_modified_square = 2 * minimize_rate * self.h_SQUARE
        #show choices in here:
        piece_choices = []
        if actual_turn == 1:
            piece_choices = ['bQ','bH','bB','bC']
            top_padding = self.h_pixels - self.h_SQUARE * 2 - h_modified_square
        else:
            piece_choices = ['wQ','wH','wB','wC']
            top_padding = self.h_SQUARE * 2 
        for index,piece_choice in enumerate(piece_choices):
            image = pygame.transform.scale(self.image_piece[piece_choice],(l_modified_square,h_modified_square))
            image.fill((255, 255, 255, 126), None, pygame.BLEND_RGBA_MULT)
            position_image = (left_padding + l_modified_square * index,top_padding)
            self.screen.blit(image,position_image)
        pygame.display.update()
        locked = True
        print("Entered here")
        while locked :
            for event_selection in pygame.event.get():
                if event_selection.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event_selection.type == pygame.MOUSEBUTTONDOWN :
                    print("We got a click")
                    #now let's see what he chose
                    coord_x,coord_y = event_selection.pos
                    for index,piece_choice in enumerate(piece_choices):
                        left_limit = left_padding + index * l_modified_square
                        right_limit = left_limit + l_modified_square
                        bottom_limit = top_padding + h_modified_square
                        top_limit = top_padding
                        if left_limit <= coord_x <= right_limit and top_limit <= coord_y <= bottom_limit:
                            self.table.board[final_pos[0]][final_pos[1]] = piece_choice
                            locked = False
                            break
                            
    def get_click_coords(self,event): # get the click coords
        return event.pos[1] // self.l_SQUARE,event.pos[0] // self.h_SQUARE

#used by handle_click


############
############
############
############
            

def main():
    print("Here we are going to try to make this bullshit")
    game = GUIChessGame(600, 600)
    game.start_game()


if __name__ == "__main__":
    main()

    
