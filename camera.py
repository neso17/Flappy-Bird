import cv2
import pygame
import mediapipe as mp
import numpy as np
import math
import threading

class Camera(threading.Thread):
    def __init__(self, screen_w, screen_h):
        # Initialize the threading superclass
        super().__init__()
        self.screen_w = screen_w
        self.screen_h = screen_h
        
        self.cap = cv2.VideoCapture(0)
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1, 
            min_detection_confidence=0.7, 
            min_tracking_confidence=0.4
        )
        self.mp_draw = mp.solutions.drawing_utils

        # Threading state safety variables
        self.running = True
        self.index_y = None
        self.gesture = "NONE"
        self.latest_surface = None
        self.lock = threading.Lock() # Prevents data corruption between threads

        # Start the background thread instantly
        self.daemon = True # Closes the thread automatically when the game exits
        self.start()

    def run(self):
        """The actual code running continuously in the background thread."""
        while self.running:
            success, frame = self.cap.read()
            if not success:
                continue

            frame = cv2.flip(frame, 1)
            
            # Read current values safely
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            
            local_index_y = None
            local_gesture = "NONE"
            
            # Create a localized black background (or base frame)
            black_bg = np.zeros_like(frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    idx = hand_landmarks.landmark[8]
                    thumb = hand_landmarks.landmark[4]
                    
                    local_index_y = idx.y
                    
                    distance = math.hypot(idx.x - thumb.x, idx.y - thumb.y)
                    if distance < 0.04:
                        local_gesture = "CLICK"
                    
                    self.mp_draw.draw_landmarks(
                        black_bg, 
                        hand_landmarks, 
                        self.mp_hands.HAND_CONNECTIONS,
                        self.mp_draw.DrawingSpec(color=(0, 255, 128), thickness=2, circle_radius=5),
                        self.mp_draw.DrawingSpec(color=(255, 255, 255), thickness=2)
                    )

            # Format the array into a clean Pygame surface
            display_frame = cv2.cvtColor(black_bg, cv2.COLOR_BGR2RGB)
            display_frame = cv2.transpose(display_frame)
            pygame_surface = pygame.surfarray.make_surface(display_frame)
            pygame_surface = pygame.transform.scale(pygame_surface, (self.screen_w, self.screen_h))

            # Push tracking data back to Pygame safely using a thread Lock
            with self.lock:
                self.index_y = local_index_y
                self.gesture = local_gesture
                self.latest_surface = pygame_surface

    def get_tracking_data(self):
        """Called by Pygame inside update() to instantly read values without lag."""
        with self.lock:
            return self.latest_surface, self.index_y, self.gesture

    def release(self):
        self.running = False
        self.cap.release()