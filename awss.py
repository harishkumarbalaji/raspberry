import boto3
from datetime import datetime
from time import sleep
import nexmo
import RPi.GPIO as GPIO

client = nexmo.Client(key='1eccfa21', secret='7E4gjWD88PgTqcl1')

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
gas=3
GPIO.setup(gas, GPIO.IN,pull_up_down=GPIO.PUD_UP)

client=boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('iotcar')

columns=["Time","Date","Status"]
count=""

while True:
    now = datetime.now()
    today = now.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    if GPIO.input(gas):
        count="Normal"
    else:
        count="Alert!"
        print("Alert!!")
        client.send_message({
            'from': '91',
            'to': '919677219665',
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
    sleep(1)
