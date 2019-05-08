#!/usr/bin/env python3

# Please feel free to modify any part of the code or add any functions, or modify the argument of 
# the given functions. But please keep the name of the given functions

# Please feel free to import any libraries you need.

# You are required to finish the genetic_algorithm function, and you may need to complete crossover, 
# mutate and select.

import bisect
import matplotlib.pyplot as plt
import random

num_states = 10
num_digits = 3
num_elitism = 5     # number of elites to pick
prob_mutate = 0.5   # mutation probability on a single digit

def crossover(old_gen, probability_crossover):   # 3 point crossover
    #TODO START
    new_population = []
    # precondition: old_gen contains the 2 parents
    dad = old_gen[0]
    mom = old_gen[0]
    if random.random() < probability_crossover:   # perform 3 point crossover
        # pos can be in [0, 29] 
        pos_one = random.randint(0, num_states * num_digits - 3)
        pos_two = random.randint(pos_one + 1, num_states * num_digits - 2)
        pos_three = random.randint(pos_two + 1, num_states * num_digits - 1)
        new_population.append(dad[:pos_one] + mom[pos_one:pos_two] + dad[pos_two:pos_three] + mom[pos_three:])
    else:                                         # randonly choose dad / mom
        new_population.append(dad if random.random() < 0.5 else mom)

    #TODO END
    return new_population

def mutate(old_gen, probability_mutation):
    #TODO START
    new_gen = old_gen
    if random.random() < probability_mutation:   # perform the mutation
        for i in range(num_states * num_digits):
            if random.random() < prob_mutate:
                temp = random.randint(1, 4) if i % 3 == 0 else random.randint(0, 9)
                new_gen = new_gen[:i] + str(temp) + new_gen[i+1:] 

    #TODO END
    return new_gen

def select(old_gen):    # rank selection
    #TODO START
    new_population = []

    sequence = generate_sequence(len(old_gen))
    # select two parents
    r = random.randint(1, len(old_gen) * (len(old_gen) + 1) / 2)   # e.g., n = 10, [0, 54]
    new_population.append(old_gen[bisect.bisect_left(sequence, r)])
    r = random.randint(1, len(old_gen) * (len(old_gen) + 1) / 2)
    new_population.append(old_gen[bisect.bisect_left(sequence, r)])
    #TODO END
    return new_population

def generate_sequence(n):   # e.g., n = 10, sequence = [10, 19, 27, 34, 40, 45, 49, 52, 54, 55]
    sofar = 0
    sequence = []
    for i in range(n, 0, -1):
        sofar = sofar + i
        sequence.append(sofar)
    assert len(sequence) == n
    return sequence

def genetic_algorithm(population, food_map_file_name, max_generation, probability_crossover, probability_mutation):
    #TODO START
    stats = []   # [ [max, min, avg], [ ... ], [ ... ], ... ]
    max_fitness = -1
    max_individual = ""
    max_trial = ""
    
    food_map, map_size = get_map(food_map_file_name)
    # assume the initial population doesn't count as an generation, thus
    # +1 to evaluate the last generation
    for i in range(max_generation + 1):
        # record statistics of the current generation
        fitness = []
        cur_max = -1; cur_min = 32*32; cur_sum = 0
        # evaluate the fitness for each individual
        for j in range(len(population)):
            trial, cur_fitness = ant_simulator(food_map, map_size, population[j])
            fitness.append(cur_fitness)
            # update statistics (of the current generations)
            if cur_fitness > cur_max:
                cur_max = cur_fitness
                # max_fitness, max_individual and max_trial are for the last generation
                max_fitness = cur_fitness
                max_individual = population[j]
                max_trial = trial
            cur_min = cur_fitness if cur_fitness < cur_min else cur_min
            cur_sum = cur_sum + cur_fitness

        stats.append([cur_max, cur_min, cur_sum / len(population)])

        # when the current population is not the last generation, construct new 
        # population (the next generation) by selection, crossover and mutation
        if i < max_generation:
            new_population = []   # NOTE: size of population remains the same across generations
            # sort the current population by fitness score
            population = [individual for _, individual in sorted(zip(fitness, population), reverse=True)]
            # elitism (copy the best num_elitism individual to the new population)
            new_population.extend(population[:num_elitism])
            # the rest of the new population
            for j in range(len(population) - 1):
                new_population.append(mutate(crossover(select(population), probability_crossover)[0], probability_mutation))
            
            population = new_population

    return max_fitness, max_individual, max_trial, stats, population
    #TODO END    

def initialize_population(num_population):
    #TODO START
    population = []
    for i in range(num_population):
        individual = ""
        for j in range(num_states):   # each individual = num_states * num_digits = 10 * 3
            individual = individual + str(random.randint(100, 499))
        population.append(individual)

    #TODO END
    return population
    
def ant_simulator(food_map, map_size, ant_genes):
    """
    parameters:
        food_map: a list of list of strings, representing the map of the environment with food
            "1": there is a food at the position
            "0": there is no food at the position
            (0, 0) position: the top left corner of the map
            (x, y) position: x is the row, and y is the column
        map_size: a list of int, the dimension of the map. It is in the format of [row, column]
        ant_genes: a string with length 30. It encodes the ant's genes, for more information, please refer to the handout.
    
    return:
        trial: a list of list of strings, representing the trials
            1: there is food at that position, and the spot was not visited by the ant
            0: there is no food at that position, and the spot was not visited by the ant
            empty: the spot has been visited by the ant
    
    It takes in the food_map and its dimension of the map and the ant's gene information, and return the trial in the map
    """
    
    step_time = 200
    
    trial = []
    for i in food_map:
        line = []
        for j in i:
            line.append(j)
        trial.append(line)

    position_x, position_y = 0, 0
    orientation = [(1, 0), (0, -1), (-1, 0), (0, 1)] # face down, left, up, right
    fitness = 0
    state = 0
    orientation_state = 3
    gene_list = [ant_genes[i : i + 3] for i in range(0, len(ant_genes), 3)]
    
    for i in range(step_time):
        if trial[position_x][position_y] == "1":
            fitness += 1
        trial[position_x][position_y] = " "
        
        sensor_x = (position_x + orientation[orientation_state][0]) % map_size[0]
        sensor_y = (position_y + orientation[orientation_state][1]) % map_size[1]
        sensor_result = trial[sensor_x][sensor_y]
        
        if sensor_result == "1":
            state = int(gene_list[state][2])
        else:
            state = int(gene_list[state][1])
        
        action = gene_list[state][0]

        if action == "1":     # move forward
            position_x = (position_x + orientation[orientation_state][0]) % map_size[0]
            position_y = (position_y + orientation[orientation_state][1]) % map_size[1]
        elif action == "2":   # turn right
            orientation_state = (orientation_state + 1) % 4
        elif action == "3":   # turn left
            orientation_state = (orientation_state - 1) % 4
        elif action == "4":   # do nothing
            pass
        else:
            raise Exception("invalid action number!")
    
    return trial, fitness
        
def get_map(file_name):
    """
    parameters:
        file_name: a string, the name of the file which stored the map. The first line of the map is the dimension (row, column), the rest is the map
            1: there is a food at the position
            0: there is no food at the position
    
    return:
        food_map: a list of list of strings, representing the map of the environment with food
            "1": there is a food at the position
            "0": there is no food at the position
            (0, 0) position: the top left corner of the map
            (x, y) position: x is the row, and y is the column
        map_size: a list of int, the dimension of the map. It is in the format of [row, column]
    
    It takes in the file_name of the map, and return the food_map and the dimension map_size
    """
    food_map = []
    map_file = open(file_name, "r")
    first_line = True
    map_size = []
    
    for line in map_file:
        line = line.strip()
        if first_line:
            first_line = False
            map_size = line.split()
            continue
        if line:
            food_map.append(line.split())
    
    map_file.close()
    return food_map, [int(i) for i in map_size]

def display_trials(trials, target_file):
    """
    parameters:
        trials: a list of list of strings, representing the trials
            1: there is food at that position, and the spot was not visited by the ant
            0: there is no food at that position, and the spot was not visited by the ant
            empty: the spot has been visited by the ant
        taret_file: a string, the name the target_file to be saved
    
    It takes in the trials, and target_file, and saved the trials in the target_file. You can open the target_file to take a look at the ant's trial.
    """
    trial_file = open(target_file, "w")
    for line in trials:
        trial_file.write(" ".join(line))
        trial_file.write("\n")
    trial_file.close()

if __name__ == "__main__":
    #TODO START
    #You will need to modify the parameters below.
    #The parameters are for references, please feel free add more or delete the ones you do not intend to use in your genetic algorithm
    population_size = 100
    population = initialize_population(population_size)
    food_map_file_name = "muir.txt"

    max_generation = 200
    probability_crossover = 0.2
    probability_mutation = 0.3
    max_fitness, max_individual, max_trial, stats, population = genetic_algorithm(population, food_map_file_name, max_generation, probability_crossover, probability_mutation)

    display_trials(max_trial, "max_trial.txt")
    
    plt.figure(1)
    plt.plot([i for i in range(len(stats))], [i[0] for i in stats], marker = "o")
    plt.xlabel("generation")
    plt.xlim((0, 200))
    plt.ylim((0, max(i[0] for i in stats) + 10))
    plt.ylabel("most fit individual")
    plt.savefig("max_fitness_per_ generation.png")
    
    plt.figure(2)
    muir_fitness = []
    santafe_fitness = []
    muir_food_map, muir_map_size = get_map("muir.txt")
    santafe_food_map, santafe_map_size = get_map("santafe.txt")

    for individual in population:
        trial, individual_muir_fitness = ant_simulator(muir_food_map, muir_map_size, individual)
        trial, individual_santafe_fitness = ant_simulator(santafe_food_map, santafe_map_size, individual)
        muir_fitness.append(individual_muir_fitness)
        santafe_fitness.append(individual_santafe_fitness)

    plt.plot([i for i in range(len(muir_fitness))], muir_fitness, marker = "o", color = "blue", label = "muir")
    plt.plot([i for i in range(len(santafe_fitness))], santafe_fitness, marker = "o", color = "green", label = "santa fe")
    plt.xlabel("individuals in the last generation")
    plt.xlim((0, population_size))
    plt.ylim((0, max(muir_fitness + santafe_fitness) + 10))
    plt.ylabel("fitness")
    plt.legend()
    plt.savefig("fitness_of_last_generation_on_muir_and_santa_fe.png")
    #TODO END
    
    '''
    # Example of how to use get_map, ant_simulator and display trials function
    food_map, map_size = get_map("muir.txt")
    ant_genes = "335149249494173115455311387263"
    trial, fitness = ant_simulator(food_map, map_size, ant_genes)
    display_trials(trial, "trial.txt")
    '''

