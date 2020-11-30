import numpy as np

def crossover(a,b,crossoverPoint) :
    point = int(len(a) * crossoverPoint)
    return  np.concatenate([a[:point],b[point:]])

def mutate(a,rate,variance) :
    mutations = int(rate * len(a))
    for i in range(mutations) :
        index = np.random.randint(0,len(a))
        a[index] = np.random.normal(0,variance)
    return np.clip(a,0,1)


def generateInitalalPopulation(popSize,policyLength) :
    return np.random.rand(popSize,policyLength)


def genetic(evaluation_func,iterations,policyLength,popSize,mutsPerGen) :
        population = generateInitalalPopulation()
        population_scores = np.zeros(popSize)
        population_scores[:] = np.nan

        while 1 :
        # Main Loop
            # Evaluate all none evaluated
            for i in range(popSize) :
                if population_scores[i] == np.nan :
                    population_scores[i] = evaluation_func(population[i,:])
                    print(i," scores",population_scores[i])


            print(population_scores)
            sorted_indexes = np.argsort(population_scores)
            print(sorted_indexes)
            parent1 = population[sorted_indexes[0],:]
            parent2 = population[sorted_indexes[1],:]
            child = crossover(parent1,parent2)
            worst_policy_index = sorted_indexes[-1]
            population[worst_policy_index,:] = child
            population_scores[worst_policy_index] = 0
            for i in range(mutsPerGen) :
                index = np.random.randint(0,popSize) 
                population[index,:] = mutate(population[index,:])
                population_scores[index] = 0



