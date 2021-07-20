import pandas as pd
import random

class bbga:

    def __init__(self):
        pass
    
    # MAKE POPULATION
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

    # 2 BLOCK FITNESS
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

    # 3 BLOCK FITNESS
    @staticmethod
    def fitness_3_block(i: int, j: int, k: int,  R):
        r = R[i][j]
        f = r * (2**i + 2**j + 2**k)
        return f

    @staticmethod
    def get_i_j_k(individual: str):
        index = int(len(individual)/3)
        first_gene, second_gene, third_gene = individual[:index], individual[index:2*index], individual[2*index:]
        i, j, k = first_gene.count('1'), second_gene.count('1'), third_gene.count('1')
        return i, j, k

    @staticmethod
    def max_3block_fitness(n: int, R):
        max_f = bbga.fitness_3_block(n, n, n, R)
        return max_f

    # MUTATION
    @staticmethod
    def mutate(individual: str, n: int, blocks: int) -> str:
        if (blocks == 2):
            val = 2
        else:
            val = 3
        mutated_individual = ['']*val*n
        for i in range(len(individual)):
            if random.random() < (1 / (val*n)):
                mutated_individual[i] = random.choice(['0', '1'])
            else:
                mutated_individual[i] = individual[i]
        return ''.join(mutated_individual)

    # CROSSOVER
    @staticmethod
    def one_point_crossover(parent_1: str, parent_2: str) -> str:
        pointer = random.randrange(0, len(parent_1) - 1)
        new_gene_1 = parent_1[0:pointer]
        new_gene_2 = parent_2[pointer:]
        child = new_gene_1 + new_gene_2
        return child

    @staticmethod
    def two_point_crossover(parent_1: str, parent_2: str) -> str:
        pointer_1 = random.randrange(0, len(parent_1) - 1)
        pointer_2 = random.randrange(0, len(parent_1) - 1)
        while pointer_1 == pointer_2:
            pointer_2 = random.randrange(0, len(parent_1) - 1)
        if pointer_1 > pointer_2:
            pointer_1, pointer_2 = pointer_2, pointer_1
        new_gene_1 = parent_1[0:pointer_1]
        new_gene_2 = parent_2[pointer_1:pointer_2]
        new_gene_3 = parent_1[pointer_2:]
        child = new_gene_1 + new_gene_2 + new_gene_3
        return child

    @staticmethod
    def case_handler(deme, n: int, case: int, blocks:int) -> str:
        parent_1 = random.choice(deme)
        parent_2 = random.choice(deme)

        # Experiment 0, one point crossover
        if case == 0:
            cross = bbga.one_point_crossover(parent_1, parent_2)
            return bbga.mutate(cross, n, blocks)

        # Experiment 1, two point crossover
        elif case == 1:
            cross = bbga.two_point_crossover(parent_1, parent_2)
            return bbga.mutate(cross, n, blocks)

        else:
            print('--- CASE ERROR ---')
            return

    @staticmethod
    def ga_extension(n: int, case: int, blocks: int):
    
        generations = 0
        population = bbga.make_population(n)
        R = bbga.make_R(n)
        if(blocks == 2):
            max_f = bbga.max_fitness(n, R)
        else:
            val = int((n * 2) / 3)
            max_f = bbga.fitness_3_block(val, val, val, R)
        flag = 0
        
        while generations <= 2000:
                            
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

                    child = bbga.case_handler(deme, n, case, blocks)
                    # Choose an individual to be replaced
                    index_a = random.randrange(0, len(deme) - 1)
                    individual_a = deme[index_a]

                    index_b = random.randrange(0, len(deme) - 1)
                    individual_b = deme[index_b]
                    
                    if (blocks == 2):
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

                    else:
                        a_i, a_j, a_k = bbga.get_i_j_k(individual_a)
                        b_i, b_j, b_k = bbga.get_i_j_k(individual_b)
                        
                        if bbga.fitness_3_block(a_i, a_j, a_k, R) > bbga.fitness_3_block(b_i, b_j, b_k, R):
                            deme[index_b] = child
                        else:
                            deme[index_a] = child
                        
                        # Has max fitness been found
                        child_i, child_j, child_k = bbga.get_i_j_k(child)
                        if bbga.fitness_3_block(child_i, child_j, child_k, R) == max_f:
                            flag += 1
                            break
                
                # Get out of population loop
                if flag == 1:
                    break
            
            # Get out of generation loop
            if flag == 1:
                break
        
        return generations

if __name__ == "__main__":
    gas = bbga()
    cases = [0, 1]
    blocks = [2, 3]
    n_vals = [6, 12, 24, 36, 48]
    for block_size in blocks:
        print('\nBLOCK SIZE:', block_size)
        for case in cases:
            print('\nCASE:', case)
            for n in n_vals:
                print('N:', n)
                results = []
                for i in range(30):
                    val = gas.ga_extension(n, case, block_size)
                    if (val < 2000):
                        results.append(val)
                print(results)