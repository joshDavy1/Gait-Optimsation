"""A L shape attached with a joint and constrained to not tip over.
This example is also used in the Get Started Tutorial. 
"""

__docformat__ = "reStructuredText"

import sys, random
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
from pymunk import Vec2d
import numpy as np

# Proportionality constant


body = None
link1_body = None
link2_body = None
motor1 = None
motor2 = None
def add_robot(space) :
    global body,link1_body,link2_body,motor1,motor2
    # BODY
    width = 30
    length = 80
    mass = 25
    x,y = 50,350
    moment = pymunk.moment_for_box(mass, (length, width))
    body = pymunk.Body(mass, moment)
    body.position = Vec2d(x,y)
    shape = pymunk.Poly.create_box(body, (length, width))
    shape.friction = 0.6
    space.add(body,shape)

    # Link 1
    width = 5
    length = 50
    mass = 0.2
    x,y = 150,375
    moment = pymunk.moment_for_box(mass, (length, width))
    link1_body = pymunk.Body(mass, moment)
    link1_body.position = Vec2d(x,y)
    link1_shape = pymunk.Poly.create_box(link1_body, (length, width))
    link1_shape.friction = 1
    link1_body.angle = 0
    space.add(link1_body,link1_shape)
    # Link 2
    width = 5
    length = 50
    mass = 3
    x,y = 200,375
    moment = pymunk.moment_for_box(mass, (length, width))
    link2_body = pymunk.Body(mass, moment)
    link2_body.position = Vec2d(x,y)
    link2_shape = pymunk.Poly.create_box(link2_body, (length, width))
    link2_shape.friction = 10
    link2_body.angle = 0
    space.add(link2_body,link2_shape)

    ## Joints
    link1_to_base = pymunk.PinJoint(link1_body,body,(-30,-5),(45,25))
    link1_to_base.distance = 0
    space.add(link1_to_base)

    link1_to_link2 = pymunk.PinJoint(link1_body,link2_body,(30,5),(-30,-5))
    link1_to_link2.distance = 0
    space.add(link1_to_link2)

    ## Motors
    motor1 = pymunk.SimpleMotor(body,link1_body,0)
    motor1.max_force = 400000
    space.add(motor1)
    motor2 = pymunk.SimpleMotor(link1_body,link2_body,0)
    motor2.max_force = 200000
    space.add(motor2)

def add_ground(space) :
    ground = pymunk.Segment(space.static_body, (-4000, 300), (4000, 300), 2)
    ground.friction = 0.2
    space.add(ground)

# Keeps track of how many timesteps since policy began not counting current stage
x = 0
iterations = 0
def get_joint_angle(policy,visualisation) :
    global current_stage,x,iterations,time

    if time < 100 :
        return 0,0

    if time < (100+x) :
        return policy[current_stage][0:2]
    else :
        x += 100#policy[current_stage][2] 
        current_stage += 1
        # if visualisation:
        #     input()
        if current_stage == len(policy) :
            # if visualisation :
            #     print("hi")
            current_stage = 0
            iterations += 1
        return policy[current_stage][0:2]

key_pressed = False
p = 4
time = 0
current_stage = 0
distance = 0
def test_policy(policy,tickrate,generation,policyNo,visualisation,noIterations) :
    global time,iterations,distance,key_pressed
    iterations = 0

    if visualisation :
        pygame.init()
        screen = pygame.display.set_mode((1000, 600))
        pygame.display.set_caption("Crawler Robot")
        clock = pygame.time.Clock()
        draw_options = pymunk.pygame_util.DrawOptions(screen)
    

    # Space
    space = pymunk.Space()
    space.gravity = (0.0, -500.0)
    add_robot(space)
    add_ground(space)

    
    while True:
        if visualisation :
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

        # get current joint angles
        a,b = get_joint_angle(policy,visualisation)
        a = np.radians(a)
        b = np.radians(b)

        # Proportional Control
        delta1 = a - link1_body.angle 
        motor1.rate = -p*delta1
        delta2 = b - (link2_body.angle)
        motor2.rate = -p*delta2

        # Text
        if visualisation :
            font = pygame.font.Font('freesansbold.ttf', 16) 
            text = font.render('Generation: ' + str(generation) + " Policy Number: " + str(policyNo)
            + " Score: " + str(round(body.position.x-50,1)), True, (0,0,0),(255,255,255))
            textRect = text.get_rect() 
            textRect.center = (300,100)

         # time and draw
        space.step(1/200.0)
        if visualisation :
            screen.fill((255,255,255))
            screen.blit(text,textRect)
            space.debug_draw(draw_options)
            pygame.display.flip()
            clock.tick(tickrate)
        time += 1
        # After 5 iterations break
        if iterations == noIterations :
            break
    
    # return wasnt working idk why so it just assigns a variable
    distance = body.position.x - 50

def is_key_pressed() :
    return key_pressed



# distance of last run
def get_last_distance() :
    return distance
