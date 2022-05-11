import pygame
from bird import Bird
from pipe import Pipe
from base import Base
from population import Population
from settings import *

class Game:
    def __init__(self):
        # self.bird  = Bird(30, D_HEIGHT // 2, 0, BIRD_IMG)
        self.birds = Population()
        self.birds.populate()
        self.pipes = [Pipe(PIPE_IMG)]
        self.bases = [Base(0, D_HEIGHT - 100, BASE_IMG), Base(D_WIDTH, D_HEIGHT - 100, BASE_IMG)]
        self.score = 0
        self.clock = pygame.time.Clock()
        self.frame_rate = 60

    def run(self):
        loop = True
        while loop:
            self.clock.tick(self.frame_rate)
            fps = int(self.clock.get_fps())

            if all([bird.dead for bird in self.birds.population]):
                self.birds.breed()
                self.reset()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    loop = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        print(self.birds.display_best_gene())

            for bird in self.birds.population:
                bird.move()
                bird.look(self.pipes[0])
                bird.age += 1
                bird.fitness = bird.calc_fitness()
                # chance_to_flap = random.random()
                chance_to_flap = bird.think()
                # print(chance_to_flap)
                if chance_to_flap >= 0.5:
                    bird.flap()
                else:
                    bird.vel = 3

                if bird.y >= self.bases[0].y:
                    bird.dead = True

                for pipe in self.pipes:
                    if pipe.detect_collision(bird):
                        bird.dead = True

            add_pipe = False
            passed_pipes = []
            
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

            self.draw_window(display, fps)

    def draw_window(self, win, fps):
        score_text = ARCADE_FONT.render("Score " + str(self.score), 1, (255, 255, 255))
        fps_text = ARCADE_FONT.render("fps " + str(fps), 1, (255, 255, 255))
        gen_text = ARCADE_FONT.render("gen " + str(self.birds.generation), 1, (255, 255, 255))
        alive_text = ARCADE_FONT.render("alive " + str(len([i for i in self.birds.population if not i.dead])), 1, (255, 255, 255))
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

        for bird in self.birds.population:
            if not bird.dead:
                bird.draw(win)
                bird.debug(win)                

        win.blit(score_text, (10, 10))
        win.blit(fps_text, (150, 10))
        win.blit(gen_text, (270, 10))
        win.blit(alive_text, (370, 10))
        pygame.display.flip()

    def reset(self):
        # self.birds = Population()
        # self.birds.populate()
        self.pipes = [Pipe(PIPE_IMG)]
        self.bases = [Base(0, D_HEIGHT - 100, BASE_IMG), Base(D_WIDTH, D_HEIGHT - 100, BASE_IMG)]
        self.score = 0
