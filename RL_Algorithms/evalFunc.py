
import numpy as np 
import random
from math import pi

from time import sleep
from saver import append_policy

WHEEL_DIAM = 0.106
PULSES_PER_REV = 400
ENC_DIFF_CNST = 1/25

POLICY_ITERATIONS = 3

enc1_offset = 0
enc2_offset = 0


def reset_fitness(method) :
    global enc1_offset,enc2_offset
    enc1_offset = method.robot.getEncoderValue(1)
    enc2_offset = method.robot.getEncoderValue(2)

def get_fitness(method) :
    global enc1_offset,enc2_offset
    count1 =  method.robot.getEncoderValue(1) - enc1_offset
    count2 =  method.robot.getEncoderValue(2) - enc2_offset
    count = -(count1+count2 - ENC_DIFF_CNST*abs(count1-count2))
    return round(count,4)


def evaluation_function(policy,filename,method) :
    method.setParameters(policy)
    for i in range(6) :
        method.robot.setJointPos(i,1)
    input()
    reset_fitness(method)
    #reset_fitness(method)
    for i in range(POLICY_ITERATIONS) :
        method.runGait(64,30)
    fit = get_fitness(method)
    append_policy(filename,policy,fit)
    print(fit)
    return fit
