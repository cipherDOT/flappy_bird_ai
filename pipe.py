import pygame
import random
from settings import D_WIDTH

class Pipe:
    def __init__(self, img, x = D_WIDTH):
        self.x = x
        self.vel = 3
        self.img = img
        self.top_pipe = pygame.transform.flip(self.img, False, True)
        self.bottom_pipe = self.img
        self.height = self.set_height()
        self.gap_height = 150
        self.pipe_height = self.bottom_pipe.get_height()
        self.pipe_width = self.bottom_pipe.get_width()
        self.top_height = self.height - self.top_pipe.get_height() - self.gap_height
        self.bottom_height = self.height
        self.cleared = False

    def set_height(self):
        height = random.randint(175, 625)
        return height

    def move(self):
        self.x -= self.vel

    def draw(self, win):
        win.blit(self.top_pipe, (self.x, self.height - self.pipe_height - self.gap_height))
        win.blit(self.bottom_pipe, (self.x, self.height))

    def has_passed_screen(self):
        return self.x + self.pipe_width < 0

    def detect_collision(self, bird):
        bird_mask = bird.get_mask()
        
        
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)
        top_offset = (self.x - bird.x, self.top_height - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom_height - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False
