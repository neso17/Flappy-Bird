import pygame
import sys
from bird import Bird
from pipe import Pipe
from camera import Camera

class Game:
    def __init__(self):
        self.screen_w = 1600
        self.screen_h = 1000
        #set up display: input is tuple of (width, height)
        self.screen = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.camera = Camera(self.screen_w, self.screen_h)

        self.bg = pygame.image.load("background.jpg").convert_alpha()
        self.bg = pygame.transform.scale(self.bg, (1600, 1000))

        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 50)

        self.duration = 30
        self.state = "START"
        self.high_score = 0
        self.score = 0
        
        self.bird = Bird((255, 255, 0), 55)
        self.pipes = []

        self.PIPE_SPAWN = pygame.USEREVENT + 1      # cusotm event PIPE_SPAWN
        pygame.time.set_timer(self.PIPE_SPAWN, 2500)

    def reset_game(self):
        self.bird = Bird((255, 255, 0), 55)
        self.pipes = []
        self.score = 0
        self.state = "PLAY"

    def handle_events(self):

        #event is a object- params: eventtype, pump(clear queue), exlude) returns List
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.camera.release()
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

    # Add a variable to track the background inside __init__
    # self.current_bg = None
    # self.pipe_spawn_timer = 0  # To track spawning since you are not using the timer event here

    def update(self):
        # Instantly poll data arrays from the background camera thread without blocking!
        BG_image, indexF_y, current_gesture = self.camera.get_tracking_data()
        self.current_bg = BG_image

        # --- STATE: START MENU ---
        if self.state == "START":
            if current_gesture == "CLICK":
                self.state = "PLAY"

        # --- STATE: ACTIVE GAMEPLAY ---
        elif self.state == "PLAY":
            # AUTO PAUSE: Trigger state safety freeze if hand is lost
            if indexF_y is None:
                self.state = "PAUSE"
                return

            # Map finger height range smoothly across viewport resolution
            pos = int(indexF_y * self.screen_h)
            self.bird.set_position(pos)

            for pipe in self.pipes[:]:
                pipe.move()
                if not pipe.passed and pipe.scr_w < self.bird.x:
                    pipe.passed = True
                    self.score += 1
                if pipe.IsOffScreen():
                    self.pipes.remove(pipe)

            # Evaluate boundary constraints or pipe layers
            if self.bird.y > self.screen_h or self.bird.y < 0 or any(pipe.hasCollided(self.bird) for pipe in self.pipes):
                self.state = "END"
                if self.score > self.high_score:
                    self.high_score = self.score

        # --- STATE: AUTO-PAUSED ---
        elif self.state == "PAUSE":
            if indexF_y is not None:
                self.state = "PLAY"

        # --- STATE: GAME OVER MENU ---
        elif self.state == "END":
            if current_gesture == "CLICK":
                self.reset_game()

    def draw_background(self):
        # Simply display the frame captured during the update pass
        if self.current_bg is not None:
            self.screen.blit(self.current_bg, (0, 0))
        else:
            self.screen.fill((113, 197, 207))
            self.screen.blit(self.bg, (0, 0))

    def draw(self):
        self.draw_background()
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
