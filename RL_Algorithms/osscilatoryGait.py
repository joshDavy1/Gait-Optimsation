from math import sin
import numpy as np
import matplotlib.pyplot as plt
from time import sleep
from robot import Robot
PI = 3.1412
freq = 1

class OsscilatoryGait() :
    def __init__(self,noOfJoints) :
        self.gaitParameters = [[0 for i in range(2)] for j in range(noOfJoints)]
        self.policySize = 2*noOfJoints 
        self.noOfJoints = noOfJoints
        self.offset = 0.5
        try :
            self.robot = Robot()
            self.robot.setJointRange(0,0,135)
            self.robot.setJointRange(3,180,45)
            self.robot.setJointRange(1,0,135)
            self.robot.setJointRange(4,180,45)
            sleep(0.5)
        except :
            print("Could not connect to robot.")
            exit()
            

    
    def getPolicyLength(self) :
        return self.policySize

    def setParameters(self,paramaters) :
        for i in range(self.noOfJoints) :
            for j in range(2) :
                self.gaitParameters[i][j] = paramaters[2*i+j]
        #print(self.gaitParameters)

    def getParameters(self) :
        parameters = [0 for i in range(self.policySize)]
        for i in range(self.noOfJoints) :
            for j in range(2) :
                parameters[2*i+j] = self.gaitParameters[i][j]
        return parameters

    def mapTo(self,x,lowerValue,upperValue) :
        return lowerValue + (upperValue-lowerValue)*x

    def getGait(self,noOfDiscretePoints,freq) :
        gait = [[0 for i in range(noOfDiscretePoints)] for i in range(self.noOfJoints)]
        for i in range(self.noOfJoints) :
            amplitude = self.gaitParameters[i][0]
            phase = self.gaitParameters[i][1]
            frequency = freq/noOfDiscretePoints
            
            for t in range(len(gait[i])) :
                gait[i][t] = (1/2) + (amplitude/2)*sin(2*PI*frequency*t+phase*PI)
        return gait

    def getRightLegIndex(self,offset,noOfDiscretePoints,i) :
        ''' Returns the index for the right legs step. I.E. The step at the offset'''
        index = i + (offset*noOfDiscretePoints) - 1
        if index >= noOfDiscretePoints :
            index -= noOfDiscretePoints
        return int(index)

    def runGait(self,noOfDiscretePoints,tickTime) :
        ''' Runs gait  on the robot '''
        gait = np.array(self.getGait(noOfDiscretePoints,freq))
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
    a = OsscilatoryGait(3)
    a.setParameters([0.2,1,0.2,0.4,0.7,0.1])
    print(a.getParameters())
    x = np.array(a.getGait(300,5))
    print(x.shape)
    plt.plot(x.T)
    plt.show()