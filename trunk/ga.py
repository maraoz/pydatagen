#!/usr/bin/python
# -*- coding: utf-8 -*-

# ga.py
# generic genetic algorithm excecuting class



POPULATION_SIZE = 100
MAX_GENERATIONS = 1000000

PARENTS_PER_GENERATION = 50



class GeneticAlgorithm(object):
    
    def __init__(self, fitness_function, random_chromosome_function
                 mating_funcion, mutation_function):
        
        self.fitness = fitness_function
        self.random_chromosome = random_chromosome_function
        self.combine = mating_function
        self.mutate = mutation_function
        
        self.population = []
        self.generation = 0
        
    def get_best_individual(self):
        return max(self.population, key=self.fitness)

    def calculate_fitness(self):
        for individual in self.population:
            chrm = individual['genes']
            individual['fitness'] = self.fitness(chrm)
        
    def next_generation(self):
        self.generation += 1

    def initialize_population(self):
        for i in xrange(POPULATION_SIZE):
            chromosome = self.random_chromosome()
            individual = {'genes' : chromosome, 'fitness' : 0}
            self.population.append(individual)
        
    def get_parents(self):
        raise NotImplementedError
        
    def get_offspring(self, parents):
        raise NotImplementedError
        
    def get_selected(self, parents, offspring):
        raise NotImplementedError
    
    
    def run(self):
        
        self.initialize_population()    
        while (self.generation < MAX_GENERATIONS):
            self.calculate_fitness()
            offspring = self.get_offspring()
            self.population = self.getSelected(parents,offspring)
            self.nextGeneration()
        
        best = self.getBestIndividual()
        
        return best
            

class SimpleGeneticAlgorithm(GeneticAlgorithm):


    def get_parents(self):
        
        if len(self.population) != POPULATION_SIZE:
            raise ValueError, "Population size corrupt, must be %d and is %d" % (POPULATION_SIZE, len(self.population))
     
        evaluatedPopulation = [(self.fitness(ind), ind) for ind in self.population]
        evaluatedPopulation.sort()

        return [parent for (fitness, parent) in evaluatedPopulation[:PARENTS_PER_GENERATION]]

    def mate(self, parents):
        return [self.mutate(individual) for individual in parents]
    
    def get_offspring(self, parents):
        children = self.mate(parents)
        return children
    
    def get_selected(self, parents, offspring):
        return parents+offspring
        

def main():
    pass
    

if __name__ == "__main__":
    main()
