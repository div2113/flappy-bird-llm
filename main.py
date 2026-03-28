import pygame
import sys
import math
import random
from settings import *
from bird import Bird
from pipes import PipeManager
from background import Background
from game_state import *
from sounds import SoundManager

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# --- FONTS ---
font_xl    = pygame.font.SysFont('Arial', 62, bold=True)
font_big   = pygame.font.SysFont('Arial', 48, bold=True)
font_med   = pygame.font.SysFont('Arial', 32, bold=True)
font_small = pygame.font.SysFont('Arial', 20, bold=True)
font_xs    = pygame.font.SysFont('Arial', 16)

# ─── PARTICLES ────────────────────────────────────────────
class Particle:
    def __init__(self, x, y, color=None, star=False):
        self.x = x
        self.y = y
        self.star = star
        self.color = color or (
            random.randint(180, 255),
            random.randint(180, 255),
            random.randint(50, 255)
        )
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-6, -1) if not star else random.uniform(-0.5, 0.5)
        self.life = random.randint(40, 90)
        self.max_life = self.life
        self.size = random.randint(3, 8)

    def update(self):
        self.x += self.vx
        self.vy += 0.15        # gravity on confetti
        self.y += self.vy
        self.life -= 1

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))
        r = max(1, int(self.size * (self.life / self.max_life)))
        if self.star:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), r)
        else:
            pygame.draw.rect(screen, self.color,
                             (int(self.x), int(self.y), r * 2, r))

# ─── HELPERS ──────────────────────────────────────────────
def draw_text_center(text, font, color, y, shadow=True, shadow_color=(0,0,0)):
    if shadow:
        s = font.render(text, True, shadow_color)
        screen.blit(s, (SCREEN_WIDTH//2 - s.get_width()//2 + 3, y + 3))
    surf = font.render(text, True, color)
    screen.blit(surf, (SCREEN_WIDTH//2 - surf.get_width()//2, y))

def draw_rounded_panel(x, y, w, h, color, alpha=180, radius=18):
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(surf, (*color, alpha), (0, 0, w, h), border_radius=radius)
    screen.blit(surf, (x, y))

def get_medal(score):
    if score >= 40: return "🏆 PLATINUM", (220, 240, 255)
    if score >= 20: return "🥇 GOLD",     (255, 220, 50)
    if score >= 10: return "🥈 SILVER",   (210, 210, 210)
    if score >= 5:  return "🥉 BRONZE",   (200, 130, 60)
    return None, None

def draw_glow(surface, color, x, y, radius, intensity=80):
    for r in range(radius, 0, -8):
        alpha = int(intensity * (r / radius))
        glow = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(glow, (*color, alpha), (r, r), r)
        surface.blit(glow, (x - r, y - r))

# ─── OBJECTS ──────────────────────────────────────────────
def reset_game():
    return Bird(), PipeManager(), 0

bird, pipe_manager, score = reset_game()
background = Background()
sounds = SoundManager()

# ─── STATE ────────────────────────────────────────────────
state       = START
high_score  = 0
timer       = 0
is_new_best = False

# Start screen demo bird
demo_bird_x   = -40
demo_bird_y   = 260
demo_bird_vy  = 0

# Particles
particles = []

# Confetti colors
CONFETTI = [
    (255,80,80),(80,255,80),(80,160,255),
    (255,220,50),(255,120,200),(120,255,220)
]

# Screen shake
shake_frames  = 0
shake_intensity = 0

# ─── STAR PARTICLES on start screen ───────────────────────
star_particles = [Particle(random.randint(0, SCREEN_WIDTH),
                            random.randint(0, SCREEN_HEIGHT - 100),
                            color=(255,255,220), star=True)
                  for _ in range(30)]

# ─── GAME LOOP ────────────────────────────────────────────
running = True
while running:
    timer += 1

    # ── EVENTS ──
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if state == START and event.key == pygame.K_SPACE:
                state = PLAYING
            elif state == PLAYING and event.key == pygame.K_SPACE:
                bird.jump()
                sounds.play_flap()
            elif state == GAME_OVER and event.key == pygame.K_SPACE:
                bird, pipe_manager, score = reset_game()
                particles.clear()
                is_new_best = False
                state = PLAYING

    # ── UPDATE ──
    background.update()

    # Star particles (start screen ambience)
    for p in star_particles:
        p.x += 0.2
        if p.x > SCREEN_WIDTH:
            p.x = 0
            p.y = random.randint(0, SCREEN_HEIGHT - 100)

    # Confetti/explosion particles
    particles = [p for p in particles if p.life > 0]
    for p in particles:
        p.update()

    # Screen shake countdown
    if shake_frames > 0:
        shake_frames -= 1

    # Demo bird on start screen
    if state == START:
        demo_bird_vy += 0.3
        demo_bird_y  += demo_bird_vy
        demo_bird_x  += 2.5
        if demo_bird_y > SCREEN_HEIGHT - GROUND_HEIGHT - 34 or demo_bird_y < 60:
            demo_bird_vy = -5
        if demo_bird_x > SCREEN_WIDTH + 60:
            demo_bird_x = -40
            demo_bird_y = 260

    if state == PLAYING:
        bird.update()
        pipe_manager.update()

        for pipe in pipe_manager.pipes:
            if not pipe['scored'] and bird.x > pipe['x'] + PIPE_WIDTH:
                score += 1
                pipe['scored'] = True
                sounds.play_score()
                # Score burst
                for _ in range(10):
                    particles.append(Particle(
                        bird.x + 17, int(bird.y) + 17,
                        color=random.choice(CONFETTI)
                    ))

        bird_rect = pygame.Rect(bird.x+4, int(bird.y)+4,
                                bird.size-8, bird.size-8)
        for pipe in pipe_manager.pipes:
            top_r = pygame.Rect(pipe['x'], 0, PIPE_WIDTH, pipe['gap_y'])
            bot_r = pygame.Rect(pipe['x'], pipe['gap_y']+PIPE_GAP,
                                PIPE_WIDTH, SCREEN_HEIGHT)
            if bird_rect.colliderect(top_r) or bird_rect.colliderect(bot_r):
                is_new_best = score > high_score
                if is_new_best: 
                    high_score = score
                    sounds.play_best()
                else:
                    sounds.play_hit() 
                shake_frames = 18
                # Death explosion
                for _ in range(40):
                    particles.append(Particle(
                        bird.x+17, int(bird.y)+17,
                        color=random.choice(CONFETTI)
                    ))
                state = GAME_OVER

        if bird.y >= SCREEN_HEIGHT - GROUND_HEIGHT - bird.size:
            is_new_best = score > high_score
            if is_new_best: 
                high_score = score
                sounds.play_best()
            else:
                sounds.play_hit()
            shake_frames = 18
            for _ in range(40):
                particles.append(Particle(
                    bird.x+17, int(bird.y)+17,
                    color=random.choice(CONFETTI)
                ))
            state = GAME_OVER

    # ── DRAW ──
    # Screen shake offset
    ox = random.randint(-shake_intensity, shake_intensity) if shake_frames > 0 else 0
    oy = random.randint(-shake_intensity, shake_intensity) if shake_frames > 0 else 0
    shake_intensity = shake_frames * 0 + (3 if shake_frames > 0 else 0)

    background.draw(screen)

    # Star particles
    for p in star_particles:
        r = random.randint(1, 3)
        pygame.draw.circle(screen, (255, 255, 200),
                           (int(p.x), int(p.y)), r)

    pipe_manager.draw(screen)

    # Ground
    pygame.draw.rect(screen, GROUND_COLOR,
                     (ox, SCREEN_HEIGHT - GROUND_HEIGHT + oy,
                      SCREEN_WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(screen, GRASS_COLOR,
                     (ox, SCREEN_HEIGHT - GROUND_HEIGHT + oy,
                      SCREEN_WIDTH, 15))
    for i in range(0, SCREEN_WIDTH, 20):
        pygame.draw.polygon(screen, (80,160,60), [
            (i+ox,      SCREEN_HEIGHT - GROUND_HEIGHT + 15 + oy),
            (i+5+ox,    SCREEN_HEIGHT - GROUND_HEIGHT + 5  + oy),
            (i+10+ox,   SCREEN_HEIGHT - GROUND_HEIGHT + 15 + oy)
        ])

    # Particles
    for p in particles:
        p.draw(screen)

    bird.draw(screen)

    # ════════════════════════════════════════
    #  START SCREEN
    # ════════════════════════════════════════
    if state == START:

        # Demo bird flying
        temp_bird = Bird()
        temp_bird.x  = demo_bird_x
        temp_bird.y  = demo_bird_y
        temp_bird.draw(screen)

        # Top glow bar
        glow_bar = pygame.Surface((SCREEN_WIDTH, 6), pygame.SRCALPHA)
        pulse = int(abs(math.sin(timer * 0.04)) * 255)
        glow_bar.fill((255, 220, 50, pulse))
        screen.blit(glow_bar, (0, 130))

        # Title panel
        draw_rounded_panel(20, 135, SCREEN_WIDTH-40, 210,
                           (10, 20, 50), alpha=200)

        # Glowing title
        glow_r = int(abs(math.sin(timer * 0.05)) * 20) + 5
        draw_glow(screen, (255,200,0), SCREEN_WIDTH//2, 175, glow_r+30, 60)
        draw_text_center("FLAPPY", font_xl, (255, 230, 0), 148,
                         shadow_color=(180,100,0))
        draw_text_center("BIRD",   font_xl, (255, 160, 30), 205,
                         shadow_color=(150,70,0))

        # Divider
        pygame.draw.line(screen, (255,200,50,180),
                         (50, 268), (SCREEN_WIDTH-50, 268), 2)

        # Pulse button
        btn_alpha = int(abs(math.sin(timer * 0.06)) * 120) + 100
        draw_rounded_panel(70, 278, SCREEN_WIDTH-140, 42,
                           (50,200,50), alpha=btn_alpha)
        draw_text_center("▶  PRESS SPACE TO FLY", font_small,
                         (220,255,220), 288, shadow=False)

        # Hint
        draw_text_center("dodge the pipes · survive · be legend",
                         font_xs, (180,220,255), 340, shadow=False)

    # ════════════════════════════════════════
    #  PLAYING — HUD
    # ════════════════════════════════════════
    elif state == PLAYING:
        # Score pill
        pill = pygame.Surface((90, 44), pygame.SRCALPHA)
        pygame.draw.rect(pill, (0,0,0,120), (0,0,90,44), border_radius=22)
        screen.blit(pill, (SCREEN_WIDTH//2 - 45, 20))
        draw_text_center(str(score), font_med, WHITE, 28)

    # ════════════════════════════════════════
    #  GAME OVER SCREEN
    # ════════════════════════════════════════
    elif state == GAME_OVER:

        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Main panel
        draw_rounded_panel(80, SCREEN_HEIGHT-200,
                           SCREEN_WIDTH-40, SCREEN_HEIGHT-180,
                           (15, 10, 30), alpha=220)

        # GAME OVER title — pulse red
        pulse_r = int(abs(math.sin(timer * 0.08)) * 40) + 215
        draw_text_center("GAME OVER", font_big,
                         (pulse_r, 50, 50), 95)

        # New best flash
        if is_new_best:
            flash = int(abs(math.sin(timer * 0.15)) * 255)
            draw_text_center("✨ NEW BEST! ✨", font_small,
                             (flash, 255, 100), 148)

        # Divider
        pygame.draw.line(screen, (180,50,50),
                         (50, 170), (SCREEN_WIDTH-50, 170), 2)

        # Score card
        draw_rounded_panel(60, 178, SCREEN_WIDTH-120, 50,
                           (30,30,60), alpha=200)
        draw_text_center(f"SCORE    {score}", font_med,
                         WHITE, 190)

        draw_rounded_panel(60, 236, SCREEN_WIDTH-120, 40,
                           (40,35,10), alpha=180)
        draw_text_center(f"BEST      {high_score}", font_small,
                         (255,220,80), 248)

        # Medal
        medal_text, medal_color = get_medal(score)
        if medal_text:
            draw_rounded_panel(60, 284, SCREEN_WIDTH-120, 36,
                               (20,40,20), alpha=180)
            draw_text_center(medal_text, font_small,
                             medal_color, 293)

        # Restart button — pulse green
        btn_alpha = int(abs(math.sin(timer * 0.07)) * 100) + 120
        draw_rounded_panel(70, 332, SCREEN_WIDTH-140, 40,
                           (30,160,30), alpha=btn_alpha)
        draw_text_center("▶  SPACE to restart", font_small,
                         (220,255,220), 342, shadow=False)

        draw_text_center("ESC to quit", font_xs,
                         (160,160,160), 385, shadow=False)

    # ── FLIP ──
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()