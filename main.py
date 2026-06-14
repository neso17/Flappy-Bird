import time

from game import Game

if __name__ == "__main__":
    flappy_game = Game()
    time.sleep(1)  # Allow camera to initialize
    flappy_game.run()



# A Surface is a pixel canvas used to draw shapes, hold sprites, and handle transparency.