import pygame
import random
from settings import *

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
        self.gene_length = GENE_LENGTH
        self.gene = []
        self.fitness = -1
        self.dead = False
        self.generation = -1
        self.age = 0
        self.visual_inputs = []

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

    def create_genes(self):
        for _ in range(self.gene_length):
            random_gene = random.uniform(0, 1)
            self.gene.append(random_gene)

    def calc_fitness(self):
        # using a fitness function to find the fitness of
        # the specific genome, and use it as the metric to
        # improve it's probability of becoming a parent
        return self.age / 100

    def crossover(self, partner):
        child = Bird(30, D_HEIGHT // 2, 0, BIRD_IMG)
        for i in range(self.gene_length):
            if i % 2 == 0:
                child.gene.append(self.gene[i])
            else:
                child.gene.append(partner.gene[i])

        return child

    def mutate(self):
        for i in range(GENE_LENGTH):
            mutation_probability = round(random.uniform(0, 1), 2)
            if mutation_probability == MUTATION_RATE:
                mutated_gene = random.uniform(-0.005, 0.005)
                self.gene[i] += mutated_gene

    def look(self, pipe):
        self.visual_inputs = []
        self.visual_inputs.append(1 - (self.y / D_HEIGHT))
        self.visual_inputs.append(self.vel / self.terminal_vel)
        self.visual_inputs.append(1 - (pipe.x / D_WIDTH))
        self.visual_inputs.append(1 - (pipe.height / D_HEIGHT))

    def debug(self, win):
        # pygame.draw.line(win, (255, 0, 0), (self.x, self.y), ((1 - self.visual_inputs[2]) * D_WIDTH, self.visual_inputs[3] * D_HEIGHT), 5)
        pygame.draw.line(win, (255, 0, 0), (self.x, self.y), ((-1 - self.visual_inputs[2]) * D_WIDTH, self.y), 5)
        pygame.draw.line(win, (255, 0, 0), (self.x, self.y), (self.x, (-1 - self.visual_inputs[3]) * D_HEIGHT), 5)

    def think(self):
        out = 0
        for i in range(self.gene_length):
            out += self.gene[i] * self.visual_inputs[i]

        return out
