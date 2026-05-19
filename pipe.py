import random
import pygame

class Pipe:
  def __init__(self, screen_w, screen_h):
    self.scr_w = screen_w
    self.scr_h = screen_h
    self.w = 80
    self.gap = 220
    self.speed = 5
    self.passed = False

    min_h = 40
    max_h = screen_h - self.gap - 40
        
    self.top_h = random.randint(min_h, max_h)
    self.bottom_h = screen_h - self.top_h - self.gap

  def move(self):
    self.scr_w -= self.speed

  def IsOffScreen(self):
    return self.scr_w < -self.w
  
  def hasCollided(self, bird):
    if bird.y < self.top_h or bird.y + bird.size > self.scr_h - self.bottom_h:
      if bird.x + bird.size > self.scr_w and bird.x < self.scr_w + self.w:
        return True
    return False
  
  def draw(self, screen):
    pygame.draw.rect(screen, (0, 255, 0), (self.scr_w, 0, self.w, self.top_h))
    pygame.draw.rect(screen, (0, 255, 0), (self.scr_w, self.scr_h - self.bottom_h, self.w, self.bottom_h))