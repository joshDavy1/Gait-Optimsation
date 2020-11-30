import numpy as np
import random


def createPermutations(policy,n,variance) :
    variations = np.zeros((n,len(policy)))
    for i in range(n-1) :
        variations[i,:] = np.round(np.clip(np.random.normal(policy,variance),0,1),4)
    variations[n-1,:] = np.array(policy)
    print(variations)
    return variations


def randomPolicy(len) :
    policy = []
    for i in range(len) :
        policy.append(round(random.random(),4))
    return policy


def hillClimbing(evaluation_func,iterations,random_starts,seed,policyLength,noOfPermuations,variance) :

    random_policys = []
    scores = []
    random.seed(seed)
    for i in range(random_starts) :
        p = randomPolicy(policyLength)
        random_policys.append(p)
        scores.append(evaluation_func(p))
    index_of_max = np.argmax(scores)
    current_policy = random_policys[index_of_max]
    iterations -= random_starts

    print(current_policy)

    rounds = 0
    while iterations > 0 :  
        print("Iteration",rounds,".")
        permuations = createPermutations(randomPolicy(policyLength),noOfPermuations,variance)
        scores = np.zeros((noOfPermuations,1))
        for i in range(noOfPermuations) :
            scores[i] = evaluation_func(permuations[i,:])
            print("Variation",permuations[i,:],"scores",scores[i])
        index_of_max = np.argmax(scores)
        current_policy =  permuations[index_of_max,:]
        iterations -= noOfPermuations
        rounds += 1
        print("i",index_of_max)
    print(current_policy)
    print("DONE")





################# TESTING ################

def evalu(policy) :
    return np.sum(policy)

if __name__ == "__main__":


    x = hillClimbing(evalu,1000,5,123,6,10,0.5)