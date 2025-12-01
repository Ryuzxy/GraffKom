import pygame

def render_bentuk(screen, image, pos):
    """Render bentuk ke screen"""
    screen.blit(image, pos)

def draw_text(screen, text, font, color, pos, center=False):
    """Helper untuk menggambar text"""
    label = font.render(text, True, color)
    if center:
        pos = label.get_rect(center=pos)
    screen.blit(label, pos)

def draw_timer(screen, time_left, font, pos):
    """Draw timer dengan visual menarik"""
    minutes = time_left // 60
    seconds = time_left % 60
    
    # Warna berdasarkan waktu
    if time_left > 10:
        color = (0, 200, 0)
    elif time_left > 5:
        color = (255, 165, 0)
    else:
        color = (255, 0, 0)
    
    timer_text = f"{minutes:02d}:{seconds:02d}"
    draw_text(screen, timer_text, font, color, pos, center=True)
    
    # Progress bar
    bar_width = 200
    bar_height = 10
    bar_x = pos[0] - bar_width // 2
    bar_y = pos[1] + 30
    
    # Background bar
    pygame.draw.rect(screen, (200, 200, 200), 
                    (bar_x, bar_y, bar_width, bar_height), 
                    border_radius=5)
    
    # Progress fill
    progress = min(time_left / 30, 1.0)  # Asumsi 30 detik maks
    fill_width = int(bar_width * progress)
    pygame.draw.rect(screen, color, 
                    (bar_x, bar_y, fill_width, bar_height), 
                    border_radius=5)

def draw_score(screen, score, font, pos):
    """Draw score dengan efek"""
    draw_text(screen, f"Skor: {score}", font, (0, 100, 200), pos)
    
def draw_streak(screen, streak, font, pos):
    """Draw streak counter"""
    if streak > 0:
        fire_emoji = "🔥" if streak >= 5 else "⭐"
        draw_text(screen, f"{fire_emoji} x{streak}", font, (255, 165, 0), pos)