import cv2
import pygame
import threading
import sys

class CameraBG:
    def __init__(self, screen_w, screen_h):
        self.scr_w = screen_w
        self.scr_h = screen_h
        self.cap = cv2.VideoCapture(0)
        self.last_frame = None
        self.running = True

        #bacground thread to proccess MR background
        self.thread = threading.Thread(target=self.update_frame, daemon=True) #daemon thread closes when main program exits
        self.thread.start() #start thread to continuously update camera feed in background

    def update_frame(self):
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (self.scr_w, self.scr_h))

            conversion = pygame.surfarray.make_surface(frame)
            conversion = pygame.transform.rotate(conversion, -90)
            conversion = pygame.transform.flip(conversion, True, False)
            self.last_frame = conversion.copy() #copy to avoid threading issues

    def get_frame(self):
        return self.last_frame

    def release(self):
        self.running = False
        self.thread.join() # wait for thread to finish before exiting
        self.cap.release()