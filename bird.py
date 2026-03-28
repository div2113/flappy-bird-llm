import pygame
from settings import *

class Bird:
    def __init__(self):
        self.x = 80                        # fixed horizontal position
        self.y = SCREEN_HEIGHT // 2        # start in middle of screen
        self.velocity = 0                  # not moving at start
        self.size = 30                     # bird size

    def jump(self):
        self.velocity = JUMP_FORCE         # shoot upward

    def update(self):
        self.velocity += GRAVITY           # gravity pulls down every frame
        self.y += self.velocity            # move bird by current velocity

        # Floor boundary — don't fall through ground
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.size
            self.velocity = 0

        # Ceiling boundary — don't fly off top
        if self.y <= 0:
            self.y = 0
            self.velocity = 0

    def draw(self, screen):
        cx = self.x + self.size // 2       # center x
        cy = int(self.y) + self.size // 2  # center y

        # Body
        pygame.draw.circle(screen, YELLOW, (cx, cy), self.size // 2)

        # Eye
        pygame.draw.circle(screen, WHITE, (cx + 7, cy - 5), 6)
        pygame.draw.circle(screen, BLACK, (cx + 9, cy - 5), 3)

        # Beak
        pygame.draw.polygon(screen, ORANGE, [
            (cx + 12, cy),
            (cx + 20, cy - 3),
            (cx + 12, cy + 5)
        ])

        # Wing
        pygame.draw.ellipse(screen, DARK_YELLOW,
                            (cx - 12, cy, 18, 10))