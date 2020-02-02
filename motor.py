l1=31
r1=11
l2=32
r2=12
import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(l1,GPIO.OUT)
GPIO.setup(r1,GPIO.OUT)
GPIO.setup(l2,GPIO.OUT)
GPIO.setup(r2,GPIO.OUT)

lf=GPIO.PWM(l1,100)
rf=GPIO.PWM(r1,100)

def backward():
    GPIO.output(l2,True)
    GPIO.output(r2,True)
def stop():	
    lf.stop()
    rf.stop()
    GPIO.output(l2,False)
    GPIO.output(r2,False)

def forward():
    lf.start(0)
    lf.ChangeDutyCycle(50)
    rf.start(0)
    rf.ChangeDutyCycle(50)
    GPIO.output(l2,False)
    GPIO.output(r2,False)
	
	
while True:
    forward()
    sleep(2)
    stop()
    sleep(1)
    backward()
    sleep(2)
    stop()
    break	
