from interpolatedGait import InterpolatedGait
import numpy as np 
import random
from math import pi
from hillclimbing import hillclimbing
from time import sleep
import scipy


WHEEL_DIAM = 0.106
PULSES_PER_REV = 400
ENC_DIFF_CNST = 10

POLICY_LENGTH = 12
POLICY_ITERATIONS = 2
POPULATION_SIZE = 10
CROSSOVER_POINT = 0.5
MUTATION_RATE  = 0.5
MUTATION_VARIANCE = 0.1
MUTATIONS_PER_GENERATION  = 3

enc1_offset = 0
enc2_offset = 0

method = InterpolatedGait(4,3)

def crossover(a,b) :
    point = int(len(a) * CROSSOVER_POINT)
    return  np.concatenate([a[:point],b[point:]])


def mutate(a) :
    mutations = int(MUTATION_RATE * len(a))
    for i in range(mutations) :
        index = np.random.randint(0,len(a))
        a[index] = np.random.normal(0,MUTATION_VARIANCE)
    return np.clip(a,0,1)


def reset_fitness() :
    global enc1_offset,enc2_offset
    enc1_offset = method.robot.getEncoderValue(1)
    enc2_offset = method.robot.getEncoderValue(2)

def get_fitness() :
    global enc1_offset,enc2_offset
    count1 =  method.robot.getEncoderValue(1) - enc1_offset
    count2 =  method.robot.getEncoderValue(2) - enc2_offset
    count = count1+count2 - ENC_DIFF_CNST*abs(count1-count2)
    ## Convert to meters
    return round(count/PULSES_PER_REV * pi * WHEEL_DIAM,4)

def save_session(filename,population,population_scores) :
    ''' Saves the current policy_fitness_matrix '''
    filename = 'sessions\\' + filename
    print("Saving to",filename)
    np.savetxt(filename,population,delimiter=",",fmt="%.4f")
    np.savetxt("scores_"+filename,population_scores,delimiter=",",fmt="%.4f")

def load_last_session(filename) :
    filename = 'sessions\\' + filename
    return np.loadtxt(filename,delimiter=",")

def evaluation_function(policy) :
    method.setParameters(policy)
    reset_fitness()
    for i in range(2) :
        method.runGait(64,30)
    return get_fitness()
    
def generateInitalalPopulation() :
    return np.random.rand(POPULATION_SIZE,POLICY_LENGTH)


def main() :
    global method
    

    option = int(input("""Machine Learning For Walking Robot. Genetic Algorithm
                    1.  Start New Run
                    2. Continue Existing Run\n"""))
    if option == 1 :
        filename = input("Enter Filename to save new run: ")
        population = generateInitalalPopulation()
        population_scores = np.zeros(POPULATION_SIZE)
    elif option == 2 :
        filename = input("Enter filename to load:")
        population = load_last_session(filename)
        population_scores = load_last_session("scores_"+filename)

    method.robot.setLED(3,1)




if __name__ == "__main__" :


   main()


