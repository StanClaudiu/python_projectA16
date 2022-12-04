import pygame
from sys import exit,argv
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

    def get_type(self): # gets the type of game that we want to play
        print('Getting game type')
        assert len(argv) == 2 and argv[1] in ["human","bot"]
        self.type_of_game = argv[1]

    def start_game(self): # start the game, selecting pvp or pvb
        if self.type_of_game == "human":
            self.start_game_human()
        else :
            self.start_game_bot()

    def start_game_bot(self): # start the game against a bot
        print('Against a bot')
        self.handle_get_wanted_color()
        first_time = True
        while True:
            if not first_time : # first time just make the table
                locked = True
                check_mate_flag = self.table.check_mate_function() # calculate once for a move
                if check_mate_flag:
                        self.finish_game_handler()
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

    def start_game_human(self): # starts the game, it firstly paints the board and after waits for instr from players
        first_time = True
        while True:
            if not first_time : # first time just make the table
                locked = True
                check_mate_flag = self.table.check_mate_function() # calculate once for a move
                if check_mate_flag:
                        self.finish_game_handler()
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

    def handle_get_wanted_color(self): # get the color that the player wants
        alpha_factor = 0.8
        length_winning_panel = self.l_pixels * alpha_factor
        height_winning_panel = self.h_pixels * alpha_factor

        left_right_padding = (1 - alpha_factor) / 2 * length_winning_panel
        up_down_padding = (1 - alpha_factor) /2  * height_winning_panel

        queen_length = (length_winning_panel//3)
        queen_height = (height_winning_panel//3)

        font_render = pygame.font.Font(None,50)
        text_surface = font_render.render('Choose the color you want : ',False,(255,255,255))

        image_black = pygame.transform.smoothscale(self.image_piece["bQ"],(queen_length,queen_height))
        image_white = pygame.transform.smoothscale(self.image_piece["wQ"],(queen_length,queen_height))

        space_between = length_winning_panel * 0.1
        pos_white_queen_ox = ((length_winning_panel - space_between) - 2 * queen_length) //2

        pos_black_queen_ox = ((length_winning_panel - space_between) - 2 * queen_length) //2 + space_between + queen_length

        pos_queens_oy = 200


        surface = pygame.Surface((length_winning_panel,height_winning_panel))
        surface.fill((170,170,170))

        surface.blit(text_surface,pygame.Rect(10,0,length_winning_panel,height_winning_panel))
        surface.blit(image_white,(pos_white_queen_ox,pos_queens_oy))
        surface.blit(image_black,(pos_black_queen_ox,pos_queens_oy))

        self.screen.blit(surface,(left_right_padding,up_down_padding))

        pygame.display.update()
        
        locked = True
        while locked:
             for event_second in pygame.event.get():
                    if event_second.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    if event_second.type == pygame.MOUSEBUTTONDOWN:
                            pos_x,pos_y = event_second.pos
                            print(pos_x,pos_y)
                            white_square_top_left = (pos_white_queen_ox + left_right_padding,up_down_padding + pos_queens_oy)
                            white_square_bottom_right = (pos_white_queen_ox + left_right_padding + queen_length,up_down_padding + pos_queens_oy + queen_height)

                            if  white_square_bottom_right[0]>=pos_x>=white_square_top_left[0] and  white_square_bottom_right[1] >= pos_y >=  white_square_top_left[1]:
                                locked = False
                                print("White queen hit!!")
                                self.color_player = "w"

                            black_square_top_left = (white_square_top_left[0] + queen_length + space_between,white_square_top_left[1])
                            black_square_bottom_right = (black_square_top_left[0] + queen_length,white_square_bottom_right[1])

                            if black_square_bottom_right[0]>= pos_x >= black_square_top_left[0] and black_square_bottom_right[1] >= pos_y >= black_square_top_left[1]:
                                locked = False
                                print("Black queen hit!!")
                                self.color_player = "b"

    def finish_game_handler(self): # This function will say who won, and after a click will close the program
        # let's make the table
        alpha_factor = 0.8
        length_winning_panel = self.l_pixels * alpha_factor
        height_winning_panel = self.h_pixels * alpha_factor

        left_right_padding = (1 - alpha_factor) / 2 * length_winning_panel
        up_down_padding = (1 - alpha_factor) /2  * height_winning_panel

        print('The game is done ')

        font_render = pygame.font.Font(None,50)



        if self.table.turn == 0:
            text_surface = font_render.render('The winner is : black!',False,(0,0,0))
            image = pygame.transform.smoothscale(self.image_piece["bQ"],(length_winning_panel//3,height_winning_panel//3))
            image.fill((255, 255, 255, 255), None, pygame.BLEND_RGBA_MULT)
        else:
            text_surface = font_render.render('The winner is : white!',False,(0,0,0))
            image = pygame.transform.smoothscale(self.image_piece["wQ"],(length_winning_panel//3,height_winning_panel//3))
            image.fill((255, 255, 255, 255), None, pygame.BLEND_RGBA_MULT)

        surface = pygame.Surface((length_winning_panel,height_winning_panel))
        surface.fill((255,255,255))
        surface.blit(text_surface,pygame.Rect(left_right_padding,up_down_padding,length_winning_panel,height_winning_panel))
        surface.set_alpha(220)
        self.screen.blit(surface,pygame.Rect(left_right_padding,up_down_padding,length_winning_panel,height_winning_panel))
        self.screen.blit(image,(self.l_pixels /2 - length_winning_panel//6,height_winning_panel//3))
        pygame.display.update()
        while True:
             for event_second in pygame.event.get():
                    if event_second.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                    if event_second.type == pygame.MOUSEBUTTONDOWN:
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
    game = GUIChessGame(600, 600)
    game.get_type()
    game.start_game()


if __name__ == "__main__":
    main()

    
