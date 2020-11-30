from interpolatedGait import InterpolatedGait
import numpy as np 
import random
from math import pi
from hillclimbing import hillclimbing
from time import sleep

WHEEL_DIAM = 0.106
PULSES_PER_REV = 400
ENC_DIFF_CNST = 10

POLICY_LENGTH = 12
POLICY_ITERATIONS = 2

enc1_offset = 0
enc2_offset = 0

method = None


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

def random_policy(len) :
    policy = []
    for i in range(len) :
        policy.append(round(random.random(),4))
    return policy

def save_session(filename,policy_fitness_matrix) :
    ''' Saves the current policy_fitness_matrix '''
    filename = 'sessions\\' + filename
    print("Saving to",filename)
    np.savetxt(filename,policy_fitness_matrix,delimiter=",",fmt="%.4f")

def update_policy_fitness_matrix(policy_fitness_matrix,current_policy,fitness) :
    policy_fitness = np.concatenate([current_policy,fitness])
    return np.concatenate([policy_fitness_matrix,[policy_fitness]])


def load_last_session(filename) :
    filename = 'sessions\\' + filename
    return np.loadtxt(filename,delimiter=",")

def get_new_policy(current_policy,evaluation_func) :
    return hillclimbing(current_policy,evaluation_func)

def evaluation_function(policy) :
    method.setParameters(policy)
    reset_fitness()
    for i in range(2) :
        method.runGait(64,30)
    return get_fitness()
    

def main() :
    global method
    method = InterpolatedGait(4,3)

    option = int(input("""Machine Learning For Walking Robot.
                    1.  Start New Run
                    2. Continue Existing Run\n"""))
    if option == 1 :
        filename = input("Enter Filename to save new run: ")
        current_policy = random_policy(POLICY_LENGTH)
        policy_fitness_matrix = np.zeros([1,POLICY_LENGTH+1])
    elif option == 2 :
        filename = input("Enter filename to load:")
        policy_fitness_matrix = load_last_session(filename)
        current_policy = policy_fitness_matrix[-1,:-1]

    method.robot.setLED(3,1)
    while 1 :
        # Main Loop
        current_policy,fitness = get_new_policy(current_policy,evaluation_function)
        print("Current Policy:" ,current_policy)
        print("Fitness:",fitness)
        input()
        policy_fitness_matrix = update_policy_fitness_matrix(policy_fitness_matrix,current_policy,fitness)
        save_session(filename,policy_fitness_matrix)


if __name__ == "__main__" :


   main()


