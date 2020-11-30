import test
import numpy as np
import random
import matplotlib.pyplot as plt
import pickle
import matplotlib.animation as animation
# simulation settings
visualisation = True
initial = 4
generations = 100
variation = 10
keep_current = False
testing = True
variations = 10
live_plotting = True
noIterations = 5

# Blank policy / good policy
if initial == 0 :
    inital_policy = [
            [0,0],
            [0,0],
            [0,0],
            [0,0],
            [0,0],
        ]
elif initial == 1 :
    inital_policy = [[-93.95865210645813, -42.01826709837254], [11.724343264726452, -3.394009889013544], [-29.974470936390645, -18.996160970053797], [-64.51436799243704, -64.38077651541987], [-95.20767453524897, -31.110187757464562]]
elif initial == 2 :
    inital_policy =[[-11.263925207248032, -154.68153321544162], [-169.81186073335996, -105.56273992160479], [123.34329810071466, 83.22316633224834], [-39.991183226461246, 89.6327364519376], [-166.79605535018376, -76.37569404869171]]
elif initial == 3:    
    inital_policy = [[-174.18295153485295, 180], [44.138433624322914, -180], [-145.2336601315913, -95.80887101514789], [173.24468955328734, 173.02571276805347], [56.42841653239217, -34.16099933905347]]
elif initial == 4:
    inital_policy = [[162.41911476729254, 13.246722436716706], [5.4666851809332035, -101.602987822853], [-141.7095642119753, -108.98188420894306], [57.24048448936381, -156.6599530896463], [-177.30953336973886, -101.74665422321108]]
def create_variations(policy) :
    ''' Creates Variations of existing policy '''
    policys = [[[0 for j in range(2)]for i in range(5)]for i in range(variations)]
    for k in range(variations):
        for i in range(5) :
            for j in range(2) :
                e = np.random.normal(0,variation)
                policys[k][i][j] = policy[i][j] + e
                # Apply limits
                if policys[k][i][j] < -180 :
                    policys[k][i][j] = -180
                if  policys[k][i][j] > 180 :
                    policys[k][i][j] = 180
    # If keep_current policy then replace the last policy with the current
    if keep_current :
        policys[variations-1] = policy
    return policys

def test_policy(policy,generation,i,visualisation) :
    test.test_policy(policy,500000,generation,i,visualisation,noIterations)
    return test.get_last_distance()


def hillclimb() :
    scores_over_time = []
    volume_over_time = []
    all_generations = []
    difference_over_time= []
    current_policy = inital_policy
    generation = 0
    fig, axs = plt.subplots(2, 1)
    fig.show()
    fig.canvas.draw()
    axs[0].set(xlabel='', ylabel='Distance')
    axs[1].set(xlabel='', ylabel='Volume Explored')
    #axs[2].set(xlabel='Generation', ylabel='Difference')
    while (not test.is_key_pressed()) and (generation < generations)  :
        policys = create_variations(current_policy)
        scores = [0 for i in range(len(policys))]

        for i in range(len(policys)) :
            scores[i] = test_policy(policys[i],generation,i,visualisation) 

        highest_score_index = np.argmax(scores)
        difference_over_time.append(calcuate_policy_difference(current_policy,
        policys[highest_score_index]))
        current_policy = policys[highest_score_index]
        all_generations.append(current_policy)
        generation += 1

        print("My Generation: ",generation)
        print("Best policy was: ",highest_score_index, " with a score of ",scores[highest_score_index],".")
        print(current_policy)

        # Data
        volume = volume_explored(current_policy)
        print("Volume: ", volume)
        volume_over_time.append(volume)
        scores_over_time.append(scores[highest_score_index])

        
        if live_plotting :
            axs[0].plot(scores_over_time,color = "blue")
            axs[1].plot(volume_over_time,color = "red")
            #axs[2].plot(difference_over_time,color = "green")
            plt.pause(0.001) 
            fig.canvas.show()
    axs[0].plot(scores_over_time,color = "blue")
    axs[1].plot(volume_over_time,color = "red")
    #axs[2].plot(difference_over_time,color = "green")
    plt.draw()
    while 1 :
        a = int(input("Enter Generation to view: "))
        test_policy(all_generations[a-1],a,-1,True)
    plt.show()

lowest_values = [[999999 for i in range(2)] for j in range(5)]
highest_values = [[-999999 for i in range(2)] for j in range(5)]
def volume_explored(policy):
    global lowest_values,highest_values
    for i in range(5) :
        for j in range(2) :
            if policy[i][j] < lowest_values[i][j] :
                lowest_values[i][j] = policy[i][j]
            if policy[i][j] >  highest_values[i][j] :
                highest_values[i][j] = policy[i][j]
    return np.sum(np.array(highest_values) - np.array(lowest_values))

def calcuate_policy_difference(policy1,policy2) :
    return np.sum(np.absolute(np.array(policy1)-np.array(policy2)))

def main() :
    if testing :
        print(test_policy(inital_policy,-1,-1,visualisation))
        print(test_policy(inital_policy,-1,-1,visualisation))
    else :
        hillclimb()
if __name__ == '__main__':
    main()