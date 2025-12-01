import pygame

class Button:
    def __init__(self, rect, text, callback, font, 
                 color=(220, 220, 220), hover_color=(200, 230, 255),
                 text_color=(0, 0, 0), border_radius=10):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.callback = callback
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.is_hovered = False
        
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, 
                        border_radius=self.border_radius)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 
                        2, border_radius=self.border_radius)
        
        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, label_rect)
        
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.callback()
                return True
        return False
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

class ToggleButton(Button):
    def __init__(self, rect, text, callback, font, 
                 active=False, on_color=(150, 255, 150), 
                 off_color=(220, 220, 220)):
        super().__init__(rect, text, callback, font, off_color)
        self.active = active
        self.on_color = on_color
        self.off_color = off_color
        
    def draw(self, screen):
        self.color = self.on_color if self.active else self.off_color
        super().draw(screen)
        
    def handle_event(self, event):
        if super().handle_event(event):
            self.active = not self.active
            return True
        return False

class ImageButton:
    def __init__(self, rect, image, callback):
        self.rect = pygame.Rect(rect)
        self.image = image
        self.callback = callback
        self.is_hovered = False
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.is_hovered:
            overlay = pygame.Surface(self.rect.size, pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 50))
            screen.blit(overlay, self.rect)
            
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                self.callback()
                return True
        return False