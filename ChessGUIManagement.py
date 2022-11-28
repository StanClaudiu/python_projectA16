import pygame
from sys import exit
import ChessBoard

class GUIChessGame:
    def  __init__(self,l_pixels,h_pixels):
       self.table = ChessBoard.backgroundBoard()
       self.pieces = pieces = ("wC","wH","wB","wK","wQ","wP","bC","bH","bB","bK","bQ","bP")
       pygame.init() # dam o cheie
       self.screen = pygame.display.set_mode((l_pixels,h_pixels))
       self.image_piece = dict()
       for piece in pieces:
           self.image_piece[piece] = pygame.image.load("ChessPieces/" + piece + ".png").convert_alpha()
       pygame.display.set_caption('Chess Game')
       self.clock = pygame.time.Clock()

    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT :
                    pygame.quit()
                    exit()
            pygame.display.update()

def main():
    print("Here we are going to try to make this bullshit")
    game = GUIChessGame(800,600)
    game.start_game()




if __name__ == "__main__":
    main()
   




