"""simpleComportaiment controller."""

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

## FOR SIMPLE COMPORTAIMENT
GRIPPER_MAX_SPEED = 0.1
objective = [0, 0, 1]
greenZone = [0, 1, 0]
avoidObstacleCounter = 0
found = False
take = False

# create the Robot instance.
robot = Robot()

##ENABLE SENSORS:
sensors = []
sensorsNames = ['so0', 'so1', 'so2','so3','so4','so5','so6','so7',
'so8','so9','so10','so11','so12','so13','so14','so15']
for s in range(16):
    sensors.append(robot.getDevice(sensorsNames[s]))
    sensors[s].enable(TIME_STEP)

##ENABLE GROUND SENSORS
left_sensor = robot.getDevice("left_sensor")
left_sensor.enable(TIME_STEP)
right_sensor = robot.getDevice("right_sensor")
right_sensor.enable(TIME_STEP)
    
##ENABLE MOTORS:
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

##ENABLE CAMERA
camera = robot.getDevice("camera")
Camera.enable(camera, TIME_STEP)
camera.recognitionEnable(TIME_STEP)
CAM_WIDTH = camera.getWidth()
CAM_HEIGHT = camera.getHeight()

##ENABLE GPS
gps = GPS("gps")
gps.enable(10)
gps = robot.getDevice("gps")

##ENABLE COMPASS
compass = robot.getDevice("compass")
compass.enable(TIME_STEP)

#################################
## GENERAL FUNCTIONS
def changeWheelsVelocity(wheels, r_speed, l_speed):
    wheels[0].setVelocity(l_speed)
    wheels[2].setVelocity(l_speed)
    wheels[1].setVelocity(r_speed)
    wheels[3].setVelocity(r_speed)
    return 0

def timeMovement(wheels, r_speed, l_speed, time):
    changeWheelsVelocity(wheels, r_speed, l_speed)
    elapsed_time = 0
    while (elapsed_time < time):
        robot.step(TIME_STEP)
        elapsed_time += TIME_STEP

#################################
## GRIPPER FUNCTIONS
def takeObjective():
    gripperMotors[0].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[0].setPosition(0.05)
    gripperMotors[1].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[2].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[1].setPosition(0.06)
    gripperMotors[2].setPosition(0.06)
    timeMovement(wheels, 1.25, 1.25, 4500)
    timeMovement(wheels, 0.0, 0.0, 1000)
    gripperMotors[1].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[2].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[1].setPosition(0.02)
    gripperMotors[2].setPosition(0.02)
    timeMovement(wheels, 0, 0, 500)
    gripperMotors[0].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[0].setPosition(0.0)
    timeMovement(wheels, 0, 0, 500)
    gripperMotors[0].setVelocity(2.0)
    gripperMotors[1].setVelocity(2.0)
    timeMovement(wheels, 0, 0, 1000)
    timeMovement(wheels, 1.25, 1.25, 1000)

def leaveObjective():
    gripperMotors[0].setVelocity(1.5)
    gripperMotors[1].setVelocity(1.5)
    timeMovement(wheels, 1.0, 1.0, 6000)
    timeMovement(wheels, 0.0, 0.0, 500)
    gripperMotors[0].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[0].setPosition(0.05)
    timeMovement(wheels, 0, 0, 500)
    gripperMotors[1].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[2].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[1].setPosition(0.04)
    gripperMotors[2].setPosition(0.04)
    timeMovement(wheels, 0, 0, 500)
    timeMovement(wheels, -1.0, -1.0, 1250)    
    gripperMotors[1].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[2].setVelocity(GRIPPER_MAX_SPEED)
    gripperMotors[1].setPosition(0.02)
    gripperMotors[2].setPosition(0.02)
    timeMovement(wheels, -1.0, 1.0, 4500)

#################################
## AVOID OBSTACLES FUNCTION
def avoidObstacles(sensors, wheels, avoidObstacleCounter):
    left_speed = 2.0
    right_speed = 2.0
    
    if (avoidObstacleCounter > 0):
        if (avoidObstacleCounter == 1):
            ## CHOCA DEL LADO DERECHO
            timeMovement(wheels, 1.0, -1.0, 4165)
        elif (avoidObstacleCounter == 2):
                ## CHOCA DEL LADO IZQUIERDO
            timeMovement(wheels, -1.0, 1.0, 4165)
        else:
            timeMovement(wheels, 1.0, -1.0, 1165)    
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

aO = avoidObstacles(sensors, wheels, avoidObstacleCounter = 0)
while robot.step(TIME_STEP) != -1:
  #  sensorsValues()
    numberObjects = camera.getRecognitionNumberOfObjects()
    objects = camera.getRecognitionObjects()
    
    if (take == False): 
        indice = getRecognition(objective, objects, numberObjects)
        if (indice != -1) and not found:
            found = goToObjective(objects, indice, 60)
        elif ((indice == -1) and not found):
            aO = avoidObstacles(sensors, wheels, aO)
        else:
            takeObjective()
            found = False
            take = True
    else:
        indice = getRecognition(greenZone, objects, numberObjects)
        if (indice != -1) and not found:
            found = goToObjective(objects, indice, 32)
        elif ((indice == -1) and not found):
            aO = avoidObstacles(sensors, wheels, aO)
        else:
            leaveObjective()
            changeWheelsVelocity(wheels, 0, 0)
            break
    pass

# Enter here exit cleanup code.
