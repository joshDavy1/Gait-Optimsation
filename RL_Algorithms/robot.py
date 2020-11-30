## Robot Interface library
import serial
import numpy as np
import PyCmdMessenger
from time import sleep


class Servo() :
    def __init__(self,ID,min = 0,max = 180) :
        self.ID = ID
        self.value = 0
        self.min = min
        self.max = max
        

class Robot() :
    def __init__(self) :
        ## Connect to robot
        arduino = PyCmdMessenger.ArduinoBoard("COM9",baud_rate=9600,int_bytes=4)
        commands = [
            ["hello",""],
            ["hello_return",""],
            ["set_servo","ii"],
            ["set_led","ii"],
            ["get_button","i"],
            ["button_return","i"],
            ["get_pot",""],
            ["pot_return","i"],
            ["get_encoder","i"],
            ["encoder_return","i"],
            ["set_all_servos","iiiiii"],
            ["error",""],
        ]
        self.c = PyCmdMessenger.CmdMessenger(arduino,commands)

        self.servos = []
        for i in range(0,3) :
            self.servos.append(Servo(i,0,180))
        for i in range(3,6) :
            self.servos.append(Servo(i,180,0))

        self.c.send("hello")
        msg = self.c.receive()
        try :
            if msg[0] == "hello_return" :
                print("Hello Message Returned. Sucsessful Connection")
        except :
            "Error: Hello Message Not Returned"

    def setLED(self,ledNo,value) :
        self.c.send("set_led",ledNo,value)

    def setJointRange(self,jointNo,max_servo_value,min_servo_value) :
        i = jointNo
        self.servos[i].max = max_servo_value
        self.servos[i].min = min_servo_value
    def setJointPos(self,jointNo,value) :
        i = jointNo
        self.servos[i].value = value

        pos = self.servos[i].min + (self.servos[i].max-self.servos[i].min)*value
        self.c.send("set_servo",jointNo+1,int(pos))
    
    def setAllJointPos(self,values) :
        for i in range(6) :
            self.setJointPos(i,values[i])

    def getJointPos(self,jointNo) :
        return self.servos[jointNo].value
    
    def recieveMessage(self,expected_message) :
        msg = self.c.receive()
        try :
            if msg[0] == expected_message :
                return msg[1]
            elif msg[0] == "error" :
                return "Error message returned"
            else :
                print("Error: unexpected return message")
        except :
            print(msg)
            print("Error: No message recieved")

    def getEncoderValue(self,encoderNo) :
        self.c.send("get_encoder",encoderNo)
        if encoderNo == 1 :
            return self.recieveMessage("encoder_return")[0]
        if encoderNo == 2 :
            return -self.recieveMessage("encoder_return")[0]
    
    def getButtonValue(self,buttonNo) :
        self.c.send("get_button",buttonNo)
        return self.recieveMessage("button_return")[0]
    
    def getPotValue(self) :
        self.c.send("get_pot")
        return self.recieveMessage("pot_return")[0]

if __name__ == '__main__' :
    robot = Robot()
    x  = 0.5
    robot.setLED(3,1)
    robot.setJointRange(0,0,135)
    robot.setJointRange(3,180,45)
    robot.setJointRange(1,0,135)
    robot.setJointRange(4,180,45)
    while 1:
        x = float(input())
        
        robot.setJointPos(1,x)
        robot.setJointPos(4,x)
        
        #print(robot.getEncoderValue(1),',',robot.getEncoderValue(2))

        # sleep(1)
        # robot.setJointPos(1,0.5)
        # robot.setJointPos(2,0.2)
        # robot.setJointPos(3,0.3)
        # robot.setJointPos(4,1-0.1)
        # robot.setJointPos(5,1-0.3)
        # robot.setJointPos(6,1-0.5)
        sleep(1)
    input()