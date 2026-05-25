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
    max_h = screen_h - self.gap - min_h
        
    self.top_h = random.randint(min_h, max_h)
    self.bottom_h = screen_h - self.top_h - self.gap

  # top mask + surface
    self.top_image = pygame.Surface((self.w, self.top_h), pygame.SRCALPHA)
    self.top_image.fill((0, 255, 0))
    self.top_mask = pygame.mask.from_surface(self.top_image)
    self.top_rect = self.top_image.get_rect(topleft=(self.scr_w, 0))

    # bottom mask + surface
    self.bottom_image = pygame.Surface((self.w, self.bottom_h), pygame.SRCALPHA)
    self.bottom_image.fill((0, 255, 0))
    self.bottom_mask = pygame.mask.from_surface(self.bottom_image)
    self.bottom_rect = self.bottom_image.get_rect(topleft=(self.scr_w, screen_h - self.bottom_h))


  def move(self):
    self.scr_w -= self.speed
    #update rects
    self.top_rect.x = self.scr_w
    self.bottom_rect.x = self.scr_w

    
  def IsOffScreen(self):
    return self.scr_w < -self.w
  
  def hasCollided(self, bird):
    top_offset = (self.top_rect.x - bird.bird_rec.x, self.top_rect.y - bird.bird_rec.y)
    if bird.bird_mask.overlap(self.top_mask, top_offset):
      return True
    
    bottom_offset = (self.bottom_rect.x - bird.bird_rec.x, self.bottom_rect.y - bird.bird_rec.y)
    if bird.bird_mask.overlap(self.bottom_mask, bottom_offset):
      return True
    return False
  
  def draw(self, screen):
    pygame.draw.rect(screen, (0, 255, 0), (self.scr_w, 0, self.w, self.top_h))
    pygame.draw.rect(screen, (0, 255, 0), (self.scr_w, self.scr_h - self.bottom_h, self.w, self.bottom_h))