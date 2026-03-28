import pygame
import sys
from settings import *
from bird import Bird
from pipes import PipeManager

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

#objects

bird = Bird()
pipe_manager = PipeManager()

#SCORE
score=0
font=pygame.font.SysFont('Arial',36,bold=True)

# --- GAME LOOP ---
running = True
while running:

    # 1. EVENTS — listen for quit / keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()   # spacebar = jump!
            if event.key == pygame.K_ESCAPE:
                running = False

    #2.UPDATE
    bird.update()
    pipe_manager.update()

     # --- SCORE: did bird pass a pipe? ---
    for pipe in pipe_manager.pipes:
        if not pipe['scored'] and bird.x > pipe['x'] + PIPE_WIDTH:
            score += 1
            pipe['scored'] = True

     # --- COLLISION DETECTION ---
    bird_rect = pygame.Rect(bird.x, int(bird.y), bird.size, bird.size)

    for pipe in pipe_manager.pipes:
        top_rect = pygame.Rect(pipe['x'], 0, PIPE_WIDTH, pipe['gap_y'])
        bottom_rect = pygame.Rect(pipe['x'], pipe['gap_y'] + PIPE_GAP,
                                  PIPE_WIDTH, SCREEN_HEIGHT)
        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            print("GAME OVER!")   # we'll make this a screen in Phase 4
            running = False

    # Bird hits ground
    if bird.y >= SCREEN_HEIGHT - GROUND_HEIGHT - bird.size:
        print("GAME OVER!")
        running = False


    #3. DRAW
    screen.fill(SKY_BLUE)

    pipe_manager.draw(screen)

    #Ground
    pygame.draw.rect(screen, GROUND_COLOR,
                    (0,SCREEN_HEIGHT - GROUND_HEIGHT,
                    SCREEN_WIDTH ,GROUND_HEIGHT))

    
    # Grass strip
    pygame.draw.rect(screen, GRASS_COLOR,
                     (0, SCREEN_HEIGHT - GROUND_HEIGHT,
                      SCREEN_WIDTH, 15))

    bird.draw(screen)

     # Score display
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 40))

    # FLIP + TICK 
    pygame.display.flip()
    clock.tick(FPS)

# --- QUIT ---
pygame.quit()
sys.exit()