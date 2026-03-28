import pygame
import sys
from settings import *
from bird import Bird
from pipes import PipeManager
from game_state import *

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# --- FONTS ---
font_big   = pygame.font.SysFont('Arial', 52, bold=True)
font_med   = pygame.font.SysFont('Arial', 36, bold=True)
font_small = pygame.font.SysFont('Arial', 24)

# --- HELPERS ---
def draw_text_center(text, font, color, y):
    surface = font.render(text, True, color)
    x = SCREEN_WIDTH // 2 - surface.get_width() // 2
    screen.blit(surface, (x, y))

def reset_game():
    return Bird(), PipeManager(), 0

# --- OBJECTS ---
bird, pipe_manager, score = reset_game()

# --- STATE ---
state = START

# --- GAME LOOP ---
running = True
while running:

    # 1. EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            # START screen → press Space to play
            if state == START:
                if event.key == pygame.K_SPACE:
                    state = PLAYING

            # PLAYING → Space to jump
            elif state == PLAYING:
                if event.key == pygame.K_SPACE:
                    bird.jump()

            # GAME OVER → Space to restart
            elif state == GAME_OVER:
                if event.key == pygame.K_SPACE:
                    bird, pipe_manager, score = reset_game()
                    state = PLAYING

    # 2. UPDATE (only when playing)
    if state == PLAYING:
        bird.update()
        pipe_manager.update()

        # Scoring
        for pipe in pipe_manager.pipes:
            if not pipe['scored'] and bird.x > pipe['x'] + PIPE_WIDTH:
                score += 1
                pipe['scored'] = True

        # Collision — pipes
        bird_rect = pygame.Rect(bird.x, int(bird.y), bird.size, bird.size)
        for pipe in pipe_manager.pipes:
            top_rect    = pygame.Rect(pipe['x'], 0, PIPE_WIDTH, pipe['gap_y'])
            bottom_rect = pygame.Rect(pipe['x'], pipe['gap_y'] + PIPE_GAP,
                                      PIPE_WIDTH, SCREEN_HEIGHT)
            if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                state = GAME_OVER

        # Collision — ground
        if bird.y >= SCREEN_HEIGHT - GROUND_HEIGHT - bird.size:
            state = GAME_OVER

    # 3. DRAW
    screen.fill(SKY_BLUE)

    pipe_manager.draw(screen)

    # Ground
    pygame.draw.rect(screen, GROUND_COLOR,
                     (0, SCREEN_HEIGHT - GROUND_HEIGHT,
                      SCREEN_WIDTH, GROUND_HEIGHT))
    pygame.draw.rect(screen, GRASS_COLOR,
                     (0, SCREEN_HEIGHT - GROUND_HEIGHT,
                      SCREEN_WIDTH, 15))

    bird.draw(screen)

    # --- START SCREEN ---
    if state == START:
        # Dark overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))

        draw_text_center("🐦 FLAPPY BIRD", font_big, YELLOW, 180)
        draw_text_center("Press SPACE to Start", font_small, WHITE, 280)
        draw_text_center("Press ESC to Quit", font_small, WHITE, 315)

    # --- PLAYING --- show score
    elif state == PLAYING:
        draw_text_center(str(score), font_med, WHITE, 40)

    # --- GAME OVER SCREEN ---
    elif state == GAME_OVER:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))

        draw_text_center("GAME OVER", font_big, (220, 50, 50), 160)
        draw_text_center(f"Score: {score}", font_med, WHITE, 250)
        draw_text_center("Press SPACE to Restart", font_small, WHITE, 320)
        draw_text_center("Press ESC to Quit", font_small, WHITE, 355)

    # 4. FLIP + TICK
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()