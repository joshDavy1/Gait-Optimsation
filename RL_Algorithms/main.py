import numpy as np 
import random

## Gait Parameter style
from interpolatedGait import InterpolatedGait
from osscilatoryGait import OsscilatoryGait
## Evalute gait on robot 
from evalFunc import evaluation_function
## Minimisation method
from skopt import gp_minimize
from hillclimbing import hillClimbing
from genetic import genetic

# Selected gait method
#method = InterpolatedGait(3,3)
method = OsscilatoryGait(3)
POLICY_LENGTH = method.getPolicyLength()


def main() :
    ## Save policy fitnesses as we go
    filename = input("Enter filename: ")
    def eval(policy) :
        return evaluation_function(policy,filename,method)

    res = gp_minimize(func = eval,
                      dimensions = [[0.,1,] for i in range(POLICY_LENGTH)],
                      acq_func="LCB",
                      n_calls = 50,
                      noise = 500,
                      kappa = 25,
                      verbose = True,
                      n_random_starts = 1,
                      random_state = random.randint(0,999))
    print(res)


if __name__ == "__main__" :
   main()


