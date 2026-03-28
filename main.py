import pygame
import sys
from settings import *
from bird import Bird

# --- INIT ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

#--Create Bird --

bird = Bird()

# --- GAME LOOP ---
running = True
while running:

    # 1. EVENTS — listen for quit / keypresses
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                bird.jump()   # spacebar = jump!
            if event.key == pygame.K_ESPACE:
                running = False

    #2.UPDATE
    bird.update()

    #3. DRAW
    screen.fill(SKY_BLUE)

    #Ground
    pygame.draw.rect(screen, GROUND_COLOR,
                    (0,SCREEN_HEIGHT - GROUND_HEIGHT,
                    SCREEN_WIDTH ,GROUND_HEIGHT))

    
    # Grass strip
    pygame.draw.rect(screen, GRASS_COLOR,
                     (0, SCREEN_HEIGHT - GROUND_HEIGHT,
                      SCREEN_WIDTH, 15))

    bird.draw(screen)

    # FLIP + TICK 
    pygame.display.flip()
    clock.tick(FPS)

# --- QUIT ---
pygame.quit()
sys.exit()