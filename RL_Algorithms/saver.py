import numpy as np

def append_policy(filename,policy,fitness) :
    policy_fitness = np.concatenate([policy,[fitness]])
    filename = 'sessions\\' + filename
    try :
        policy_fitness_matrix = np.loadtxt(filename,delimiter=",")
    except :
        policy_fitness_matrix = np.zeros((1,len(policy)+1))
    policy_fitness_matrix = np.concatenate([policy_fitness_matrix,[policy_fitness]])
    print("Saving to",filename)
    np.savetxt(filename,policy_fitness_matrix,delimiter=",",fmt="%.4f")