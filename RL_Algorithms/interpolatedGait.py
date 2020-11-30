import numpy as np
import matplotlib.pyplot as plt
from time import sleep

from robot import Robot

class InterpolatedGait() :
    def __init__(self,noOfSteps,noOfJoints ):
        """ Initialise gait """
        self.policySize = noOfSteps * noOfJoints 
        self.noOfJoints = noOfJoints
        self.noOfSteps = noOfSteps
        self.steps = [[0 for i in range(noOfSteps)] for j in range(noOfJoints)]
        self.offset = 0.5
        
        try :
            self.robot = Robot()
            self.robot.setJointRange(0,0,135)
            self.robot.setJointRange(3,180,45)
            self.robot.setJointRange(1,0,135)
            self.robot.setJointRange(4,180,45)
        except :
            print("Could not connect to robot.")
            self.robot = None


    def setParameters(self,parameters) :
        """Unflatten parameters to step matrix"""
        for i in range(self.noOfJoints) :
            for j in range(self.noOfSteps) :
                self.steps[i][j] = parameters[self.noOfSteps*i + j]

    def getPolicyLength(self) :
        return self.policySize

    def getParameters(self) :
        """Flatten step matrix to parameter array"""
        parameters = [0 for i in range(self.policySize)]
        for i in range(self.noOfJoints) :
            for j in range(self.noOfSteps) :
                parameters[i*self.noOfSteps + j] = self.steps[i][j] 
        return parameters
        
    def interpolatePoints(self,initalValue,finalValue,points) :
        """ linear interpolation between two points """
        interpolatedPoints = [0 for i in range(points)]
        gap = (finalValue - initalValue)/points
        for i in range(points) :
            interpolatedPoints[i] = initalValue + (i*gap)
        return interpolatedPoints

    def getGait(self,noOfDiscretePoints) :
        ''' No of Discrete Steps should be a multiple of no. of steps '''
        gait = [[] for j in range(self.noOfJoints)]
        gapBetweenSteps = int(noOfDiscretePoints/(self.noOfSteps))
        for joint in range(self.noOfJoints) :
            for step in range(self.noOfSteps) :
                initalValue = self.steps[joint][step]
                if (step+1) == self.noOfSteps :
                    finalValue = self.steps[joint][0]
                else :
                    finalValue =  self.steps[joint][step+1]
                gait[joint] +=  self.interpolatePoints(initalValue,finalValue,int(gapBetweenSteps))
        return gait

    def getRightLegIndex(self,offset,noOfDiscretePoints,i) :
        ''' Returns the index for the right legs step. I.E. The step at the offset'''
        index = i + (offset*noOfDiscretePoints) - 1
        if index >= noOfDiscretePoints :
            index -= noOfDiscretePoints
        return int(index)

    def runGait(self,noOfDiscretePoints,tickTime) :
        ''' Runs gait  on the robot '''
        gait = np.array(self.getGait(noOfDiscretePoints))
        gait = gait.T
        for i in range(len(gait)) :
            leftLeg = gait[i]
            x = self.getRightLegIndex(self.offset,noOfDiscretePoints,i)
            rightLeg = gait[x-1]
            self.robot.setJointPos(0,rightLeg[0])
            self.robot.setJointPos(1,rightLeg[1])
            self.robot.setJointPos(2,rightLeg[2])
            self.robot.setJointPos(3,leftLeg[0])
            self.robot.setJointPos(4,leftLeg[1])
            self.robot.setJointPos(5,leftLeg[2])
            sleep(tickTime/1000)


if __name__ == '__main__' :
    a = InterpolatedGait(3,2)

    a.setParameters([0,0.6,0.2,0.4,0.7,0.1,5])
    print(a.getParameters())
    x = np.array(a.getGait(24))
    print(x.shape)
    plt.plot(x.T)
    plt.show()
