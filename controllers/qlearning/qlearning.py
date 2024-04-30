"""qlearning controller."""

# You may need to import some classes of the controller module. Ex:

from controller import Robot, Motor, DistanceSensor, GPS
from controller import Camera, CameraRecognitionObject
import numpy as np
import math
import random

TIME_STEP = 64
MAX_SPEED = 3
##ENVIRONMENT
environment_rows = 6
environment_columns = 6
cell_size = 2
SIZE = 6
AUX = 0

## FOR Q-LEARNING
EPSILON = 0.9
DISCOUNT_FACTOR = 0.9
LEARNING_RATE = 0.9
Q_VALUES = np.zeros((environment_rows, environment_columns, 4))
actions = ['up','right','down','left']
rewards = np.full((environment_rows, environment_columns), 0)
rewards[0, 2] = 100
rewards[1, 4] = -100

# create the Robot instance.
robot = Robot()
#Enable sensors:
sensors = []
sensorsNames = ['so0', 'so1', 'so2','so3','so4','so5','so6','so7',
'so8','so9','so10','so11','so12','so13','so14','so15']
for s in range(16):
    sensors.append(robot.getDevice(sensorsNames[s]))
    sensors[s].enable(TIME_STEP)
##GROUND SENSORS
#center_sensor = robot.getDevice("center_sensor")
#center_sensor.enable(TIME_STEP)
left_sensor = robot.getDevice("left_sensor")
left_sensor.enable(TIME_STEP)
right_sensor = robot.getDevice("right_sensor")
right_sensor.enable(TIME_STEP)
    
    # Enable motors:
wheels = []
wheelsName = ['back left wheel',
'back right wheel',
'front left wheel',
'front right wheel']
for i in range(4):
    wheels.append(robot.getDevice(wheelsName[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)

##CAMERA
camera = robot.getDevice("camera")
Camera.enable(camera, TIME_STEP)
camera.recognitionEnable(TIME_STEP)
CAM_WIDTH = camera.getWidth()
CAM_HEIGHT = camera.getHeight()

##GPS
gps = GPS("gps")
gps.enable(10)
gps = robot.getDevice("gps")

#################################
#################################
#################################
####Q LEARNING FUNCTIONS
def getNextAction(row, column, epsilon):
    if (np.random.random() < epsilon):
        return np.argmax(Q_VALUES[row, column])
    else:
        return np.random.randint(4)
     
def validateAction(action, row, column, sensors):
##UP, RIGHT, DOWN, LEFT
    if (action == 0) and (row == 0):
            return False
    elif (action == 1) and (column == 5):
            return False
    elif (action == 2) and (row == 5):
        return False
    elif (action == 3) and (column == 0):
            return False
    return True

def isTerminalState(reward):
    if (reward == 0):
        return False
    else:
        return True

#################################
#################################
#################################

def changeWheelsVelocity(wheels, r_speed, l_speed):
    wheels[0].setVelocity(l_speed)
    wheels[2].setVelocity(l_speed)
    wheels[1].setVelocity(r_speed)
    wheels[3].setVelocity(r_speed)
    return 0
    
def timeMovement(wheels, r_speed, l_speed, time, straight):
    changeWheelsVelocity(wheels, r_speed, l_speed)
    ms = time
    elapsed_time = 0
    while (elapsed_time < ms):
        if (straight):
            straighten()
        robot.step(TIME_STEP)
        elapsed_time += TIME_STEP

def getCell(gps, cell_size):
    position = gps.getValues()
    row = int((position[0] + (SIZE / 2)))
    column = int((position[1] + (SIZE/2)))
    return row, column

def changePosition(row, column, n_row, n_column, wheels):
    if ((row != n_row) or (column != n_column)):
        return True
    else:
        return False

def newCell():
    start_row, start_column = getCell(gps, cell_size)
    row, column = getCell(gps, cell_size)
    aux = changePosition(start_row, start_column, row, column, wheels)
    
    while not aux:
        timeMovement(wheels, 1.0, 1.0, 1000, True)
        row, column = getCell(gps, cell_size)
        aux = changePosition(start_row, start_column, row, column, wheels)
    
    if (aux):
        timeMovement(wheels, 1.0, 1.0, 3500, True)
        row, column = getCell(gps, cell_size)
    return row, column

def moveRandomRow(actual_row, random_row, direction):
    aux = False
    if (actual_row > random_row):
        if (direction == "UP"):
            timeMovement(wheels, 0, 0, 1200, False)
        elif (direction == "DOWN"):
             timeMovement(wheels, -1.0, 1.0, 4200 * 2, False)
        elif (direction == "RIGHT"):
            timeMovement(wheels, 1.0, -1.0, 4200, False)
        elif (direction == "LEFT"):
            timeMovement(wheels, -1.0, 1.0, 4200, False)
        actual_direction = "UP"
    elif (actual_row < random_row):
        if (direction == "UP"):
            timeMovement(wheels, -1.0, 1.0, 4200 * 2, False)
        elif (direction == "DOWN"):
            timeMovement(wheels, 0, 0, 1200, False)
        elif (direction == "RIGHT"):
            timeMovement(wheels, -1.0, 1.0, 4200, False)
        elif (direction == "LEFT"):
            timeMovement(wheels, 1.0, -1.0, 4200, False)
        actual_direction = "DOWN"
    elif (actual_row == random_row):
        aux = True
        actual_direction = direction
    while not (random_row == actual_row):
        timeMovement(wheels, 1.0, 1.0, 1000, True)
        actual_row, column = getCell(gps, cell_size)
    if (aux == True):
        timeMovement(wheels, 0, 0, 1000, False)
    else:
        timeMovement(wheels, 1.0, 1.0, 3500, True)
    return actual_direction

def moveRandomColumn(actual_column, random_column, direction):
    aux = False
    if (actual_column > random_column):
        if (direction == "UP"):
            timeMovement(wheels, 1.0, -1.0, 4200, False)
        elif (direction == "DOWN"):
            timeMovement(wheels, -1.0, 1.0, 4200, False)
        elif (direction == "RIGHT"): 
            timeMovement(wheels, -1.0, 1.0, 4200 * 2, False)
        elif (direction == "LEFT"):
            timeMovement(wheels, 0, 0, 1200, False)
        new_direction = "LEFT"  
    elif (actual_column < random_column):
        if (direction == "UP"):
            timeMovement(wheels, -1.0, 1.0, 4200, False)
        elif (direction == "DOWN"):
            timeMovement(wheels, 1.0, -1.0, 4200, False)
        elif (direction == "RIGHT"): 
            timeMovement(wheels, 0, 0, 1200, False)
        elif (direction == "LEFT"):
            timeMovement(wheels, -1.0, 1.0, 4200 * 2, False)
        new_direction = "RIGHT"
    elif(actual_column == random_column):
        aux = True;
        new_direction = direction
    while not (random_column == actual_column):
        timeMovement(wheels, 1.0, 1.0, 1000, True)
        row, actual_column = getCell(gps, cell_size)
    if (aux == True):
        timeMovement(wheels, 0, 0, 1000, False)
    else:
        timeMovement(wheels, 1.0, 1.0, 3500, True)
    return new_direction
        
def moveRandomPosition(direction):
    actual_row, actual_column = getCell(gps, cell_size)
    row = random.randint(0, 5)
    column = random.randint(0,5)
    new_direction = moveRandomRow(actual_row, row, direction)
    new_episode_direction = moveRandomColumn(actual_column, column, new_direction)
    return new_episode_direction

def getMovement(row, column, wheels, sensors, direction):
    action = getNextAction(row, column, EPSILON)
    while not (validateAction(action, row, column, sensors)):
        action = getNextAction(row, column, EPSILON)
    if actions[action] == 'up':
        if (direction == "UP"):
            timeMovement(wheels, 0, 0, 1200, False)
        elif (direction == "DOWN"):
             timeMovement(wheels, -1.0, 1.0, 4200 * 2, False)
        elif (direction == "RIGHT"):
            timeMovement(wheels, 1.0, -1.0, 4200, False)
        elif (direction == "LEFT"):
            timeMovement(wheels, -1.0, 1.0, 4200, False)
    elif actions[action] == 'right':
        if (direction == "UP"):
            timeMovement(wheels, -1.0, 1.0, 4200, False)
        elif (direction == "DOWN"):
            timeMovement(wheels, 1.0, -1.0, 4200, False)
        elif (direction == "RIGHT"): 
            timeMovement(wheels, 0, 0, 1200, False)
        elif (direction == "LEFT"):
            timeMovement(wheels, -1.0, 1.0, 4200 * 2, False)
    elif actions[action] == 'down':
        if (direction == "UP"):
            timeMovement(wheels, -1.0, 1.0, 4200 * 2, False)
        elif (direction == "DOWN"):
            timeMovement(wheels, 0, 0, 1200, False)
        elif (direction == "RIGHT"):
            timeMovement(wheels, -1.0, 1.0, 4200, False)
        elif (direction == "LEFT"):
            timeMovement(wheels, 1.0, -1.0, 4200, False)
    elif actions[action] == 'left':
        if (direction == "UP"):
            timeMovement(wheels, 1.0, -1.0, 4200, False)
        elif (direction == "DOWN"):
            timeMovement(wheels, -1.0, 1.0, 4200, False)
        elif (direction == "RIGHT"):
            timeMovement(wheels, -1.0, 1.0, 4200 * 2, False)
        elif (direction == "LEFT"):
            timeMovement(wheels, 0, 0, 1200, False)      
    return action

def getDirection(action):
    if (action == 0):
        return "UP"
    elif (action == 1):
        return "RIGHT"
    elif (action == 2):
        return "DOWN"
    elif (action == 3):
        return "LEFT"

def qLearning(direction):
    row, column = getCell(gps, cell_size)
    is_terminal = isTerminalState(rewards[row, column])
    while not (is_terminal):
        old_row, old_column = row, column
        action = getMovement(row, column, wheels, sensors, direction)
        direction = getDirection(action)
        row, column = newCell()
        reward = rewards[row, column]

        old_q_value = Q_VALUES[old_row, old_column, action]

        temporal_difference = reward + (DISCOUNT_FACTOR * np.max(Q_VALUES[row, column])) - old_q_value

        new_q_value = old_q_value + (LEARNING_RATE * temporal_difference)

        Q_VALUES[old_row, old_column, action] = new_q_value

        print("Q_VALUES: ")
        print(Q_VALUES)
       
        is_terminal = isTerminalState(rewards[row, column])

    return direction
        
def straighten():
    left_value = left_sensor.getValue()
    right_value = right_sensor.getValue()
    left_speed = 1.0
    right_speed = 1.0
    if (left_value == 1000.0 and right_value < 1000.0):
        right_speed = -1.0
    if (right_value == 1000.0 and left_value < 1000.0):
        left_speed = -1.0
    if (left_value == 1000.0 and right_value == 1000.0):
        left_speed = 1.0
        right_speed = 1.0
    changeWheelsVelocity(wheels, right_speed, left_speed)
        

x= 0
while robot.step(TIME_STEP) != -1:
    if (x==0):
        direction = "DOWN"
    if (x != 1000):
        direction1 = qLearning(direction)
        direction = moveRandomPosition(direction1)
        x = x+1
    if (x == 1000):
        changeWheelsVelocity(wheels, 0,0)

    
    pass
# Enter here exit cleanup code.


