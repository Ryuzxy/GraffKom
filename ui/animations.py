import pygame
import math

class FadeAnimation:
    def __init__(self, duration=500):
        self.duration = duration
        self.start_time = 0
        self.alpha = 0
        self.running = False
        
    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.running = True
        
    def update(self):
        if not self.running:
            return
            
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        self.alpha = int(255 * progress)
        
        if progress >= 1.0:
            self.running = False
            
    def get_alpha(self):
        return self.alpha
    
    def is_finished(self):
        return not self.running

class ScaleAnimation:
    def __init__(self, start_scale=0, end_scale=1, duration=300):
        self.start_scale = start_scale
        self.end_scale = end_scale
        self.duration = duration
        self.start_time = 0
        self.running = False
        
    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.running = True
        
    def update(self):
        if not self.running:
            return self.end_scale
            
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        # Ease-out function
        progress = 1 - (1 - progress) ** 3
        
        scale = self.start_scale + (self.end_scale - self.start_scale) * progress
        
        if progress >= 1.0:
            self.running = False
            
        return scale
    
    def is_finished(self):
        return not self.running

class ShakeAnimation:
    def __init__(self, intensity=10, duration=200):
        self.intensity = intensity
        self.duration = duration
        self.start_time = 0
        self.running = False
        
    def start(self):
        self.start_time = pygame.time.get_ticks()
        self.running = True
        
    def update(self):
        if not self.running:
            return (0, 0)
            
        elapsed = pygame.time.get_ticks() - self.start_time
        progress = min(elapsed / self.duration, 1.0)
        
        if progress >= 1.0:
            self.running = False
            return (0, 0)
            
        # Mengurangi intensitas seiring waktu
        current_intensity = self.intensity * (1 - progress)
        
        # Get shake offset using sine waves
        offset_x = math.sin(elapsed * 0.1) * current_intensity
        offset_y = math.cos(elapsed * 0.07) * current_intensity * 0.7
        
        return (offset_x, offset_y)
    
    def is_finished(self):
        return not self.running