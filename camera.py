import cv2
import pygame

class CameraBG:
    def __init__(self, screen_w, screen_h):
        self.scr_w = screen_w
        self.scr_h = screen_h
        self.cap = cv2.VideoCapture(0)

    def get_frame(self):
        success, frame = self.cap.read()
        if not success:
            return None

        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        frame = cv2.resize(frame, (self.scr_w, self.scr_h))
        
        surface = pygame.surfarray.make_surface(frame)
        surface = pygame.transform.rotate(surface, -90)
        surface = pygame.transform.flip(surface, True, False)
        return surface

    def release(self):
        self.cap.release()