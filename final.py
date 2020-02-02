import RPi.GPIO as GPIO
import time
import boto3
from datetime import datetime
import nexmo

client=boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('iotcar')

columns=["Time","Date","Status"]
count=""

client = nexmo.Client(key='1eccfa21', secret='7E4gjWD88PgTqcl1')

l1=31
r1=11
l2=32
r2=12

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


gas=3
GPIO.setup(gas, GPIO.IN,pull_up_down=GPIO.PUD_UP)
 
GPIO.setup(l1,GPIO.OUT)
GPIO.setup(r1,GPIO.OUT)
GPIO.setup(l2,GPIO.OUT)
GPIO.setup(r2,GPIO.OUT)

lf=GPIO.PWM(l1,100)
rf=GPIO.PWM(r1,100)


#set GPIO Pins
GPIO_TRIGGER = 35
GPIO_ECHO = 36

GPIO_TRIGGER2 = 37
GPIO_ECHO2 = 38
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

GPIO.setup(GPIO_TRIGGER2, GPIO.OUT)
GPIO.setup(GPIO_ECHO2, GPIO.IN)

 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
def distance2():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER2, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER2, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO2) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO2) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance2 = (TimeElapsed * 34300) / 2
 
    return distance2

def backward():
    GPIO.output(l2,True)
    GPIO.output(r2,True)
def niruthu():	
    lf.stop()
    rf.stop()
    GPIO.output(l2,False)
    GPIO.output(r2,False)

def forward(x):
    lf.start(0)
    lf.ChangeDutyCycle(x)
    rf.start(0)
    rf.ChangeDutyCycle(x)
    GPIO.output(l2,False)
    GPIO.output(r2,False)

c=1

if __name__ == '__main__':
    try:
        while True:
            nil=100
            dist1 = distance()
            dist2 = distance2()
            print ("front = %.1f cm " % dist1)
            print ("back = %.1f cm " % dist2)
            if(c==1):
                if (dist1<5 or dist2<5):
                    while (nil>=20):
                        forward(nil)
                        nil=nil-1
                        time.sleep(0.01)
                    niruthu()
                    time.sleep(5)
                    c=2
                else:
                    forward(100)
            else:
                if (dist1<5 or dist2<5):
                    niruthu()
                    time.sleep(5)
                    c=1
                else:
                    backward()
            print(c)  
            now = datetime.now()
            today = now.strftime("%d/%m/%Y")
            current_time = now.strftime("%H:%M:%S")
            if GPIO.input(gas):
                count="Normal"
                print("normal")
            else:
                count="Alert!"
                print("Alert!!")
                client.send_message({
                    'from': 'CAR',
                    'to': '919500136398',
                    'text': 'Alert!! Your Car is in danger!.',
                })
            response = table.put_item(
                Item={
                    columns[0]: current_time,
                    columns[1]: today,
                    columns[2]: count
                        }
                    )
            print(response["ResponseMetadata"]["HTTPStatusCode"])

        
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

