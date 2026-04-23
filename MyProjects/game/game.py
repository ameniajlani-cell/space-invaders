import pygame
import random
from player import Player
from enemy import Enemy
from bullet import Bullet

# ============================================================================
# Color Constants for consistency across the game
# ============================================================================
COLOR_PRIMARY = (0, 255, 200)      # Cyan - Primary accent color
COLOR_SECONDARY = (255, 100, 200)  # Magenta - Secondary accent
COLOR_BACKGROUND = (15, 15, 30)    # Dark blue - Background
COLOR_DANGER = (255, 80, 80)       # Red - Danger/Game Over
COLOR_TEXT = (255, 255, 255)       # White - Main text
COLOR_DARK_BG = (10, 10, 20)       # Very dark blue - Darker elements

PLAYER_WIDTH = 30
PLAYER_GAP = 10

class Game:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Space Invaders")

        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        self.max_waves = 1     # selected wave limit (1–5)
        self.selected_waves = 1


        
        # Animation frame counter for subtle animations
        self.frame_count = 0

        self.background = pygame.image.load(r"C:\Users\amani\Desktop\MyProjects\MyProjects\game\background.png").convert()
        self.background = pygame.transform.scale(self.background, (800, 600))

        pygame.mixer.init()
        self.shoot_sound = pygame.mixer.Sound(r"C:\Users\amani\Desktop\MyProjects\MyProjects\game\shoot.wav")
        self.shoot_sound.set_volume(0.2)


        self.player1 = Player(375, 520)
        self.player2 = Player(200, 520)  # Second player at different position
        self.player2_active = False  # Flag to check if second player is active

        self.enemies = []
        self.wave_number = 1
        self.enemy_speed = 2
        self.enemy_descent = 0.2
        self.enemy_count = 8

        self.spawn_enemies()
        self.bullets = []

        self.p1_score = 0
        self.p2_score = 0
        self.p1_lives = 3
        self.p2_lives = 3

    def menu(self):
        """Main menu screen with single/multiplayer selection."""
        font_big = pygame.font.SysFont("Consolas", 60, bold=True)
        font_small = pygame.font.SysFont("Consolas", 35, bold=True)
    
        # Button rectangles
        single_rect = pygame.Rect(250, 250, 300, 50)
        multi_rect = pygame.Rect(250, 320, 300, 50)
    
        while True:
            self.win.blit(self.background, (0, 0))
    
            # Title with accent color
            title_text = font_big.render("SPACE INVADERS", True, COLOR_PRIMARY)
            self.win.blit(title_text, (150, 120))
    
            mouse_pos = pygame.mouse.get_pos()
    
            # Button hover effects with color constants
            single_color = (60, 60, 120) if single_rect.collidepoint(mouse_pos) else COLOR_BACKGROUND
            multi_color = (60, 60, 120) if multi_rect.collidepoint(mouse_pos) else COLOR_BACKGROUND
    
            # Draw buttons
            pygame.draw.rect(self.win, single_color, single_rect)
            pygame.draw.rect(self.win, multi_color, multi_rect)
            
            # Draw button borders
            pygame.draw.rect(self.win, COLOR_PRIMARY, single_rect, 2)
            pygame.draw.rect(self.win, COLOR_PRIMARY, multi_rect, 2)
    
            single_text = font_small.render("SINGLE PLAYER", True, COLOR_PRIMARY)
            multi_text = font_small.render("MULTIPLAYER", True, COLOR_PRIMARY)
            self.win.blit(single_text, single_text.get_rect(center=single_rect.center))
            self.win.blit(multi_text, multi_text.get_rect(center=multi_rect.center))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Keyboard selection
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.player2_active = False
                        return
                    if event.key == pygame.K_2:
                        self.player2_active = True
                        return

                # Mouse selection
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if single_rect.collidepoint(event.pos):
                        self.player2_active = False
                        return
                    if multi_rect.collidepoint(event.pos):
                        self.player2_active = True
                        return

    def spawn_enemies(self):
        self.enemies.clear()
        for _ in range(self.enemy_count):
            x = random.randint(60, 740)
            y = random.randint(40, 200)
            skin = random.choice(["MyProjects\\game\\enemy1.png", "MyProjects\\game\\enemy2.png"])
            self.enemies.append(Enemy(x, y, skin,self.enemy_speed,self.enemy_descent))


    def wave_selection_menu(self):
        font_title = pygame.font.SysFont("Consolas", 50, bold=True)
        font_btn = pygame.font.SysFont("Consolas", 28, bold=True)

        buttons = []
        for i in range(1, 6):
            rect = pygame.Rect(140 + (i - 1) * 110, 250, 90, 50)
            buttons.append((i, rect))

        start_rect = pygame.Rect(300, 350, 200, 55)

        while True:
            self.win.blit(self.background, (0, 0))

            title = font_title.render("SELECT NUMBER OF WAVES", True, COLOR_PRIMARY)
            self.win.blit(title, (110, 120))

            mouse_pos = pygame.mouse.get_pos()

            # Wave buttons
            for wave, rect in buttons:
                color = COLOR_PRIMARY if wave == self.selected_waves else COLOR_BACKGROUND
                pygame.draw.rect(self.win, color, rect, 2)
                text = font_btn.render(str(wave), True, COLOR_PRIMARY)
                self.win.blit(text, text.get_rect(center=rect.center))

            # Start button
            start_color = COLOR_SECONDARY if start_rect.collidepoint(mouse_pos) else COLOR_BACKGROUND
            pygame.draw.rect(self.win, start_color, start_rect, 2)
            start_text = font_btn.render("START", True, COLOR_SECONDARY)
            self.win.blit(start_text, start_text.get_rect(center=start_rect.center))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    for wave, rect in buttons:
                        if rect.collidepoint(event.pos):
                            self.selected_waves = wave

                    if start_rect.collidepoint(event.pos):
                        self.max_waves = self.selected_waves
                        return


    def run(self):
        self.menu()
        self.wave_selection_menu()
        while self.running:
            self.clock.tick(60)
            self.events()
            self.update()
            self.draw()
        if self.game_over:
            self.game_over_screen()
        pygame.quit()


    def game_over_screen(self):
        """Game Over screen with score display and restart options."""
        font_big = pygame.font.SysFont("Consolas", 60, bold=True)
        font_small = pygame.font.SysFont("Consolas", 35, bold=True)


        if self.player2_active:
            if self.p1_score > self.p2_score:
                winner = "PLAYER 1 WINS"
            elif self.p2_score > self.p1_score:
                winner = "PLAYER 2 WINS"
            else:
                winner = "DRAW"
        else:
            winner = "GAME OVER"


        # Button rectangles
        replay_rect = pygame.Rect(250, 350, 300, 50)
        quit_rect = pygame.Rect(250, 420, 300, 50)

        while True:
            self.win.blit(self.background, (0, 0))

            # Game Over Text with danger color
            game_over_text = font_big.render("GAME OVER", True, COLOR_DANGER)
            self.win.blit(game_over_text, (250, 150))

            winner_text = font_big.render(self.winner, True, COLOR_PRIMARY)
            self.win.blit(winner_text, (200, 190))

            # Score Display with primary color
            score_text = font_small.render(f"FINAL SCORE: {self.p1_score} - {self.p2_score}", True, COLOR_PRIMARY)
            self.win.blit(score_text, (270, 250))

            # Get mouse position for button hover effects
            mouse_pos = pygame.mouse.get_pos()
            replay_color = (60, 60, 120) if replay_rect.collidepoint(mouse_pos) else COLOR_BACKGROUND
            quit_color = (60, 60, 120) if quit_rect.collidepoint(mouse_pos) else COLOR_BACKGROUND

            # Draw buttons
            pygame.draw.rect(self.win, replay_color, replay_rect)
            pygame.draw.rect(self.win, quit_color, quit_rect)
            
            # Draw button borders
            pygame.draw.rect(self.win, COLOR_PRIMARY, replay_rect, 2)
            pygame.draw.rect(self.win, COLOR_PRIMARY, quit_rect, 2)

            replay_text = font_small.render("PLAY AGAIN", True, COLOR_PRIMARY)
            quit_text = font_small.render("QUIT", True, COLOR_PRIMARY)

            self.win.blit(replay_text, replay_text.get_rect(center=replay_rect.center))
            self.win.blit(quit_text, quit_text.get_rect(center=quit_rect.center))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if replay_rect.collidepoint(event.pos):
                        self.__init__()     # Restart the whole game
                        self.run()
                        return

                    if quit_rect.collidepoint(event.pos):
                        pygame.quit()
                        return
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.bullets.append(Bullet(self.player1.x + 23, self.player1.y))
                    self.shoot_sound.play()
                if event.key == pygame.K_LCTRL:  # Left control for player 2 shooting
                    if self.player2_active:
                        self.bullets.append(Bullet(self.player2.x + 23, self.player2.y))
                        self.shoot_sound.play()

    def update(self):
        keys = pygame.key.get_pressed()
        # Player 1
        if keys[pygame.K_LEFT] and self.player1.x > 10:
            self.player1.x -= 5

        if keys[pygame.K_RIGHT]:
            if self.player2_active:
                limit = self.player2.x - PLAYER_WIDTH - PLAYER_GAP
            else:
                limit = 740

            if self.player1.x < limit:
                self.player1.x += 5

        # Player 2
        if self.player2_active:
            if keys[pygame.K_a] and self.player2.x > self.player1.x + PLAYER_WIDTH + PLAYER_GAP:
                self.player2.x -= 5

            if keys[pygame.K_d] and self.player2.x < 740:
                self.player2.x += 5

        for bullet in self.bullets[:]:
            bullet.y -= 8
            if bullet.y < 0:
                self.bullets.remove(bullet)

        for enemy in self.enemies[:]:
            enemy.move()
            
            if enemy.y > 580:
                self.enemies.remove(enemy)
                continue

            for bullet in self.bullets[:]:
                if enemy.rect().colliderect(bullet.rect()):
                    self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    if bullet.x < 400:  # Assuming player 1's bullets are on the left half
                        self.p1_score += 1
                    else:  # Player 2's bullets are on the right half
                        self.p2_score += 1

        if enemy.rect().colliderect(self.player1.rect()):
            self.p1_lives -= 1
            self.enemies.remove(enemy)

        if self.player2_active and enemy.rect().colliderect(self.player2.rect()):
            self.p2_lives -= 1
            self.enemies.remove(enemy)

        if self.p1_lives <= 0:
            if self.player2_active:
                self.winner = "PLAYER 2 WINS"
            else:
                self.winner = "GAME OVER"

            self.running = False
            self.game_over = True
            return
        
        if self.player2_active and self.p2_lives <= 0:
            self.winner = "PLAYER 1 WINS"
            self.running = False
            self.game_over = True
            return

        if len(self.enemies) < self.enemy_count:
            self.spawn_enemies()

        if len(self.enemies) == 0 :
            if self.wave_number >= self.max_waves:
                self.running = False
                self.game_over = True
                return
            self.wave_number += 1
            self.enemy_count += 2
            self.enemy_speed += 0.5
            self.enemy_descent += 0.1
            self.spawn_enemies()

    # ========================================================================
    # HUD Drawing with improved aesthetics
    # ========================================================================
    def draw_hud(self):
    # HUD dimensions
        HUD_HEIGHT = 70
        WIDTH = 800

        # --- Background transparent HUD bar ---
        hud_surface = pygame.Surface((WIDTH, HUD_HEIGHT), pygame.SRCALPHA)
        hud_surface.fill((10, 10, 30, 200))  # Dark with alpha
        self.win.blit(hud_surface, (0, 0))

        # Bottom separator line
        pygame.draw.line(
            self.win, COLOR_PRIMARY,
            (0, HUD_HEIGHT - 2), (WIDTH, HUD_HEIGHT - 2), 2
        )

        # Fonts
        font_main = pygame.font.SysFont("Consolas", 26, bold=True)
        font_secondary = pygame.font.SysFont("Consolas", 16)

        # --- LEFT: SCORE ---

        font_main = pygame.font.SysFont("Consolas", 26, bold=True)

        # Player 1
        p1_text = font_main.render(
            f"P1 {self.p1_score}  {'♡' * self.p1_lives}",
            True,
            COLOR_PRIMARY
        )
        self.win.blit(p1_text, (20, 12))

        # Player 2
        if self.player2_active:
            p2_text = font_main.render(
                f"P2 {self.p2_score}  {'♡' * self.p2_lives}",
                True,
                COLOR_SECONDARY
            )
            self.win.blit(p2_text, (20, 42))



        # --- CENTER: WAVE ---
        wave_text = font_main.render(f"WAVE {self.wave_number}", True, COLOR_PRIMARY)
        wave_rect = wave_text.get_rect(center=(WIDTH // 2, 22))
        self.win.blit(wave_text, wave_rect)

        # --- RIGHT: LIVES (simple indicator for now) ---
        lives_text = font_main.render("", True, COLOR_DANGER)
        self.win.blit(lives_text, (WIDTH - 120, 12))

        # --- SECOND ROW: CONTROLS (dimmed) ---
        if self.player2_active:
            controls = "P1: ◄ ► SPACE    P2: A / D  CTRL"
            control_color = COLOR_SECONDARY
        else:
            controls = "◄ ► MOVE    SPACE TO SHOOT"
            control_color = COLOR_TEXT

        controls_text = font_secondary.render(controls, True, control_color)
        controls_rect = controls_text.get_rect(center=(WIDTH // 2, 48))
        self.win.blit(controls_text, controls_rect)
    def draw(self):
        # Increment animation frame counter
        self.frame_count = (self.frame_count + 1) % 360  # Cycle every 6 seconds at 60 FPS
        
        # Draw background
        self.win.blit(self.background, (0, 0))
        
        # Draw improved HUD
        self.draw_hud()
        
        # Draw game entities
        self.player1.draw(self.win)
        if self.player2_active:
            self.player2.draw(self.win)

        for enemy in self.enemies:
            enemy.draw(self.win)

        for bullet in self.bullets:
            bullet.draw(self.win)

        pygame.display.update()