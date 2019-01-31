import os
import RPi.GPIO as GPIO

DEBUG = False

class Servo:
    
    def __init__(self, min, max, range, id):
        self.min = min
        self.max = max
        self.range = range
        self.id = id
        
    def setAngle(self, angle):
        cmd = "echo " + str(self.id) + "=" + str((angle/180*(self.max-self.min)+self.min)*180/self.range-(180-self.range)/2+60) + "> /dev/servoblaster" #str(((angle/self.range*(self.max-self.min)+self.min)*180/self.range+60))
        os.system(cmd)
        if(DEBUG):
            print(str(self.id) + ": " + str(angle) + " degrees")
            
            
class Stepper:
    
    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        
        GPIO.setup(a, GPIO.OUT)
        GPIO.setup(b, GPIO.OUT)
        GPIO.setup(c, GPIO.OUT)
        GPIO.setup(d, GPIO.OUT)
        
        self.curStep = 0
        
    def step(self, dir):
        if dir:
            self.curStep -= 1
        else:
            self.curStep += 1
        
        if (self.curStep > 3):
            self.curStep = 0
        if (self.curStep < 0):
            self.curStep = 3
            
        if (self.curStep == 0):
            GPIO.output(self.a, GPIO.HIGH)
            GPIO.output(self.b, GPIO.LOW)
            GPIO.output(self.c, GPIO.HIGH)
            GPIO.output(self.d, GPIO.LOW)
        elif (self.curStep == 1):
            GPIO.output(self.a, GPIO.HIGH)
            GPIO.output(self.b, GPIO.LOW)
            GPIO.output(self.c, GPIO.LOW)
            GPIO.output(self.d, GPIO.HIGH)
        elif (self.curStep == 2):
            GPIO.output(self.a, GPIO.LOW)
            GPIO.output(self.b, GPIO.HIGH)
            GPIO.output(self.c, GPIO.LOW)
            GPIO.output(self.d, GPIO.HIGH)
        elif (self.curStep == 3):
            GPIO.output(self.a, GPIO.LOW)
            GPIO.output(self.b, GPIO.HIGH)
            GPIO.output(self.c, GPIO.HIGH)
            GPIO.output(self.d, GPIO.LOW)
    
    def free(self):
            GPIO.output(self.a, GPIO.LOW)
            GPIO.output(self.b, GPIO.LOW)
            GPIO.output(self.c, GPIO.LOW)
            GPIO.output(self.d, GPIO.LOW)