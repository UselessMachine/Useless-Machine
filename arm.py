import math
import motors
import time

class robotArm:
    angle = 0
    radius = 0
    offsetY = 60
    offsetZ = -8
    a = 121
    b = 91
    c = 45
    omega = 0
    
    def __init__(self, motors):
        self.motors = motors
            
    def goto(self, x, y):
        startTime = time.time()
        self.radius = math.hypot(x, y+self.offsetY)
        self.angle = math.acos(x/self.radius)*180/math.pi#-math.atan((y+self.offsetY)/x)*180/math.pi
        self.setOmega((-90)/(1+math.pow(2,(self.radius-130)/10)))
        
        #print("Radius: ", self.radius, "Angle: ", self.angle);
        self.setMotors()
        time1 = time.time() - startTime
        #print(time1)
        
    def angleRadius(self, angle, radius):
        self.radius = radius
        self.angle = angle
        self.setMotors()
    
    def setOmega(self, omega):
        self.omega = omega
    
    def getX(self):
        x = math.cos(self.angle*math.pi/180)*self.radius
        return x
    
    def getY(self):
        y = math.sin(self.angle*math.pi/180)*self.radius - offsetY
        return y
    
    def setMotors(self):
        startTime = time.time()
        
        h = self.offsetZ - math.sin(self.omega/180*math.pi)*self.c
        r = self.radius - math.cos(self.omega/180*math.pi)*self.c
        time1 = time.time() - startTime
        #print(time1)
        
        beta = 180/math.pi * math.acos((math.pow(r, 2)+math.pow(h, 2)-math.pow(self.a, 2)-math.pow(self.b, 2))/(-2*self.a*self.b))
        alpha = 180/math.pi *(math.acos(h/math.hypot(h, r)) + math.acos(math.sin(beta/180*math.pi)*self.b/math.hypot(h, r)))
        time2 = time.time() - startTime
        
        self.motors[0].setAngle(self.angle)
        self.motors[1].setAngle(90-(alpha-90))
        self.motors[2].setAngle(180-beta)
        self.motors[3].setAngle(90+(180-(180-alpha)-beta)+self.omega)
        time3 = time.time() - startTime
        
        #print("Time 1:", time1, " Time 2:", time2, " Time 3: ", time3)
        
class switchArm:
    radius = 59
    angle = 90
    
    stepperDistance = 102/500
    
    def __init__(self, servo, stepper):
        self.servo = servo
        self.stepper = stepper
        
    def moveL(self, dir):
        if dir:
            self.radius += self.stepperDistance
        else:
            self.radius -= self.stepperDistance
        
        self.stepper.step(dir)
        
    def moveA(self, dir, a):
        if dir:
            self.angle += a
        else:
            self.angle -= a
        self.servo.setAngle(self.angle)
                
    def getX(self):
        x = math.cos(self.angle*math.pi/180)*self.radius
        return x
 
    def getY(self):
        y = math.sin(self.angle*math.pi/180)*self.radius
        return y
    
    def getRadius(self):
        return self.radius
    
    def getAngle(self):
        return self.angle