import pygame
import random
from settings import *

class PipeManager:
    def __init__(self):
        self.pipes = []              # list of all active pipes
        self.spawn_timer = 0         # counts frames until next pipe
        self.spawn_interval = 90     # spawn new pipe every 90 frames
        self.speed = PIPE_SPEED      # how fast pipes move left

    def spawn_pipe(self):
        # Random gap position
        gap_y = random.randint(150, SCREEN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 50)

        self.pipes.append({
            'x': SCREEN_WIDTH + 10,  # start just off right edge
            'gap_y': gap_y,          # top of the gap
            'scored': False          # have we counted this pipe yet?
        })

    def update(self):
        # Spawn timer
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_pipe()
            self.spawn_timer = 0

        # Move all pipes left
        for pipe in self.pipes:
            pipe['x'] -= self.speed

        # Remove pipes that have gone off screen
        self.pipes = [p for p in self.pipes if p['x'] > -PIPE_WIDTH]

    def draw(self, screen):
        for pipe in self.pipes:
            # Top pipe
            top_rect = pygame.Rect(
                pipe['x'], 0,
                PIPE_WIDTH, pipe['gap_y']
            )
            pygame.draw.rect(screen, PIPE_COLOR, top_rect)
            pygame.draw.rect(screen, PIPE_DARK, top_rect, 3)  # outline

            # Bottom pipe
            bottom_y = pipe['gap_y'] + PIPE_GAP
            bottom_rect = pygame.Rect(
                pipe['x'], bottom_y,
                PIPE_WIDTH, SCREEN_HEIGHT - bottom_y
            )
            pygame.draw.rect(screen, PIPE_COLOR, bottom_rect)
            pygame.draw.rect(screen, PIPE_DARK, bottom_rect, 3)  # outline

            # Pipe caps (the little ledge on top/bottom of pipes)
            cap_rect_top = pygame.Rect(
                pipe['x'] - 5, pipe['gap_y'] - 20,
                PIPE_WIDTH + 10, 20
            )
            cap_rect_bottom = pygame.Rect(
                pipe['x'] - 5, bottom_y,
                PIPE_WIDTH + 10, 20
            )
            pygame.draw.rect(screen, PIPE_COLOR, cap_rect_top)
            pygame.draw.rect(screen, PIPE_COLOR, cap_rect_bottom)
            pygame.draw.rect(screen, PIPE_DARK, cap_rect_top, 3)
            pygame.draw.rect(screen, PIPE_DARK, cap_rect_bottom, 3)