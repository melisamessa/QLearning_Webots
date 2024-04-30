"""mbController controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
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
## FOR Q-LEARNING
EPSILON = 0.9
DISCOUNT_FACTOR = 0.9
LEARNING_RATE = 0.9
Q_VALUES = np.zeros((environment_rows, environment_columns, 4))
actions = ['up','right','down','left']
rewards = np.full((environment_rows, environment_columns), 0)
rewards[0, 0] = 100
rewards[0, 5] = -100
X = 0
## FOR SIMPLE COMPORTAIMENT
GRIPPER_MAX_SPEED = 0.1
objective = [0, 0, 1]
greenZone = [0, 1, 0]
avoidObstacleCounter = 0
found = False
take = False

# CREATE ROBOT INSTANCE
robot = Robot()
# ENABLE SENSORS
sensors = []
sensorsNames = ['so0', 'so1', 'so2','so3','so4','so5','so6','so7',
'so8','so9','so10','so11','so12','so13','so14','so15']
for s in range(16):
    sensors.append(robot.getDevice(sensorsNames[s]))
    sensors[s].enable(TIME_STEP)

# ENABLE GROUND SENSORS
left_sensor = robot.getDevice("left_sensor")
left_sensor.enable(TIME_STEP)
right_sensor = robot.getDevice("right_sensor")
right_sensor.enable(TIME_STEP)
    
# ENABLE MOTORS
wheels = []
wheelsName = ['back left wheel',
'back right wheel',
'front left wheel',
'front right wheel']
for i in range(4):
    wheels.append(robot.getDevice(wheelsName[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)

gripperMotors = []
gripper = ["lift motor","left finger motor","right finger motor"]
for i in range(3):
    gripperMotors.append(robot.getDevice(gripper[i]))

# ENABLE CAMERA
camera = robot.getDevice("camera")
Camera.enable(camera, TIME_STEP)
camera.recognitionEnable(TIME_STEP)
CAM_WIDTH = camera.getWidth()
CAM_HEIGHT = camera.getHeight()

# ENABLE GPS
gps = GPS("gps")
gps.enable(10)
gps = robot.getDevice("gps")

# ENABLE COMPASS
compass = robot.getDevice("compass")
compass.enable(TIME_STEP)

#################################
## GRIPPER FUNCTIONS
def takeObjective():
    gripperMotors[0].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[0].setPosition(0.05)
    gripperMotors[1].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[2].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[1].setPosition(0.06)
    gripperMotors[2].setPosition(0.06)
    timeMovement(wheels, 1.25, 1.25, 4500, False)
    timeMovement(wheels, 0.0, 0.0, 1000, False)
    gripperMotors[1].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[2].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[1].setPosition(0.02)
    gripperMotors[2].setPosition(0.02)
    timeMovement(wheels, 0, 0, 500, False)
    gripperMotors[0].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[0].setPosition(0.0)
    timeMovement(wheels, 0, 0, 500, False)
    gripperMotors[0].setVelocity(2.0)
    gripperMotors[1].setVelocity(2.0)
    timeMovement(wheels, 0, 0, 1000, False)
    timeMovement(wheels, 1.25, 1.25, 1000, False)

def leaveObjective():
    timeMovement(wheels, 1.0, 1.0, 900, False)
    gripperMotors[0].setVelocity(1.5)
    gripperMotors[1].setVelocity(1.5)
    timeMovement(wheels, 0.0, 0.0, 500, False)
    gripperMotors[0].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[0].setPosition(0.05)
    timeMovement(wheels, 0, 0, 500, False)
    gripperMotors[1].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[2].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[1].setPosition(0.04)
    gripperMotors[2].setPosition(0.04)
    timeMovement(wheels, 0, 0, 500, False)
    timeMovement(wheels, -1.0, -1.0, 1150, False)    
    gripperMotors[1].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[2].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[1].setPosition(0.02)
    gripperMotors[2].setPosition(0.02)

#################################
## AVOID OBSTACLES FUNCTION
def avoidObstacles(sensors, wheels, avoidObstacleCounter):
    left_speed = 2.0
    right_speed = 2.0
    
    if (avoidObstacleCounter > 0):
        if (avoidObstacleCounter == 1):
            ## CHOCA DEL LADO DERECHO
            timeMovement(wheels, 1.0, -1.0, 4165, False)
        elif (avoidObstacleCounter == 2):
                ## CHOCA DEL LADO IZQUIERDO
            timeMovement(wheels, -1.0, 1.0, 4165, False)
        else:
            timeMovement(wheels, 1.0, -1.0, 1165, False)    
        avoidObstacleCounter = 0
    
    if (sensors[4].getValue() >= 980) or (sensors[2].getValue() >= 900) or (sensors[5].getValue() >= 900):
        avoidObstacleCounter = 1
    
    if (sensors[3].getValue() >= 980) or (sensors[4].getValue() >= 900 and sensors[3].getValue() >= 900):
        avoidObstacleCounter = 2
    
    if (sensors[5].getValue() >= 800 and sensors[7].getValue() >= 600 and sensors[8].getValue() >= 600) or (sensors[0].getValue() >= 800 and sensors[2].getValue() > 900):
        avoidObstacleCounter = 3
        
    if ((sensors[4].getValue() >= 900) and (sensors[8].getValue() > 900)):
        avoidObstacleCounter = 1
    
    if (sensors[4].getValue() >= 900) and (sensors[15].getValue() > 900):
        avoidObstacleCounter = 2
        
    changeWheelsVelocity(wheels, right_speed, left_speed)
    return avoidObstacleCounter

###############################################
### RECOGNITION FUNCTIONS
def equalsColors(objects, objective, n):
    for i in range(n):
        if (objects[i] != objective[i]):
            return False
    return True

def getRecognition(objective, objects, numberObjects):
    for i in range(numberObjects):
        if (equalsColors(objects[i].getColors(), objective, 3)):
            return i
    return -1

def goToObjective(objects, i, pos):
    position = objects[i].getPositionOnImage()
    if (position[1] == pos):
        return True
    if (position[0] < (CAM_WIDTH/2 - 1)):
        left_speed = -1.0
        right_speed = 1.0
    else:
        if (position[0] > (CAM_WIDTH/2 + 1)):
            left_speed = 1.0
            right_speed = -1.0
        else:
            left_speed = 1.0
            right_speed = 1.0
    changeWheelsVelocity(wheels, right_speed, left_speed)
    return False

#################################
# Q LEARNING FUNCTIONS
def getNextAction(row, column, epsilon):
    if (np.random.random() < epsilon):
        return np.argmax(Q_VALUES[row, column])
    else:
        return np.random.randint(4)
     
def validateAction(action, row, column, sensors):
##ARRIBA, DERECHA, ABAJO, IZQUIERDA
    if (action == 0) and ((row == 0) or (row == 3 and column == 0) or (row == 5 and column == 3)):
            return False
    elif (action == 1) and ((column == 5) or (row == 4 and column == 2)):
            return False
    elif (action == 2) and ((row == 5) or (row == 1 and column == 0) or (row == 3 and column == 3)):
        return False
    elif (action == 3) and ((column == 0) or (row == 2 and column == 1) or (row == 4 and column == 4)):
            return False
    return True

def isTerminalState(reward):
    if (reward == 0):
        return False
    else:
        return True

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
    cPosition = changePosition(start_row, start_column, row, column, wheels)
    
    while not cPosition:
        timeMovement(wheels, 1.0, 1.0, 1000, True)
        row, column = getCell(gps, cell_size)
        cPosition = changePosition(start_row, start_column, row, column, wheels)
    
    if (cPosition):
        timeMovement(wheels, 1.0, 1.0, 3500, True)
        row, column = getCell(gps, cell_size)
    return row, column
    
def avoidObstacleRow(actual_row, random_row, column, direction):
    if (column == 0 and random_row == 2):
        n_direction = moveRandomRow(actual_row, 1, direction)
        moveRandomColumn(column, column+1, n_direction)
        moveRandomRow(1, 2, "RIGHT")
        return 2, "DOWN"
    if (actual_row < 2 and random_row > 2 and column == 0):
        n_direction = moveRandomRow(actual_row, 1, direction)
        moveRandomColumn(column, column+1, n_direction)
        moveRandomRow(1, 1+2, "RIGHT")
        moveRandomColumn(column+1, column, "DOWN")
        return 3, "LEFT"
    elif (actual_row > 2 and random_row < 2 and column == 0):
        n_direction = moveRandomRow(actual_row, 3, direction)
        moveRandomColumn(column, column+1, n_direction)
        moveRandomRow(3, 3-2, "RIGHT")
        moveRandomColumn(column+1, column, "UP")
        return 1, "LEFT"
    elif (actual_row < 4 and random_row > 4 and column == 3):
        n_direction = moveRandomRow(actual_row, 3, direction)
        moveRandomColumn(column, column+1, n_direction)
        moveRandomRow(3, 3+2, "RIGHT")
        moveRandomColumn(column+1, column, "DOWN")
        return 5, "LEFT"
    elif (actual_row > 4 and random_row < 4 and column == 3):
        moveRandomColumn(column, column+1, direction)
        moveRandomRow(actual_row,  actual_row-2, "RIGHT")
        moveRandomColumn(column+1, column, "UP")
        return 3, "LEFT"
    else:
        return actual_row, direction

def avoidObstacleColumn(actual_column, row, random_column, direction):
    if (actual_column < 3 and random_column > 3 and row == 4):
        moveRandomColumn(actual_column, 2, direction)
        moveRandomRow(row, row-1, "RIGHT")
        moveRandomColumn(2, 2+2, "UP")
        moveRandomRow(row-1, row, "RIGHT")
        return 4
    elif (actual_column > 3 and random_column < 3 and row == 4):
        moveRandomColumn(actual_column, 4, direction)
        moveRandomRow(row, row-1, "LEFT")
        moveRandomColumn(4, 4-2, "UP")
        moveRandomRow(row-1, row, "LEFT")
        return 4
    else:
        return actual_column
        
def moveRandomRow(actual_row, random_row, direction):
    move = False
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
    if (actual_row == random_row):
        move = True
        actual_direction = direction
    while not (random_row == actual_row):
        timeMovement(wheels, 1.0, 1.0, 1000, True)
        actual_row, column = getCell(gps, cell_size)
    if (move == True):
        timeMovement(wheels, 0, 0, 1000, False)
    else:
        timeMovement(wheels, 1.0, 1.0, 3500, True)
    return actual_direction

def moveRandomColumn(actual_column, random_column, direction):
    move = False
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
        move = True;
        new_direction = direction
    while not (random_column == actual_column):
        timeMovement(wheels, 1.0, 1.0, 1000, True)
        row, actual_column = getCell(gps, cell_size)
    if (move == True):
        timeMovement(wheels, 0, 0, 1000, False)
    else:
        timeMovement(wheels, 1.0, 1.0, 3500, True)
    return new_direction
        
def moveRandomPosition(direction):
    actual_row, actual_column = getCell(gps, cell_size)
    row = random.randint(0, 5)
    column = random.randint(0,5)
    if ((row == 2 and column == 0) or (row == 4 and column == 3) or (row == 0 and (column == 0 or column == 5))):
        row = random.randint(0, 5)
        column = random.randint(0,5)
    new_row, row_direction = avoidObstacleRow(actual_row, row, actual_column, direction)
    if (new_row != actual_row):
        new_direction = moveRandomRow(new_row, row, row_direction)
    else:
        new_direction = moveRandomRow(actual_row, row, row_direction)
    if (row == 2 and column == 1):
        new_episode_direction = "DOWN"
    else:
        new_column = avoidObstacleColumn(actual_column, row, column, new_direction)
        if (new_column != actual_column):
            new_episode_direction = moveRandomColumn(new_column, column, "DOWN")
        else:    
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

def compassGetDirection():
    direction = ""
    orientation = compass.getValues()
    angle_degrees = math.degrees(math.atan2(orientation[1], orientation[2]))
    if (angle_degrees <= -89.9 and angle_degrees > -90.09):
        direction = "UP"
    elif ((angle_degrees > 0 and angle_degrees < 89.9) or (angle_degrees > 90.09)):
        direction = "RIGHT"
    elif (angle_degrees >= 89.9 and angle_degrees < 90.09):
        direction = "DOWN"
    elif ((angle_degrees < 0 and angle_degrees < -89.9) or (angle_degrees >= -90.09)):
        direction = "LEFT"
    return direction            

aO = avoidObstacles(sensors, wheels, avoidObstacleCounter = 0)
while robot.step(TIME_STEP) != -1:
    if (X==0):
        numberObjects = camera.getRecognitionNumberOfObjects()
        objects = camera.getRecognitionObjects()
        indice = getRecognition(objective, objects, numberObjects)
        if (indice != -1):
            found = goToObjective(objects, indice, 60)
            if found:
                take = takeObjective()
                direction = compassGetDirection()
                row, column = getCell(gps, cell_size)
                moveRandomColumn(column, column+1, direction)
                X = X+1
        else:
            aO = avoidObstacles(sensors, wheels, aO)
    if (X < 1000) and (X > 0):
        direction1 = qLearning(direction)
        if (X == 1):
            leaveObjective()
        direction = moveRandomPosition(direction1)
        X = X+1
    if (X == 1):
        changeWheelsVelocity(wheels, 0,0)
    pass

# Enter here exit cleanup code.
