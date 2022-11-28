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
            self.image_piece[piece] = pygame.transform.scale(self.image_piece[piece], (self.l_SQUARE, self.h_SQUARE))
        pygame.display.set_caption('Chess Game')
        self.clock = pygame.time.Clock()

    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
            self.draw_table()
            self.draw_pieces()
            pygame.display.update()

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
        for row in range(0,8):
            for col in range(0,8):
                if self.table.board[col][row] != "--":
                    self.screen.blit(self.image_piece[self.table.board[col][row]],(row * self.l_SQUARE, col * self.h_SQUARE))
                    

def main():
    print("Here we are going to try to make this bullshit")
    game = GUIChessGame(600, 600)
    game.start_game()


if __name__ == "__main__":
    main()
