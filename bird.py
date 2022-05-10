import pygame
from settings import blitRotateCenter

class Bird:
    def __init__(self, x, y, vel, img):
        self.x = x
        self.y = y
        self.vel = vel
        self.img = img
        self.acc = 0.005
        self.tick_count = 0
        self.jump_vel = -3
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
        # v = u + at
        # we are updating the velocity value and we increment the 
        # bird's y position w.r.t the velocity.
        self.vel = self.vel + self.acc * self.tick_count

        # terminal velocity
        if self.vel >= self.terminal_vel:
            self.vel = (self.vel/abs(self.vel)) * self.terminal_vel

        # changing the bird's position w.r.t velocity
        self.y += self.vel

        # tilt up
        if self.vel < 0:  
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        # tilt down
        else:  
            if self.tilt > -self.max_rotation:
                self.tilt -= self.rotation_velocity
        
    def get_mask(self):
        return pygame.mask.from_surface(self.img)

