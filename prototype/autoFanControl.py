import RPi.GPIO as GPIO
import Adafruit_DHT
import time

#----------GPIO SETTINGS------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()

#-----------PIN SETTINGS------------
batteryPIN = 18
fanPIN = 12
heatingPIN = 21
pinList = [batteryPIN, fanPIN, heatingPIN]
for i in pinList:
    GPIO.setup(i, GPIO.OUT)


def getSensorData():
    H, T = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302,'4')
    print("Humidity: ", H, "  Temperature: ", T)
    return int(H), int(T)

def setPinByHumid(humid):
    if(humid > 80):
        GPIO.output(fanPIN, GPIO.LOW)   #fan on
    else:
        GPIO.output(fanPIN, GPIO.HIGH)   #fan off

while 1:
    H, T = getSensorData()
    setPinByHumid(H)
    
GPIO.cleanup()
