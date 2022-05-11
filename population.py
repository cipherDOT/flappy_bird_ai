
import math
import random
from bird import Bird
from settings import *

class Population(object):
    def __init__(self):
        self.population = []
        self.generation = 0

    def populate(self):
        self.population = [Bird(30, D_HEIGHT // 2, 0, BIRD_IMG) for _ in range(POPULATION_SIZE)]
        for genome in self.population:
            genome.create_genes()
            genome.generation = self.generation

    def natural_selection(self):
        mating_pool = []
        for genome in self.population:
            fitness_ratio = math.floor(max(genome.fitness, 0) * 100)
            for _ in range(fitness_ratio):
                mating_pool.append(genome)

        # print(f"Size of mating pool: {len(mating_pool)}")
        return mating_pool

    def breed(self):
        generation_dead = all([genome.dead for genome in self.population])
        if generation_dead:
            mating_pool = self.natural_selection()
            children = Population()

            for _ in range(POPULATION_SIZE):
                father_genome = random.choice(mating_pool)
                mother_genome = random.choice(mating_pool)
                child_genome = father_genome.crossover(mother_genome)
                child_genome.mutate()
                child_genome.generation = self.generation
                children.population.append(child_genome)

            self.population = children.population
            self.generation += 1

    def display_best_gene(self):
        print([i for i in self.population if not i.dead][0].gene)
