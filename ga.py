#!/usr/bin/python
# -*- coding: utf-8 -*-

# ga.py
# generic genetic algorithm excecuting class


from random import randint, random, choice

class GeneticAlgorithm(object):
    """ Generic class for genetic algorithm """
    
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
            individual['fitness'] = self.fitness(chrm) or 0.1
            # if 0 set fitness to a small number
    def sort_by_fitness(self):
        cmp_function = lambda c, d: cmp(d['fitness'],c['fitness'])
        self.population.sort(cmp=cmp_function)
        
    def next_generation(self):
        self.generation += 1

    def initialize_population(self):
        for i in xrange(self.population_size):
            chromosome = self.random_chromosome()
            individual = {'genes' : chromosome, 'fitness' : 0}
            self.population.append(individual)

    def mutation(self, offspring):
        new_o = []
        for child in offspring:
            new_o.append({'genes' : self.mutate(child['genes']),
                          'fitness' : 0})
        return new_o

    def get_offspring(self):
        raise NotImplementedError
        
    def introduce(self, offspring):
        raise NotImplementedError

    def population_stable(self):
        raise NotImplementedError

    def run(self):
        
        self.initialize_population()    
        while not self.population_stable() and \
              self.generation < self.max_generations:
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

    def __init__(self, max_fitness, *args, **kwargs):

        self.max_fitness = max_fitness
    
        elite = 0.4
        GeneticAlgorithm.__init__(self, *args, **kwargs)

        # we calculate how many offspring to generate based on the
        # ammount of individuals that will survive to next generation
        self.elite_ammount = int(elite * self.population_size)
        self.offspring_ammount = self.population_size - self.elite_ammount

    def population_stable(self):
        return self.population[0]['fitness'] == self.max_fitness

    def introduce(self, offspring):
        assert len(self.population) == self.population_size
        self.population = self.population[:self.elite_ammount] + offspring

    def print_best(self, is_ordered):
        if not is_ordered:
            best = max(self.population, key = lambda i: i['fitness'])
        else:
            best = self.population[-1]
        print "best in gen %d is %s with fitness %d" % \
              (self.generation, best['genes'],best['fitness'])



class AsexualGeneticAlgorithm(ElitistGeneticAlgorithm):
    """In this simple version, the offspring we generate are
        exact copies of the fittest individuals in the population.
        Then mutation will be applied, so this algorithm simulates
        asexual reproduction"""


    def get_offspring(self):
        self.sort_by_fitness()
        # optional
        self.print_best(is_ordered = True)
        return self.population[:self.offspring_ammount]

class CrossoverGeneticAlgorithm(ElitistGeneticAlgorithm):
    """In this more complex version, the offspring we generate are
        combination of two parents from previous population. The parents
        are chosen for mating using a linear roulette wheel based on
        fitness."""

    def get_random_parent(self, total):
        """ total: total population fitness """
        if total == 0:
            return choice(self.population)
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
            father = self.get_random_parent(pop_fitness)
            mother = self.get_random_parent(pop_fitness)

            combined_genes = self.combine(father['genes'],mother['genes'])
            offspring.append({'genes' : combined_genes, 'fitness' : 0})

        # optional
        self.print_best(is_ordered = True)
        return offspring
        

def main():
    pass
    

if __name__ == "__main__":
    main()
