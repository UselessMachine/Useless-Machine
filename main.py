import arm
import motors
from time import sleep
import time
import math
import RPi.GPIO as GPIO
import threading

#Joystick Pins
pinUp = 31
pinRight = 29
pinDown = 35
pinLeft = 33

#Setup switches
pinSwitch = 23
pinEndSwitch = 37

#Pins numbered by physical position
GPIO.setmode(GPIO.BOARD)
#Setup joystick inputs
GPIO.setup(pinRight, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinLeft, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinUp, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinDown, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Setup switched
GPIO.setup(pinEndSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(pinSwitch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
           
#Setup servos
futabaR = motors.Servo(19, 178, 160, 0) #DONE
spektrum = motors.Servo(40, 159, 115, 1) #DONE
hitec = motors.Servo(0, 180, 180, 2) #DONE
reely = motors.Servo(0, 180, 180, 3) #DONE
futabaS = motors.Servo(18, 178, 160, 4) #DONE

#Setup stepper
stepper = motors.Stepper(32,36,38,40)

#Setup robot arm
robotArm = arm.robotArm([futabaR, spektrum, hitec, reely])
#Setup switch arm
switchArm = arm.switchArm(futabaS, stepper)

lStepTime = time.time()

while (GPIO.input(pinEndSwitch) != GPIO.HIGH):
    if (time.time() > lStepTime + 0.002):
        stepper.step(False)
        lStepTime = time.time()
    

try:
    while (True):
        #Joystick input handling
        if GPIO.input(pinRight) == GPIO.HIGH:
            if switchArm.getAngle() < 180:
                switchArm.moveA(True, 1)
        elif GPIO.input(pinLeft) == GPIO.HIGH:
            if switchArm.getAngle() > 0:
                switchArm.moveA(False, 1)
        if GPIO.input(pinUp) == GPIO.HIGH:
            if switchArm.getRadius() > 60:
                if (time.time() > lStepTime + 0.002):
                    switchArm.moveL(False)
                    lStepTime = time.time()
        elif GPIO.input(pinDown) == GPIO.HIGH:
            if switchArm.getRadius() < 180:
                if (time.time() > lStepTime + 0.002):
                    switchArm.moveL(True)
                    lStepTime = time.time()
        robotArm.goto(switchArm.getX(), switchArm.getY())
                    
            
except KeyboardInterrupt:
    GPIO.cleanup()
    stepper.free()
