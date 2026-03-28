import pygame
import math
from settings import *

class Bird:
    def __init__(self):
        self.x = 80
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = 34
        self.flap_offset = 0        # wing animation
        self.flap_timer = 0         # controls animation speed
        self.alive = True

    def jump(self):
        self.velocity = JUMP_FORCE
        self.flap_offset = -8       # wing flap on jump

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        # Wing animation — smoothly returns to 0
        self.flap_timer += 1
        if self.flap_offset < 0:
            self.flap_offset += 0.8  # bounce back slowly

        # Floor
        if self.y >= SCREEN_HEIGHT - GROUND_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - GROUND_HEIGHT - self.size
            self.velocity = 0

        # Ceiling
        if self.y <= 0:
            self.y = 0
            self.velocity = 0

    def draw(self, screen):
        cx = int(self.x + self.size // 2)
        cy = int(self.y + self.size // 2)

        # Tilt bird based on velocity
        tilt = max(-30, min(self.velocity * 3, 90))

        # Shadow
        pygame.draw.ellipse(screen, (0, 0, 0, 60),
                            (cx - 16, cy + 14, 32, 10))

        # Body
        pygame.draw.circle(screen, (255, 220, 0), (cx, cy), 17)

        # Belly
        pygame.draw.ellipse(screen, (255, 240, 180),
                            (cx - 8, cy + 2, 18, 12))

        # Wing (animated)
        wing_y = cy + 4 + int(self.flap_offset)
        pygame.draw.ellipse(screen, (220, 170, 0),
                            (cx - 14, wing_y, 16, 9))

        # Eye white
        pygame.draw.circle(screen, WHITE, (cx + 7, cy - 6), 7)
        # Eye pupil
        pygame.draw.circle(screen, (30, 30, 30), (cx + 9, cy - 5), 4)
        # Eye shine
        pygame.draw.circle(screen, WHITE, (cx + 11, cy - 7), 2)

        # Beak — upper
        pygame.draw.polygon(screen, (255, 130, 0), [
            (cx + 10, cy - 2),
            (cx + 22, cy - 5),
            (cx + 10, cy + 2)
        ])
        # Beak — lower
        pygame.draw.polygon(screen, (220, 100, 0), [
            (cx + 10, cy + 2),
            (cx + 20, cy + 1),
            (cx + 10, cy + 6)
        ])

        # Cheek blush
        pygame.draw.circle(screen, (255, 160, 160),
                           (cx + 4, cy + 4), 4)