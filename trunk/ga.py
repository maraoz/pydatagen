#!/usr/bin/python
# -*- coding: utf-8 -*-

# ga.py
# generic genetic algorithm excecuting class


from random import randint, random

class GeneticAlgorithm(object):
    
    def __init__(self, fitness_function, random_chromosome_function,
                 mating_function, mutation_function, max_generations = 2000,
                 population_size = 100):
        
        self.fitness = fitness_function
        self.random_chromosome = random_chromosome_function
        self.combine = mating_function
        self.mutate = mutation_function

        self.max_generations = max_generations
        self.population_size = population_size
        
        self.population = []
        self.generation = 0
        
    def get_best_individual(self):
        self.evaluate_fitness()
        return max(self.population, key=lambda c: c['fitness'])
        

    def evaluate_fitness(self):
        for individual in self.population:
            chrm = individual['genes']
            individual['fitness'] = self.fitness(chrm)
    def sort_by_fitness(self):
        cmp_function = lambda c, d: cmp(c['fitness'],d['fitness'])
        self.population.sort(cmp=cmp_function)
        
    def next_generation(self):
        self.generation += 1

    def initialize_population(self):
        for i in xrange(self.population_size):
            chromosome = self.random_chromosome()
            individual = {'genes' : chromosome, 'fitness' : 0}
            self.population.append(individual)

    def get_offspring(self):
        raise NotImplementedError
        
    def introduce(self, offspring):
        raise NotImplementedError

    def mutation(self, offspring):
        new_o = []
        for child in offspring:
            new_o.append({'genes' : self.mutate(child['genes']),
                          'fitness' : 0})
        return new_o
    
    def run(self):
        
        self.initialize_population()    
        while (self.generation < self.max_generations):
            self.evaluate_fitness()
            offspring = self.get_offspring()
            offspring = self.mutation(offspring)
            self.introduce(offspring)
            self.next_generation()
        
        best = self.get_best_individual()
        
        return best['genes']


class ElitistGeneticAlgorithm(GeneticAlgorithm):
    """This class englobes the genetic algorithms which use elitism,
        that is, that a (usually small) percentage of each population
        is preserved alive and intact to the next generation. This are
        the best individuals based on fitness"""

    def __init__(self, *args, **kwargs):

        elite = 0.4
        GeneticAlgorithm.__init__(self, *args, **kwargs)

        # we calculate how many offspring to generate based on the
        # ammount of individuals that will survive to next generation
        self.elite_ammount = int(elite * self.population_size)
        self.offspring_ammount = self.population_size - self.elite_ammount

    def introduce(self, offspring):
        assert len(self.population) == self.population_size
        self.population = self.population[:self.elite_ammount] + offspring

    def print_best(ordered = False):
        if not ordered:
            best = min(self.population, key = lambda i: i['fitness']
        else:
            best = self.population[0]
        print "best in gen %d is %s with fitness %d" % \
              (self.generation, best['genes'],best['fitness'])



class AsexualGeneticAlgorithm(ElitistGeneticAlgorithm):
    """In this simple version, the offspring we generate are
        exact copies of the fittest individuals in the population.
        Then mutation will be applied, so this algorithm simulates
        asexual reproduction"""


    def get_offspring(self):
        self.sort_by_fitness()
        self.print_best(ordered=True)
        return self.population[:self.offspring_ammount]

class CrossoverGeneticAlgorithm(ElitistGeneticAlgorithm):
    """In this more complex version, the offspring we generate are
        combination of two parents from previous population. The parents
        are chosen for mating using a linear roulette wheel based on
        fitness."""

    def get_random_parent(self, total):
        r = random() * total
        s = 0
        for ind in self.population:
            s += ind['fitness']
            if s > r:
                return ind
        #shouldn't reach this point
        raise TypeError, "random number r=%f derived from total=%f \
            shouldn't be greater than sum s=%f." % (r,total,s)

    def get_offspring(self):
        self.sort_by_fitness()
        pop_fitness = sum(i['fitness'] for i in self.population)
        offspring = []
        for i in xrange(self.offspring_ammount):
            father = self.get_random_parent()
            mother = self.get_random_parent()

            offspring.append(self.combine(father,mother))

        # optional
        self.print_best(ordered=True)
        return offspring
        

def main():
    pass
    

if __name__ == "__main__":
    main()
