#!/usr/bin/env python3
"""
Game Edukasi Bentuk & Warna untuk Anak TK
Versi Lengkap dengan Fitur Kuis, Belajar, dan Leaderboard
"""

import pygame
import sys
import os

# Import modul game
from config import *
from core.game_state import GameState
from ui.screen import MainMenu, LearnMode, GameScreen, HighScoreScreen

def init_pygame():
    """Initialize pygame dengan error handling"""
    try:
        pygame.init()
        pygame.mixer.init()
        
        # Set window
        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Belajar Bentuk & Warna - Game Edukasi TK")
        
        # Set icon
        try:
            icon = pygame.Surface((32, 32))
            icon.fill((255, 0, 0))
            pygame.display.set_icon(icon)
        except:
            pass
        
        # Load font
        try:
            # Try to load custom font
            font_path = "assets/fonts/comic.ttf"
            if os.path.exists(font_path):
                font = pygame.font.Font(font_path, 28)
            else:
                font = pygame.font.Font(None, 28)
        except:
            font = pygame.font.SysFont("arial", 24)
        
        return screen, font
        
    except Exception as e:
        print(f"Error initializing pygame: {e}")
        sys.exit(1)

class Game:
    def __init__(self):
        self.screen, self.font = init_pygame()
        self.state = GameState()
        self.current_screen = "menu"
        self.clock = pygame.time.Clock()
        
    def run(self):
        """Main game loop yang benar"""
        while True:
            try:
                # Handle events GLOBAL terlebih dahulu
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            if self.current_screen != "menu":
                                self.current_screen = "menu"
                
                # Update screen berdasarkan state
                next_screen = self.update_current_screen()
                
                if next_screen and next_screen != self.current_screen:
                    self.current_screen = next_screen
                
                pygame.display.flip()
                self.clock.tick(FPS)
                
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()
                break
    
    def update_current_screen(self):
        """Render dan update screen berdasarkan state"""
        if self.current_screen == "menu":
            return self.show_menu()
        elif self.current_screen == "kuis":
            return self.show_game()
        elif self.current_screen == "belajar":
            return self.show_learn()
        elif self.current_screen == "scores":
            return self.show_scores()
    
    def show_menu(self):
        """Show main menu - FIXED VERSION"""
        screen = self.screen
        font = self.font
        
        # Clear screen
        screen.fill(BACKGROUND)
        
        # Title
        title_font = pygame.font.Font(None, 72)
        title = title_font.render("BELAJAR BENTUK & WARNA", True, PRIMARY)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = font.render("Untuk Anak TK/PAUD", True, (150, 150, 150))
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 220))
        screen.blit(subtitle, subtitle_rect)
        
        # Draw shapes preview
        from core.shapes import draw_bentuk
        shapes_preview = ["persegi", "lingkaran", "segitiga", "bintang", "hati"]
        colors_preview = [(255,0,0), (0,0,255), (0,255,0), (255,255,0), (255,0,255)]
        
        for i, (shape, color) in enumerate(zip(shapes_preview, colors_preview)):
            shape_img = draw_bentuk(shape, color, 80)
            x = 150 + i * 150
            y = WINDOW_HEIGHT - 150
            screen.blit(shape_img, (x, y))
        
        # Create buttons
        center_x = WINDOW_WIDTH // 2
        button_width = 300
        button_height = 60
        start_y = 300
        
        buttons = []
        
        # Mode Kuis
        buttons.append({
            "rect": pygame.Rect(center_x - button_width//2, start_y, button_width, button_height),
            "text": "MULAI KUIS",
            "action": "kuis",
            "color": (100, 200, 255),
            "hover": (50, 180, 255)
        })
        
        # Mode Belajar
        buttons.append({
            "rect": pygame.Rect(center_x - button_width//2, start_y + 80, button_width, button_height),
            "text": " MODE BELAJAR",
            "action": "belajar",
            "color": (255, 200, 100),
            "hover": (255, 180, 50)
        })
        
        # Pilih Level
        buttons.append({
            "rect": pygame.Rect(center_x - button_width//2, start_y + 160, button_width, button_height),
            "text": f"LEVEL: {self.state.level.upper()}",
            "action": "toggle_level",
            "color": (200, 100, 255),
            "hover": (180, 50, 255)
        })
        
        # High Scores
        buttons.append({
            "rect": pygame.Rect(center_x - button_width//2, start_y + 240, button_width, button_height),
            "text": " HIGH SCORES",
            "action": "scores",
            "color": (100, 255, 150),
            "hover": (50, 230, 100)
        })
        
        # Exit
        buttons.append({
            "rect": pygame.Rect(center_x - button_width//2, start_y + 320, button_width, button_height),
            "text": "KELUAR",
            "action": "exit",
            "color": (255, 100, 100),
            "hover": (255, 50, 50)
        })
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        # Check for mouse click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
        
        # Draw buttons and check clicks
        for btn in buttons:
            # Check hover
            is_hovered = btn["rect"].collidepoint(mouse_pos)
            
            # Draw button
            color = btn["hover"] if is_hovered else btn["color"]
            pygame.draw.rect(screen, color, btn["rect"], border_radius=10)
            pygame.draw.rect(screen, (100, 100, 100), btn["rect"], 2, border_radius=10)
            
            # Draw text
            label = font.render(btn["text"], True, (0, 0, 0))
            label_rect = label.get_rect(center=btn["rect"].center)
            screen.blit(label, label_rect)
            
            # Check click
            if mouse_clicked and is_hovered:
                if btn["action"] == "exit":
                    pygame.quit()
                    sys.exit()
                elif btn["action"] == "toggle_level":
                    levels = list(LEVELS.keys())
                    current_idx = levels.index(self.state.level)
                    next_idx = (current_idx + 1) % len(levels)
                    self.state.level = levels[next_idx]
                    # Update button text
                    btn["text"] = f"LEVEL: {self.state.level.upper()}"
                else:
                    return btn["action"]
        
        # Footer
        footer = font.render("© 2024 Game Edukasi TK", True, (200, 200, 200))
        screen.blit(footer, (WINDOW_WIDTH//2 - footer.get_width()//2, WINDOW_HEIGHT - 40))
        
        return None  # Stay in menu
    
    def show_game(self):
        """Show game screen - FIXED BUTTON CLICKS"""
        from core import generate_soal, generate_opsi, cek_jawaban, draw_bentuk
        from core.logic import hitung_skor
        # Initialize game state jika pertama kali
        if not hasattr(self, 'game_started'):
            self.game_started = True
            self.state.reset()
            self.time_left = LEVELS[self.state.level]["waktu"]
            self.last_time = pygame.time.get_ticks()
            self.score = 0
            self.streak = 0
            
            # Generate first question
            self.soal = generate_soal(BENTUK_LIST, WARNA_LIST)
            self.opsi = generate_opsi(self.soal, BENTUK_LIST, WARNA_LIST, 
                                     LEVELS[self.state.level]["opsi"])
            self.shape_img = draw_bentuk(self.soal.bentuk, self.soal.warna, 280)
            
            self.feedback = None
            self.feedback_time = 0
            self.waiting_for_next = False
            self.next_question_timer = 0
        
        # Handle events - SEDERHANAKAN!
        mouse_clicked = False
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    delattr(self, 'game_started')
                    return "menu"
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
                mouse_pos = pygame.mouse.get_pos()
        
        # Check for mouse clicks on buttons
        if mouse_clicked and not self.waiting_for_next:
            # Check back button
            back_rect = pygame.Rect(20, 20, 100, 40)
            if back_rect.collidepoint(mouse_pos):
                delattr(self, 'game_started')
                return "menu"
            
            # Check answer buttons
            button_width = 400
            button_height = 50
            start_x = (WINDOW_WIDTH - button_width) // 2
            start_y = 400
            
            for i, opsi in enumerate(self.opsi):
                btn_rect = pygame.Rect(start_x, start_y + i * 70, button_width, button_height)
                
                if btn_rect.collidepoint(mouse_pos):
                    # User clicked an answer
                    if cek_jawaban(opsi, self.soal):
                        self.feedback = "✓ BENAR!"
                        self.feedback_color = CORRECT_COLOR
                        points = hitung_skor(self.time_left, 
                                           LEVELS[self.state.level], 
                                           self.streak)
                        self.score += points
                        self.state.score = self.score  # Update game state
                        self.streak += 1
                    else:
                        self.feedback = f"✗ SALAH! Jawaban: {self.soal.bentuk} - {self.soal.warna_name}"
                        self.feedback_color = WRONG_COLOR
                        self.streak = 0
                    
                    self.feedback_time = pygame.time.get_ticks()
                    self.waiting_for_next = True
                    self.next_question_timer = pygame.time.get_ticks()
                    break
        
        # Check if it's time for next question
        if self.waiting_for_next:
            if pygame.time.get_ticks() - self.next_question_timer > 1000:  # 1 second delay
                # Generate new question
                self.soal = generate_soal(BENTUK_LIST, WARNA_LIST)
                self.opsi = generate_opsi(self.soal, BENTUK_LIST, WARNA_LIST, 
                                         LEVELS[self.state.level]["opsi"])
                self.shape_img = draw_bentuk(self.soal.bentuk, self.soal.warna, 280)
                self.time_left = LEVELS[self.state.level]["waktu"]
                self.feedback = None
                self.waiting_for_next = False
        
        # Update timer (only if not waiting for next question)
        if not self.waiting_for_next:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_time >= 1000:
                self.time_left -= 1
                self.last_time = current_time
                
                if self.time_left <= 0:
                    # Time's up
                    self.state.score = self.score
                    self.state.save_score()
                    delattr(self, 'game_started')
                    return "scores"
        
        # Draw everything
        self.screen.fill(BACKGROUND)
        
        # Header
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("TEBAK BENTUK & WARNA", True, PRIMARY)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 40))
        self.screen.blit(title, title_rect)
        
        # Game info
        info_y = 80
        font = self.font
        
        # Level
        level_text = font.render(f"Level: {self.state.level.upper()}", True, TEXT_COLOR)
        self.screen.blit(level_text, (50, info_y))
        
        # Score
        score_text = font.render(f"Skor: {self.score}", True, (0, 100, 200))
        self.screen.blit(score_text, (WINDOW_WIDTH - 150, info_y))
        
        # Streak
        if self.streak > 0:
            fire_emoji = "🔥" if self.streak >= 5 else "⭐"
            streak_text = font.render(f"{fire_emoji} x{self.streak}", True, (255, 165, 0))
            self.screen.blit(streak_text, (WINDOW_WIDTH - 300, info_y))
        
        # Timer
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        timer_text = f"{minutes:02d}:{seconds:02d}"
        
        # Timer color based on time
        if self.time_left > 10:
            timer_color = (0, 200, 0)
        elif self.time_left > 5:
            timer_color = (255, 165, 0)
        else:
            timer_color = (255, 0, 0)
        
        timer_surf = font.render(timer_text, True, timer_color)
        timer_rect = timer_surf.get_rect(center=(WINDOW_WIDTH//2, info_y))
        self.screen.blit(timer_surf, timer_rect)
        
        # Timer progress bar
        bar_width = 200
        bar_height = 8
        bar_x = WINDOW_WIDTH//2 - bar_width//2
        bar_y = info_y + 25
        
        # Background bar
        pygame.draw.rect(self.screen, (200, 200, 200), 
                        (bar_x, bar_y, bar_width, bar_height), 
                        border_radius=4)
        
        # Progress fill
        max_time = LEVELS[self.state.level]["waktu"]
        progress = min(self.time_left / max_time, 1.0)
        fill_width = int(bar_width * progress)
        pygame.draw.rect(self.screen, timer_color, 
                        (bar_x, bar_y, fill_width, bar_height), 
                        border_radius=4)
        
        # Draw shape
        if self.shape_img:
            pos_x = WINDOW_WIDTH//2 - self.shape_img.get_width()//2
            pos_y = 150
            self.screen.blit(self.shape_img, (pos_x, pos_y))
        
        # Draw answer buttons
        button_width = 400
        button_height = 50
        start_x = (WINDOW_WIDTH - button_width) // 2
        start_y = 400
        
        # Get mouse position for hover effect
        current_mouse_pos = pygame.mouse.get_pos()
        
        for i, opsi in enumerate(self.opsi):
            bentuk, warna = opsi
            text = f"{bentuk.upper()} - {warna.upper()}"
            
            btn_rect = pygame.Rect(start_x, start_y + i * 70, button_width, button_height)
            is_hovered = btn_rect.collidepoint(current_mouse_pos) and not self.waiting_for_next
            
            # Draw button
            color = (230, 240, 255) if is_hovered else (255, 255, 255)
            pygame.draw.rect(self.screen, color, btn_rect, border_radius=8)
            pygame.draw.rect(self.screen, (100, 100, 100), btn_rect, 2, border_radius=8)
            
            # Draw text
            label = font.render(text, True, (0, 0, 0))
            label_rect = label.get_rect(center=btn_rect.center)
            self.screen.blit(label, label_rect)
        
        # Draw back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        back_hovered = back_rect.collidepoint(current_mouse_pos)
        back_color = (200, 200, 255) if back_hovered else (220, 220, 220)
        pygame.draw.rect(self.screen, back_color, back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 100), back_rect, 2, border_radius=5)
        back_text = font.render("Menu", True, (0, 0, 0))
        self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        # Draw feedback
        if self.feedback and pygame.time.get_ticks() - self.feedback_time < 1000:
            feedback_font = pygame.font.Font(None, 36)
            feedback_surf = feedback_font.render(self.feedback, True, self.feedback_color)
            feedback_rect = feedback_surf.get_rect(center=(WINDOW_WIDTH//2, 350))
            self.screen.blit(feedback_surf, feedback_rect)
            
            # Draw countdown for next question
            time_left = 1.0 - (pygame.time.get_ticks() - self.feedback_time) / 1000.0
            countdown_text = font.render(f"Next in: {time_left:.1f}s", True, (150, 150, 150))
            countdown_rect = countdown_text.get_rect(center=(WINDOW_WIDTH//2, 380))
            self.screen.blit(countdown_text, countdown_rect)
        
        # Draw instructions
        if not self.waiting_for_next:
            instr_text = font.render("Klik jawaban yang sesuai dengan gambar di atas", 
                                   True, (100, 100, 100))
            instr_rect = instr_text.get_rect(center=(WINDOW_WIDTH//2, 340))
            self.screen.blit(instr_text, instr_rect)
        
        return None  # Stay in game
        
    def show_learn(self):
        """Show learning mode - SIMPLIFIED"""
        from core.shapes import draw_bentuk
        
        if not hasattr(self, 'learn_data'):
            self.learn_data = {
                'shape_idx': 0,
                'color_idx': 0,
                'shapes': BENTUK_LIST,
                'colors': list(WARNA_LIST.items()),
                'scale': 1.0,
                'scale_up': True
            }
        
        data = self.learn_data
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    delattr(self, 'learn_data')
                    return "menu"
                elif event.key == pygame.K_LEFT:
                    data['shape_idx'] = (data['shape_idx'] - 1) % len(data['shapes'])
                    data['scale'] = 0.5
                    data['scale_up'] = True
                elif event.key == pygame.K_RIGHT:
                    data['shape_idx'] = (data['shape_idx'] + 1) % len(data['shapes'])
                    data['scale'] = 0.5
                    data['scale_up'] = True
                elif event.key == pygame.K_UP:
                    data['color_idx'] = (data['color_idx'] - 1) % len(data['colors'])
                    data['scale'] = 0.5
                    data['scale_up'] = True
                elif event.key == pygame.K_DOWN:
                    data['color_idx'] = (data['color_idx'] + 1) % len(data['colors'])
                    data['scale'] = 0.5
                    data['scale_up'] = True
                elif event.key == pygame.K_SPACE:
                    import random
                    data['shape_idx'] = random.randint(0, len(data['shapes'])-1)
                    data['color_idx'] = random.randint(0, len(data['colors'])-1)
                    data['scale'] = 0.5
                    data['scale_up'] = True
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check back button
                back_rect = pygame.Rect(20, 20, 100, 40)
                if back_rect.collidepoint(mouse_pos):
                    delattr(self, 'learn_data')
                    return "menu"
        
        # Update animation
        if data['scale_up'] and data['scale'] < 1.0:
            data['scale'] += 0.05
        elif data['scale'] >= 1.0:
            data['scale_up'] = False
        
        # Get current shape and color
        shape_name = data['shapes'][data['shape_idx']]
        color_name, color_rgb = data['colors'][data['color_idx']]
        shape_img = draw_bentuk(shape_name, color_rgb, 300)
        
        # Draw
        self.screen.fill(BACKGROUND)
        
        # Title
        font = self.font
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("MODE BELAJAR", True, PRIMARY)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        # Current shape name
        current_text = f"{shape_name.upper()} - {color_name.upper()}"
        text_surf = pygame.font.Font(None, 48).render(current_text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(WINDOW_WIDTH//2, 120))
        self.screen.blit(text_surf, text_rect)
        
        # Draw shape with animation
        if shape_img:
            img_width = int(shape_img.get_width() * data['scale'])
            img_height = int(shape_img.get_height() * data['scale'])
            scaled_img = pygame.transform.scale(shape_img, (img_width, img_height))
            
            pos_x = WINDOW_WIDTH//2 - img_width//2
            pos_y = 180
            
            self.screen.blit(scaled_img, (pos_x, pos_y))
        
        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        back_rect = pygame.Rect(20, 20, 100, 40)
        is_hovered = back_rect.collidepoint(mouse_pos)
        back_color = (200, 200, 255) if is_hovered else (220, 220, 220)
        pygame.draw.rect(self.screen, back_color, back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 100), back_rect, 2, border_radius=5)
        back_text = font.render("Menu", True, (0, 0, 0))
        self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        # Instructions
        instructions = [
            "Kiri/Kanan: Ganti Bentuk",
            "Atas/Bawah: Ganti Warna",
            "Spasi: Acak Bentuk & Warna",
            "ESC: Kembali ke Menu"
        ]
        
        for i, text in enumerate(instructions):
            text_surf = font.render(text, True, (100, 100, 100))
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH//2, 400 + i * 30))
            self.screen.blit(text_surf, text_rect)
        
        return None
    
    def show_scores(self):
        """Show high scores screen"""
        scores = self.state.load_scores()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "menu"
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check back button
                back_rect = pygame.Rect(20, 20, 100, 40)
                if back_rect.collidepoint(mouse_pos):
                    return "menu"
                
                # Check play again button
                play_rect = pygame.Rect(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT - 100, 300, 50)
                if play_rect.collidepoint(mouse_pos):
                    return "kuis"
        
        # Draw
        self.screen.fill(BACKGROUND)
        
        # Title
        title_font = pygame.font.Font(None, 64)
        title = title_font.render("🏆 HIGH SCORES", True, PRIMARY)
        title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 80))
        self.screen.blit(title, title_rect)
        
        # Draw scores table
        table_y = 180
        font = self.font
        header_font = pygame.font.Font(None, 36)
        
        # Draw headers
        headers = ["Peringkat", "Nama", "Skor", "Level", "Tanggal"]
        for i, header in enumerate(headers):
            x = 100 + i * 180
            header_surf = header_font.render(header, True, (100, 100, 200))
            self.screen.blit(header_surf, (x, table_y))
        
        # Draw scores
        for idx, score_data in enumerate(scores[:10]):
            y = table_y + 50 + idx * 40
            
            # Rank with medal emoji
            if idx == 0:
                rank = "🥇"
            elif idx == 1:
                rank = "🥈"
            elif idx == 2:
                rank = "🥉"
            else:
                rank = f"{idx + 1}."
            
            columns = [
                rank,
                score_data.get("player", "Unknown"),
                str(score_data.get("score", 0)),
                score_data.get("level", "mudah").upper(),
                score_data.get("date", "")[5:16]  # Remove year
            ]
            
            for i, text in enumerate(columns):
                x = 100 + i * 180
                color = (255, 215, 0) if idx < 3 else TEXT_COLOR
                text_surf = font.render(text, True, color)
                self.screen.blit(text_surf, (x, y))
        
        # If no scores
        if not scores:
            no_scores = font.render("Belum ada skor tercatat!", True, (150, 150, 150))
            no_rect = no_scores.get_rect(center=(WINDOW_WIDTH//2, 300))
            self.screen.blit(no_scores, no_rect)
        
        # Current score
        if self.state.score > 0:
            current_score = pygame.font.Font(None, 48).render(
                f"Skor Terakhir: {self.state.score}", 
                True, 
                (0, 200, 0)
            )
            current_rect = current_score.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT - 180))
            self.screen.blit(current_score, current_rect)
        
        # Draw buttons
        mouse_pos = pygame.mouse.get_pos()
        
        # Back button
        back_rect = pygame.Rect(20, 20, 100, 40)
        back_hovered = back_rect.collidepoint(mouse_pos)
        back_color = (200, 200, 255) if back_hovered else (220, 220, 220)
        pygame.draw.rect(self.screen, back_color, back_rect, border_radius=5)
        pygame.draw.rect(self.screen, (100, 100, 100), back_rect, 2, border_radius=5)
        back_text = font.render("← Kembali", True, (0, 0, 0))
        self.screen.blit(back_text, (back_rect.x + 10, back_rect.y + 10))
        
        # Play again button
        play_rect = pygame.Rect(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT - 100, 300, 50)
        play_hovered = play_rect.collidepoint(mouse_pos)
        play_color = (50, 180, 255) if play_hovered else (100, 200, 255)
        pygame.draw.rect(self.screen, play_color, play_rect, border_radius=10)
        pygame.draw.rect(self.screen, (100, 100, 100), play_rect, 2, border_radius=10)
        play_text = font.render("🎮 MAIN LAGI", True, (0, 0, 0))
        play_rect_text = play_text.get_rect(center=play_rect.center)
        self.screen.blit(play_text, play_rect_text)
        
        return None

def main():
    """Main entry point"""
    # Check and create necessary directories
    for directory in ["assets/sounds", "assets/fonts", "data"]:
        os.makedirs(directory, exist_ok=True)
    
    print("=" * 50)
    print("GAME EDUKASI BENTUK & WARNA")
    print("Untuk Anak TK/PAUD")
    print("=" * 50)
    print("\nKontrol:")
    print("- ESC: Kembali ke Menu")
    print("- Mouse: Klik tombol")
    print("- Keyboard: Navigasi di Mode Belajar")
    print("=" * 50)
    
    game = Game()
    game.run()

if __name__ == "__main__":
    main()