import pygame
import sys
from bird import Bird
from pipe import Pipe

class Game:
    def __init__(self):
        self.screen_w = 1600
        self.screen_h = 1000
        #set up display: input is tuple of (width, height)
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.bg = pygame.image.load("background.jpg").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1600, 1000))

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 50)

        self.duration = 30
        self.state = "START"
        self.high_score = 0
        self.score = 0
        
        self.bird = Bird((255, 255, 0), 70)
        self.pipes = []

        self.PIPE_SPAWN = pygame.USEREVENT + 1      # cusotm event PIPE_SPAWN
        pygame.time.set_timer(self.PIPE_SPAWN, 1500)

    def reset_game(self):
        self.bird = Bird((255, 255, 0), 70)
        self.pipes = []
        self.score = 0
        self.state = "PLAY"

    def handle_events(self):

        #event is a object- params: eventtype, pump(clear queue), exlude) returns List
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if self.state == "START" and event.key == pygame.K_s:
                    self.state = "PLAY"
                
                elif self.state == "PLAY" and event.key == pygame.K_SPACE:
                    self.bird.jumpUp()
                
                elif self.state == "END" and event.key == pygame.K_r:
                    self.reset_game()

            if event.type == self.PIPE_SPAWN and self.state == "PLAY":
                self.pipes.append(Pipe(self.screen_w, self.screen_h))

    def update(self):
        if self.state == "PLAY":
            self.bird.update()

            for pipe in self.pipes[:]:
                pipe.move()
                if not pipe.passed and pipe.scr_w < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                if pipe.scr_w + pipe.w < 0:
                    self.pipes.remove(pipe)

            if self.bird.y > self.screen_h or self.bird.y < 0 or any(pipe.hasCollided(self.bird) for pipe in self.pipes):
                self.state = "END"
                if self.score > self.high_score:
                    self.high_score = self.score

    def draw(self):
        self.screen.fill((113, 197, 207))
        self.screen.blit(self.bg, (0, 0))
        if self.state == "START":
            start_txt = self.font.render("Press 'S' to Start!", True, (255, 255, 255))
            self.screen.blit(start_txt, (self.screen_w // 2 - 100, self.screen_h // 2))

        elif self.state == "PLAY":
            self.bird.draw(self.screen)
            for pipe in self.pipes:
                pipe.draw(self.screen)

            # Draw HUD score overlay
            score_txt = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_txt, (10, 10))

        elif self.state == "END":
            # Draw game over screens
            over_txt = self.large_font.render("GAME OVER", True, (255, 0, 0))
            score_txt = self.font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            high_txt = self.font.render(f"High Score: {self.high_score}", True, (0, 255, 0))
            retry_txt = self.font.render("Press 'R' to Restart", True, (255, 255, 255))

            self.screen.blit(over_txt, (self.screen_w // 2 - 110, self.screen_h // 2 - 80))
            self.screen.blit(score_txt, (self.screen_w // 2 - 80, self.screen_h // 2 - 10))
            self.screen.blit(high_txt, (self.screen_w // 2 - 80, self.screen_h // 2 + 30))
            self.screen.blit(retry_txt, (self.screen_w // 2 - 110, self.screen_h // 2 + 90))

        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
