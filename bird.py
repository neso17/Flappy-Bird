import pygame


class Bird:
  def __init__(self, colour, size):
    self.colour = colour
    self.size = size
    self.x = 50
    self.y = 300
    self.g = 0.5
    self.vY = 2

    #create bird
    self.birdie = pygame.image.load("birdSprite.png").convert_alpha()
    self.birdie = pygame.transform.scale(self.birdie, (int(size), size))

    self.og_birdie = self.birdie

    #rect has center at x, y
    self.bird_rec = self.birdie.get_rect(center=(int(self.x), int(self.y)))
    self.bird_mask = pygame.mask.from_surface(self.birdie)
  
  def update(self):
    #moving
    self.vY += self.g      #acc --> vel --> pos
    self.y += self.vY

    #collision prep
    self.bird_rec.center = (int(self.x), int(self.y))

  def jumpUp(self):
    self.vY = -10

  def draw(self, screen):
    screen.blit(self.birdie, self.bird_rec)



