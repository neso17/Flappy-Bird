import pygame


class Bird:
  def __init__(self, colour, size):
    self.colour = colour
    self.size = size
    self.x = 50
    self.y = 300
    self.g = 0.5
    self.vY = 2

  def update(self):
    self.vY += self.g      #acc --> vel --> pos
    self.y += self.vY

  def jumpUp(self):
    self.vY = -10
  
  def draw(self, screen):
    pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size)