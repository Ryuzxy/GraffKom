import pygame
import sys
from datetime import datetime
import os
import math

from config import *
from core import generate_soal, generate_opsi, cek_jawaban, draw_bentuk, GameState
from core.logic import hitung_skor
from .buttons import Button, ToggleButton
from .renderer import render_bentuk, draw_text, draw_timer, draw_score, draw_streak
from .animations import FadeAnimation, ScaleAnimation, ShakeAnimation

class MainMenu:
    def __init__(self, screen, font, state):
        self.screen = screen
        self.font = font
        self.state = state
        self.title_font = pygame.font.Font(None, 72)
        self.buttons = []
        self.create_buttons()
        
    def create_buttons(self):
        center_x = WINDOW_WIDTH // 2
        button_width = 300
        button_height = 60
        start_y = 300
        
        # Mode Kuis
        self.buttons.append(Button(
            rect=(center_x - button_width//2, start_y, button_width, button_height),
            text="MULAI KUIS",
            callback=self.start_kuis,
            font=self.font,
            color=(100, 200, 255),
            hover_color=(50, 180, 255)
        ))
        
        # Mode Belajar
        self.buttons.append(Button(
            rect=(center_x - button_width//2, start_y + 80, button_width, button_height),
            text="MODE BELAJAR",
            callback=self.start_belajar,
            font=self.font,
            color=(255, 200, 100),
            hover_color=(255, 180, 50)
        ))
        
        # Pilih Level
        self.buttons.append(Button(
            rect=(center_x - button_width//2, start_y + 160, button_width, button_height),
            text=f"LEVEL: {self.state.level.upper()}",
            callback=self.toggle_level,
            font=self.font,
            color=(200, 100, 255),
            hover_color=(180, 50, 255)
        ))
        
        # High Scores
        self.buttons.append(Button(
            rect=(center_x - button_width//2, start_y + 240, button_width, button_height),
            text="HIGH SCORES",
            callback=self.show_scores,
            font=self.font,
            color=(100, 255, 150),
            hover_color=(50, 230, 100)
        ))
        
        # Exit
        self.buttons.append(Button(
            rect=(center_x - button_width//2, start_y + 320, button_width, button_height),
            text="KELUAR",
            callback=self.exit_game,
            font=self.font,
            color=(255, 100, 100),
            hover_color=(255, 50, 50)
        ))
    
    def start_kuis(self):
        self.state.game_mode = "kuis"
        self.state.reset()
        return "kuis"
    
    def start_belajar(self):
        self.state.game_mode = "belajar"
        return "belajar"
    
    def toggle_level(self):
        levels = list(LEVELS.keys())
        current_idx = levels.index(self.state.level)
        next_idx = (current_idx + 1) % len(levels)
        self.state.level = levels[next_idx]
        
        # Update button text
        for btn in self.buttons:
            if "LEVEL:" in btn.text:
                btn.text = f"LEVEL: {self.state.level.upper()}"
    
    def show_scores(self):
        return "scores"
    
    def exit_game(self):
        pygame.quit()
        sys.exit()
    
    def loop(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                
                for button in self.buttons:
                    result = button.handle_event(event)
                    if result:
                        if callable(result):
                            continue
                        elif result in ["kuis", "belajar", "scores"]:
                            return result
            
            # Update buttons
            for button in self.buttons:
                if hasattr(button, 'update'):
                    button.update()
            
            # Draw
            self.screen.fill(BACKGROUND)
            
            # Title
            title = self.title_font.render("BELAJAR BENTUK & WARNA", True, PRIMARY)
            title_rect = title.get_rect(center=(WINDOW_WIDTH//2, 150))
            self.screen.blit(title, title_rect)
            
            # Subtitle
            subtitle = self.font.render("Untuk Anak TK/PAUD", True, (150, 150, 150))
            subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH//2, 220))
            self.screen.blit(subtitle, subtitle_rect)
            
            # Draw shapes preview
            shapes_preview = ["persegi", "lingkaran", "segitiga", "bintang", "hati"]
            colors_preview = [(255,0,0), (0,0,255), (0,255,0), (255,255,0), (255,0,255)]
            
            for i, (shape, color) in enumerate(zip(shapes_preview, colors_preview)):
                shape_img = draw_bentuk(shape, color, 80)
                x = 150 + i * 150
                y = WINDOW_HEIGHT - 150
                self.screen.blit(shape_img, (x, y))
            
            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)
            
            # Footer
            footer = self.font.render("© 2024 Game Edukasi TK", True, (200, 200, 200))
            self.screen.blit(footer, (WINDOW_WIDTH//2 - footer.get_width()//2, WINDOW_HEIGHT - 40))
            
            pygame.display.flip()
            clock.tick(FPS)

class LearnMode:
    def __init__(self, screen, font, state):
        self.screen = screen
        self.font = font
        self.state = state
        self.current_shape = 0
        self.current_color = 0
        self.shapes = BENTUK_LIST
        self.colors = list(WARNA_LIST.items())
        self.shape_img = None
        self.update_shape()
        self.create_buttons()
        self.anim = ScaleAnimation(0, 1, 400)
        self.anim.start()
        
    def update_shape(self):
        shape_name = self.shapes[self.current_shape]
        color_name, color_rgb = self.colors[self.current_color]
        self.shape_img = draw_bentuk(shape_name, color_rgb, 300)
        self.current_text = f"{shape_name.upper()} - {color_name.upper()}"
        
    def create_buttons(self):
        # Back button
        self.back_btn = Button(
            rect=(20, 20, 100, 40),
            text="← Kembali",
            callback=self.go_back,
            font=self.font
        )
        
        # Shape buttons
        self.prev_shape_btn = Button(
            rect=(100, 500, 50, 50),
            text="←",
            callback=self.prev_shape,
            font=pygame.font.Font(None, 40)
        )
        
        self.next_shape_btn = Button(
            rect=(WINDOW_WIDTH - 150, 500, 50, 50),
            text="→",
            callback=self.next_shape,
            font=pygame.font.Font(None, 40)
        )
        
        # Color buttons
        self.prev_color_btn = Button(
            rect=(100, 570, 50, 50),
            text="↑",
            callback=self.prev_color,
            font=pygame.font.Font(None, 40)
        )
        
        self.next_color_btn = Button(
            rect=(WINDOW_WIDTH - 150, 570, 50, 50),
            text="↓",
            callback=self.next_color,
            font=pygame.font.Font(None, 40)
        )
        
        # Random button
        self.random_btn = Button(
            rect=(WINDOW_WIDTH//2 - 100, 570, 200, 50),
            text="Acak Bentuk & Warna",
            callback=self.randomize,
            font=self.font,
            color=(200, 150, 255)
        )
    
    def prev_shape(self):
        self.current_shape = (self.current_shape - 1) % len(self.shapes)
        self.update_shape()
        self.anim.start()
        
    def next_shape(self):
        self.current_shape = (self.current_shape + 1) % len(self.shapes)
        self.update_shape()
        self.anim.start()
        
    def prev_color(self):
        self.current_color = (self.current_color - 1) % len(self.colors)
        self.update_shape()
        self.anim.start()
        
    def next_color(self):
        self.current_color = (self.current_color + 1) % len(self.colors)
        self.update_shape()
        self.anim.start()
        
    def randomize(self):
        import random
        self.current_shape = random.randint(0, len(self.shapes)-1)
        self.current_color = random.randint(0, len(self.colors)-1)
        self.update_shape()
        self.anim.start()
        
    def go_back(self):
        return "menu"
    
    def loop(self):
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                    elif event.key == pygame.K_LEFT:
                        self.prev_shape()
                    elif event.key == pygame.K_RIGHT:
                        self.next_shape()
                    elif event.key == pygame.K_UP:
                        self.prev_color()
                    elif event.key == pygame.K_DOWN:
                        self.next_color()
                    elif event.key == pygame.K_SPACE:
                        self.randomize()
                
                # Handle button events
                buttons = [self.back_btn, self.prev_shape_btn, self.next_shape_btn,
                          self.prev_color_btn, self.next_color_btn, self.random_btn]
                
                for button in buttons:
                    result = button.handle_event(event)
                    if result and button == self.back_btn:
                        return "menu"
            
            # Update animation
            self.anim.update()
            scale = self.anim.get_alpha() if hasattr(self.anim, 'get_alpha') else self.anim.update()
            
            # Draw
            self.screen.fill(BACKGROUND)
            
            # Title
            draw_text(self.screen, "MODE BELAJAR", self.font, PRIMARY, 
                     (WINDOW_WIDTH//2, 50), center=True)
            
            # Current shape name
            draw_text(self.screen, self.current_text, 
                     pygame.font.Font(None, 48), TEXT_COLOR,
                     (WINDOW_WIDTH//2, 120), center=True)
            
            # Draw shape with animation
            if self.shape_img:
                img_width = int(self.shape_img.get_width() * scale)
                img_height = int(self.shape_img.get_height() * scale)
                scaled_img = pygame.transform.scale(self.shape_img, (img_width, img_height))
                
                pos_x = WINDOW_WIDTH//2 - img_width//2
                pos_y = 180
                
                self.screen.blit(scaled_img, (pos_x, pos_y))
            
            # Draw buttons
            for button in [self.back_btn, self.prev_shape_btn, self.next_shape_btn,
                          self.prev_color_btn, self.next_color_btn, self.random_btn]:
                button.draw(self.screen)
            
            # Instructions
            instructions = [
                "Kiri/Kanan: Ganti Bentuk",
                "Atas/Bawah: Ganti Warna",
                "Spasi: Acak",
                "ESC: Kembali ke Menu"
            ]
            
            for i, text in enumerate(instructions):
                draw_text(self.screen, text, self.font, (100, 100, 100),
                         (WINDOW_WIDTH//2, 400 + i * 30), center=True)
            
            pygame.display.flip()
            clock.tick(FPS)

class GameScreen:
    def __init__(self, screen, font, state):
        self.screen = screen
        self.font = font
        self.state = state
        
        self.level_config = LEVELS[self.state.level]
        self.time_left = self.level_config["waktu"]
        self.last_time = pygame.time.get_ticks()
        
        self.soal = None
        self.opsi = []
        self.buttons = []
        self.shape_img = None
        self.feedback = None
        self.feedback_time = 0
        
        self.correct_sound = None
        self.wrong_sound = None
        self.load_sounds()
        
        self.animations = {
            "shape": ScaleAnimation(0.5, 1, 500),
            "feedback": FadeAnimation(300)
        }
        
        self.new_question()
        
    def load_sounds(self):
        """Load sound effects"""
        try:
            # Create sounds directory if not exists
            if not os.path.exists("assets/sounds"):
                os.makedirs("assets/sounds")
                
            # Try to load from file
            sound_paths = {
                "correct": "assets/sounds/correct.wav",
                "wrong": "assets/sounds/wrong.wav"
            }
            
            # Create default sounds if files don't exist
            if not os.path.exists(sound_paths["correct"]):
                self.create_default_sounds()
            
            self.correct_sound = pygame.mixer.Sound(sound_paths["correct"])
            self.wrong_sound = pygame.mixer.Sound(sound_paths["wrong"])
            
        except:
            # Fallback to simple beeps
            self.correct_sound = self.create_beep_sound(800, 200)
            self.wrong_sound = self.create_beep_sound(300, 200)
    
    def create_default_sounds(self):
        """Create simple beep sounds"""
        correct = self.create_beep_sound(800, 200)
        wrong = self.create_beep_sound(300, 200)
        
        pygame.mixer.Sound.save(correct, "assets/sounds/correct.wav")
        pygame.mixer.Sound.save(wrong, "assets/sounds/wrong.wav")
    
    def create_beep_sound(self, frequency, duration):
        """Create a simple beep sound"""
        sample_rate = 44100
        n_samples = int(round(duration * 0.001 * sample_rate))
        
        buf = bytearray(n_samples * 2)
        
        for i in range(n_samples):
            t = float(i) / sample_rate
            sine = int(32767.0 * 0.5 * math.sin(2.0 * math.pi * frequency * t))
            
            # Convert to 16-bit signed
            buf[2*i] = sine & 0xff
            buf[2*i+1] = (sine >> 8) & 0xff
        
        return pygame.mixer.Sound(buffer=bytes(buf))
    
    def new_question(self):
        """Generate new question"""
        self.soal = generate_soal(BENTUK_LIST, WARNA_LIST)
        self.opsi = generate_opsi(
            self.soal, 
            BENTUK_LIST, 
            WARNA_LIST,
            jumlah=self.level_config["opsi"]
        )
        
        self.shape_img = draw_bentuk(
            self.soal.bentuk, 
            self.soal.warna, 
            280
        )
        
        self.create_buttons()
        self.animations["shape"].start()
    
    def create_buttons(self):
        """Create answer buttons"""
        self.buttons = []
        
        button_width = 400
        button_height = 50
        start_x = (WINDOW_WIDTH - button_width) // 2
        start_y = 400
        
        for i, opsi in enumerate(self.opsi):
            bentuk, warna = opsi
            text = f"{bentuk.upper()} - {warna.upper()}"
            
            btn = Button(
                rect=(start_x, start_y + i * 70, button_width, button_height),
                text=text,
                callback=lambda v=opsi: self.handle_answer(v),
                font=self.font,
                color=(255, 255, 255),
                hover_color=(230, 240, 255),
                border_radius=8
            )
            self.buttons.append(btn)
    
    def handle_answer(self, pilihan):
        """Handle user's answer"""
        if cek_jawaban(pilihan, self.soal):
            # Correct answer
            self.feedback = "✓ BENAR!"
            self.feedback_color = CORRECT_COLOR
            points = hitung_skor(self.time_left, self.level_config, self.state.streak)
            self.state.add_score(points)
            
            if self.correct_sound:
                self.correct_sound.play()
        else:
            # Wrong answer
            self.feedback = f"✗ SALAH! Jawaban: {self.soal.bentuk} - {self.soal.warna_name}"
            self.feedback_color = WRONG_COLOR
            self.state.break_streak()
            
            if self.wrong_sound:
                self.wrong_sound.play()
        
        self.feedback_time = pygame.time.get_ticks()
        self.animations["feedback"].start()
        
        # Next question after delay
        pygame.time.set_timer(pygame.USEREVENT, 1000)
    
    def update_timer(self):
        """Update game timer"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time >= 1000:
            self.time_left -= 1
            self.last_time = current_time
            
            if self.time_left <= 0:
                # Time's up!
                self.end_game()
    
    def end_game(self):
        """End current game"""
        self.state.save_score()
        return "game_over"
    
    def go_back(self):
        """Return to menu"""
        return "menu"
    
    def loop(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        # Back button
        back_btn = Button(
            rect=(20, 20, 100, 40),
            text="← Menu",
            callback=self.go_back,
            font=self.font
        )
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                
                if event.type == pygame.USEREVENT:
                    # Time for next question
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    self.new_question()
                    self.time_left = self.level_config["waktu"]
                
                # Handle back button
                if back_btn.handle_event(event):
                    return "menu"
                
                # Handle answer buttons
                for button in self.buttons:
                    button.handle_event(event)
            
            # Update
            self.update_timer()
            self.animations["shape"].update()
            
            # Check if time's up
            if self.time_left <= 0:
                return self.end_game()
            
            # Draw
            self.screen.fill(BACKGROUND)
            
            # Header
            draw_text(self.screen, "TEBAK BENTUK & WARNA", 
                     pygame.font.Font(None, 48), PRIMARY,
                     (WINDOW_WIDTH//2, 40), center=True)
            
            # Game info
            info_y = 80
            draw_text(self.screen, f"Level: {self.state.level.upper()}", 
                     self.font, TEXT_COLOR, (50, info_y))
            draw_score(self.screen, self.state.score, self.font, (WINDOW_WIDTH - 150, info_y))
            draw_streak(self.screen, self.state.streak, self.font, (WINDOW_WIDTH - 300, info_y))
            
            # Timer
            draw_timer(self.screen, self.time_left, self.font, (WINDOW_WIDTH//2, info_y))
            
            # Draw shape with animation
            if self.shape_img:
                scale = self.animations["shape"].update()
                img_width = int(self.shape_img.get_width() * scale)
                img_height = int(self.shape_img.get_height() * scale)
                scaled_img = pygame.transform.scale(self.shape_img, (img_width, img_height))
                
                pos_x = WINDOW_WIDTH//2 - img_width//2
                pos_y = 150
                
                self.screen.blit(scaled_img, (pos_x, pos_y))
            
            # Draw buttons
            for button in self.buttons:
                button.draw(self.screen)
            
            # Draw back button
            back_btn.draw(self.screen)
            
            # Draw feedback
            if self.feedback and pygame.time.get_ticks() - self.feedback_time < 1000:
                alpha = self.animations["feedback"].get_alpha()
                if alpha > 0:
                    feedback_font = pygame.font.Font(None, 36)
                    feedback_surf = feedback_font.render(self.feedback, True, self.feedback_color)
                    feedback_surf.set_alpha(alpha)
                    
                    pos = (WINDOW_WIDTH//2, 350)
                    rect = feedback_surf.get_rect(center=pos)
                    self.screen.blit(feedback_surf, rect)
            
            pygame.display.flip()
            clock.tick(FPS)

class HighScoreScreen:
    def __init__(self, screen, font, state):
        self.screen = screen
        self.font = font
        self.state = state
        self.scores = GameState.load_scores()
        
    def create_buttons(self):
        self.back_btn = Button(
            rect=(20, 20, 100, 40),
            text="← Kembali",
            callback=self.go_back,
            font=self.font
        )
        
        self.play_again_btn = Button(
            rect=(WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT - 100, 300, 50),
            text="MAIN LAGI",
            callback=self.play_again,
            font=self.font,
            color=(100, 200, 255)
        )
    
    def go_back(self):
        return "menu"
    
    def play_again(self):
        self.state.reset()
        return "kuis"
    
    def loop(self):
        self.create_buttons()
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "menu"
                
                if self.back_btn.handle_event(event):
                    return "menu"
                if self.play_again_btn.handle_event(event):
                    return "kuis"
            
            # Draw
            self.screen.fill(BACKGROUND)
            
            # Title
            draw_text(self.screen, "HIGH SCORES", 
                     pygame.font.Font(None, 64), PRIMARY,
                     (WINDOW_WIDTH//2, 80), center=True)
            
            # Draw scores table
            table_y = 180
            header_font = pygame.font.Font(None, 36)
            headers = ["Peringkat", "Nama", "Skor", "Level", "Tanggal"]
            
            # Draw headers
            for i, header in enumerate(headers):
                x = 100 + i * 180
                draw_text(self.screen, header, header_font, (100, 100, 200), (x, table_y))
            
            # Draw scores
            for idx, score_data in enumerate(self.scores[:10]):
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
                    draw_text(self.screen, text, self.font, color, (x, y))
            
            # If no scores
            if not self.scores:
                draw_text(self.screen, "Belum ada skor tercatat!", 
                         self.font, (150, 150, 150),
                         (WINDOW_WIDTH//2, 300), center=True)
            
            # Current score
            if self.state.score > 0:
                draw_text(self.screen, f"Skor Terakhir: {self.state.score}", 
                         pygame.font.Font(None, 48), (0, 200, 0),
                         (WINDOW_WIDTH//2, WINDOW_HEIGHT - 180), center=True)
            
            # Draw buttons
            self.back_btn.draw(self.screen)
            self.play_again_btn.draw(self.screen)
            
            pygame.display.flip()
            clock.tick(FPS)