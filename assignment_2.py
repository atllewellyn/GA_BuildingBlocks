import pandas as pd
import random

class bbga:

    def __init__(self):
        pass

    @staticmethod
    def make_individual(n: int) -> str:
        individual = []
        for i in range(2*n):
            individual.append(random.choice(['0', '1']))
        return ''.join(individual)

    @staticmethod
    def make_deme(n: int) -> [str]:
        deme = []
        for i in range(20):
            deme.append(bbga.make_individual(n))
        return deme

    @staticmethod
    def make_population(n: int) -> [[str]]:
        population = []
        for i in range(20):
            population.append(bbga.make_deme(n))
        return population

    @staticmethod
    def make_R(n: int):
        R = []
        for i in range(n + 1):
            temp = []
            for j in range(n + 1):
                temp.append(random.uniform(0.5, 1))
            R.append(temp)
        return R

    @staticmethod
    def fitness(i: int, j: int, R):
        r = R[i][j]
        f = r * (2**i + 2**j)
        return f

    @staticmethod
    def get_i_j(individual: str):
        first_gene, second_gene = individual[:int(len(individual)/2)], individual[int(len(individual)/2):]
        i, j = first_gene.count('1'), second_gene.count('1')
        return i, j

    @staticmethod
    def max_fitness(n: int, R):
        max_f = bbga.fitness(n, n, R)
        return max_f

    @staticmethod
    def mutate(individual: str, n) -> str:
        mutated_individual = ['']*2*n
        for i in range(len(individual)):
            if random.random() < (1 / (2*n)):
                mutated_individual[i] = random.choice(['0', '1'])
            else:
                mutated_individual[i] = individual[i]
        return ''.join(mutated_individual)

    @staticmethod
    def one_point_crossover(parent_1: str, parent_2: str) -> str:
        pointer = random.randrange(0, len(parent_1) - 1)
        new_gene_1 = parent_1[0:pointer]
        new_gene_2 = parent_2[pointer:]
        child = new_gene_1 + new_gene_2
        return child

    @staticmethod
    def uniform_crossover(parent_1: str, parent_2: str) -> str:
        output = ['']*len(parent_1)
        for i in range(len(parent_1)):
            if parent_1[i] == '1' and parent_2[i] =='1':
                output[i] = '1'
            elif parent_1[i] == '0' and parent_2[i] =='0':
                output[i] = '0'
            elif random.random() < 0.5:
                output[i] = '0'
            else:
                output[i] = '1'
        return ''.join(output)

    @staticmethod
    def disjoint_set(n: int) -> str:
        disjoint_ones = '1'*n
        disjoint_zeros = '0'*n 
        disjoint_list = [disjoint_ones, disjoint_zeros]
        index = random.randrange(0, 2)
        first = disjoint_list[index]
        if index == 0:
            index = 1
        else:
            index = 0
        second = disjoint_list[index]
        disjoint = first + second
        return disjoint
    
    @staticmethod
    def random_map(n: int) -> str:
        n = int(n/2)
        i = bbga.make_individual(n)
        j = bbga.make_individual(n)
        while i == j:
            j = bbga.make_individual(n)
        return i + j
    
    @staticmethod
    def shuffle_genetic_map(n: int, individual: str) -> str:
        g_1 = individual[:n]
        g_2 = individual[n:]
        g_1_shuffle = random.sample(g_1, len(g_1))
        g_2_shuffle = random.sample(g_2, len(g_2))
        shuffle = g_1_shuffle + g_2_shuffle
        out = ''
        return out.join(shuffle)

    @staticmethod
    def random_shuffle(individual: str) -> str:
        shuffle = random.sample(individual, len(individual))
        return ''.join(shuffle)

    @staticmethod
    def richard_shuffle(individual: str) -> str:
        i_string = []
        j_string = []
        for i in range(len(individual)):
            if i % 2 == 0:
                i_string.append(individual[i])
            else:
                j_string.append(individual[i])
        i_string = random.sample(i_string, len(i_string))
        j_string = random.sample(j_string, len(j_string))
        output_string = i_string + j_string
        return ''.join(output_string)


    @staticmethod
    def case_handler(deme, n: int, case: int) -> str:
        parent_1 = random.choice(deme)
        parent_2 = random.choice(deme)

        # Experiment 0, no crossover
        if case == 0:
            return bbga.mutate(parent_1, n)

        # Experiment 1, one-point crossover
        elif case == 1:
            cross = bbga.one_point_crossover(parent_1, parent_2)
            return bbga.mutate(cross, n)

        # Experiment 2, uniform crossover
        elif case == 2:
            cross = bbga.uniform_crossover(parent_1, parent_2)
            return bbga.mutate(cross, n)

        # Experiment 3, random genetic map, one point crossover
        elif case == 3:
            if random.random() > 0.8:
                parent_2 = bbga.make_individual(n)
            cross = bbga.one_point_crossover(parent_1, parent_2)
            return bbga.mutate(cross, n)

        else:
            print('--- CASE ERROR ---')
            return

    @staticmethod
    def ga(n: int, case: int):
    
        generations = 0
        population = bbga.make_population(n)
        R = bbga.make_R(n)
        max_f = bbga.max_fitness(n, R)
        flag = 0
        
        while generations <= 1:
                            
            # Increment counter
            generations += 1
                    
            for deme in population:
                
                # Migration
                choice = random.choice(population)
                # Account for choice being this deme
                while choice == deme:
                    choice = random.choice(population)
                index_a = random.randrange(0, len(deme) - 1)
                index_b = random.randrange(0, len(deme) - 1)
                deme[index_a] = choice[index_b]
                
                for i in range(len(deme)):
                    
                    # Create child
                    child = bbga.case_handler(deme, n, case)
                    
                    # Choose an individual to be replaced
                    index_a = random.randrange(0, len(deme) - 1)
                    individual_a = deme[index_a]

                    index_b = random.randrange(0, len(deme) - 1)
                    individual_b = deme[index_b]
                    
                    a_i, a_j = bbga.get_i_j(individual_a)
                    b_i, b_j = bbga.get_i_j(individual_b)
                    
                    if bbga.fitness(a_i, a_j, R) > bbga.fitness(b_i, b_j, R):
                        deme[index_b] = child
                    else:
                        deme[index_a] = child
                    
                    # Has max fitness been found
                    child_i, child_j = bbga.get_i_j(child)
                    if bbga.fitness(child_i, child_j, R) == max_f:
                        flag += 1
                        break
                
                # Get out of population loop
                if flag == 1:
                    break
            
            # Get out of generation loop
            if flag == 1:
                break
        
        return generations