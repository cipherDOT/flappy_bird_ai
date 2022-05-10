

# todo:
#       [x] add collision detection
#       [x] add game class
#       [ ] add genes
#       [ ] add genetic evolution algorithm 
# ----------------------------------------------- required imports ------------------------------------------------------ #


import pygame
import os
import random

pygame.font.init()

# ----------------------------------------------- global variables ------------------------------------------------------ #

D_WIDTH = 500
D_HEIGHT = 800

display = pygame.display.set_mode((D_WIDTH, D_HEIGHT))
BIRD_IMG =  pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bird.png'))).convert_alpha()
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'pipe.png'))).convert_alpha()
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'base.png'))).convert_alpha()
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join('assets', 'bg - dark.png'))).convert_alpha()
ARCADE_FONT = pygame.font.Font(os.path.join('assets', 'ARCADECLASSIC.TTF'), 24)
pygame.display.set_caption('Flappy bird')
pygame.display.set_icon(BIRD_IMG)

# ---------------------------------------------- image rotate func ----------------------------------------------------- #

def blitRotateCenter(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect)

# -------------------------------------------------- Bird class ------------------------------------------------------- #

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


# -------------------------------------------------- Pipe class ------------------------------------------------------- #

class Pipe:
    def __init__(self, x = D_WIDTH):
        self.x = x
        self.vel = 3
        self.top_pipe = pygame.transform.flip(PIPE_IMG, False, True)
        self.bottom_pipe = PIPE_IMG
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
        # pygame.draw.circle(win, (255, 0, 0), (self.x, self.bottom_height), 10)
        # pygame.draw.circle(win, (255, 0, 0), (self.x, self.top_height), 10)
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

# -------------------------------------------------- Base class ------------------------------------------------------- #

class Base:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0.5

    def move(self):
        self.x -= self.velocity

    def draw(self):
        display.blit(BASE_IMG, (self.x, self.y))

# -------------------------------------------------- Game class ------------------------------------------------------- #

class Game:
    def __init__(self):
        self.bird  = Bird(30, D_HEIGHT // 2, 0, BIRD_IMG)
        self.pipes = [Pipe()]
        self.bases = [Base(0, D_HEIGHT - 100), Base(D_WIDTH, D_HEIGHT - 100)]
        self.score = 0
        self.clock = pygame.time.Clock()

    def run(self):
        loop = True
        while loop:
            self.clock.tick(120)
            fps = int(self.clock.get_fps())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.flap()

                    if event.key == pygame.K_d:
                        print(fps)
            
            add_pipe = False
            passed_pipes = []
            self.bird.move()
            for pipe in self.pipes:
                pipe.move()
                if pipe.has_passed_screen():
                    add_pipe = True
                    passed_pipes.append(pipe)

            if add_pipe:
                self.pipes.append(Pipe())

            for pipe in passed_pipes:
                self.pipes.remove(pipe)
                self.score += 1

            for pipe in self.pipes:
                if pipe.detect_collision(self.bird):
                    self.reset()

            draw_window(display, self.bird, self.pipes, self.bases, self.score, fps)

    def reset(self):
        self.bird  = Bird(30, D_HEIGHT // 2, 0, BIRD_IMG)
        self.pipes = [Pipe()]
        self.bases = [Base(0, D_HEIGHT - 100), Base(D_WIDTH, D_HEIGHT - 100)]
        self.score = 0

# ------------------------------------------------- draw win func ----------------------------------------------------- #

def draw_window(win, bird, pipes, bases, score, fps):
    score_text = ARCADE_FONT.render("Score " + str(score), 1, (255, 255, 255))
    fps_text = ARCADE_FONT.render("fps " + str(fps), 1, (255, 255, 255))
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)
    
    for base in bases:
        base.move()
        base.draw()

    for base in bases:
        if base.x <= 0 - BG_IMG.get_width():
            bases.append(Base(D_WIDTH, D_HEIGHT - 100))
            bases.remove(base)

    bird.draw(win)
    win.blit(score_text, (10, 10))
    win.blit(fps_text, (150, 10))
    pygame.display.flip()

# ------------------------------------------------- initialize game ----------------------------------------------------- #

if __name__ == "__main__":
    game = Game()
    game.run()

# -------------------------------------------------------------------------------------------------------------------------#
