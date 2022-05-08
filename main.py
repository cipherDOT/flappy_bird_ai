

import pygame
import os
import random

pygame.font.init()

D_WIDTH = 500
D_HEIGHT = 800
GEN = 0

display = pygame.display.set_mode((D_WIDTH, D_HEIGHT))
BIRD_IMG =  pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird2.png')))
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'pipe.png')))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'base.png')))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bg.png')))
pygame.display.set_caption('Flappy bird')
pygame.display.set_icon(BIRD_IMG)

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect)

# -------------------------------------------------------------------------------------------------------------------------#
class Bird:
    def __init__(self, x, y, vel, img):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.acc = 0.005
        self.tick_count = 0
        self.jump_vel = -4
        self.terminal_vel = 7
        self.height = self.y
        self.tilt = 0
        self.max_rotation = 25
        self.rotation_velocity = 3

    def draw(self, win):
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def flap(self):
        self.vel = self.jump_vel
        self.tick_count = 0

    def move(self):
        self.tick_count += 1

        # for downward acceleration
        self.vel = self.vel + self.acc * self.tick_count  # calculate vel

        # terminal velocity
        if self.vel >= self.terminal_vel:
            self.vel = (self.vel/abs(self.vel)) * self.terminal_vel

        self.y += self.vel

        if self.vel < 0:  # tilt up
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:  # tilt down
            if self.tilt > -self.max_rotation:
                self.tilt -= self.rotation_velocity
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

# -------------------------------------------------------------------------------------------------------------------------#

class Pipe:
    pass

# -------------------------------------------------------------------------------------------------------------------------#

class Base:
    pass

def draw_window(win, bird):
    win.blit(BG_IMG, (0, 0))
    bird.draw(win)
    pygame.display.flip()


def main():
    run = True
    bird = Bird(30, D_HEIGHT // 2, 0, BIRD_IMG)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.flap()
        
        bird.move()
        draw_window(display, bird)

if __name__ == "__main__":
    main()
