import pygame
pygame.font.init()
from bird import Bird
from pipe import Pipe
from base import Base
from settings import *

class Game:
    def __init__(self):
        self.bird  = Bird(30, D_HEIGHT // 2, 0, BIRD_IMG)
        self.pipes = [Pipe(PIPE_IMG)]
        self.bases = [Base(0, D_HEIGHT - 100, BASE_IMG), Base(D_WIDTH, D_HEIGHT - 100, BASE_IMG)]
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
                self.pipes.append(Pipe(PIPE_IMG))

            for pipe in passed_pipes:
                self.pipes.remove(pipe)
                self.score += 1

            for pipe in self.pipes:
                if pipe.detect_collision(self.bird):
                    self.reset()

            self.draw_window(display, fps)

    def reset(self):
        self.bird  = Bird(30, D_HEIGHT // 2, 0, BIRD_IMG)
        self.pipes = [Pipe(PIPE_IMG)]
        self.bases = [Base(0, D_HEIGHT - 100, BASE_IMG), Base(D_WIDTH, D_HEIGHT - 100, BASE_IMG)]
        self.score = 0

    def draw_window(self, win, fps):
        score_text = ARCADE_FONT.render("Score " + str(self.score), 1, (255, 255, 255))
        fps_text = ARCADE_FONT.render("fps " + str(fps), 1, (255, 255, 255))
        win.blit(BG_IMG, (0, 0))

        for pipe in self.pipes:
            pipe.draw(win)
        
        for base in self.bases:
            base.move()
            base.draw(win)

        for base in self.bases:
            if base.x <= 0 - BG_IMG.get_width():
                self.bases.append(Base(D_WIDTH, D_HEIGHT - 100, BASE_IMG))
                self.bases.remove(base)

        self.bird.draw(win)
        win.blit(score_text, (10, 10))
        win.blit(fps_text, (150, 10))
        pygame.display.flip()


