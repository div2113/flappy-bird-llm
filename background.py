import pygame
import math
from settings import *

class Background:
    def __init__(self):
        self.clouds = [
            {'x': 60,  'y': 80,  'speed': 0.4, 'size': 1.0},
            {'x': 200, 'y': 50,  'speed': 0.3, 'size': 0.8},
            {'x': 320, 'y': 100, 'speed': 0.5, 'size': 1.2},
        ]
        self.time = 0

    def update(self):
        self.time += 1
        for cloud in self.clouds:
            cloud['x'] -= cloud['speed']
            if cloud['x'] < -120:
                cloud['x'] = SCREEN_WIDTH + 60

    def draw_cloud(self, screen, x, y, size):
        color = (255, 255, 255)
        r = int(28 * size)
        pygame.draw.circle(screen, color, (int(x), int(y)), r)
        pygame.draw.circle(screen, color, (int(x + r), int(y + 8)), int(r * 0.8))
        pygame.draw.circle(screen, color, (int(x - r), int(y + 8)), int(r * 0.7))
        pygame.draw.ellipse(screen, color,
                            (int(x - r * 1.2), int(y + 8),
                             int(r * 2.6), int(r * 0.9)))

    def draw(self, screen):
        # Sky gradient (simple 2 tone)
        screen.fill((135, 206, 235))
        pygame.draw.rect(screen, (160, 220, 245),
                         (0, SCREEN_HEIGHT // 2,
                          SCREEN_WIDTH, SCREEN_HEIGHT // 2))

        # Sun
        sun_y = 60 + int(math.sin(self.time * 0.01) * 5)
        pygame.draw.circle(screen, (255, 240, 100), (340, sun_y), 30)
        pygame.draw.circle(screen, (255, 255, 180), (340, sun_y), 22)

        # Sun rays
        for i in range(8):
            angle = math.radians(i * 45 + self.time * 0.3)
            x1 = 340 + int(math.cos(angle) * 33)
            y1 = sun_y + int(math.sin(angle) * 33)
            x2 = 340 + int(math.cos(angle) * 42)
            y2 = sun_y + int(math.sin(angle) * 42)
            pygame.draw.line(screen, (255, 220, 80), (x1, y1), (x2, y2), 2)

        # Clouds
        for cloud in self.clouds:
            self.draw_cloud(screen, cloud['x'], cloud['y'], cloud['size'])