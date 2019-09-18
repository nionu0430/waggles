import RPi.GPIO as GPIO
import time
from ina219 import INA219, DeviceRangeError
from time import sleep

#--------ina219 initial setup--------------
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)

#--------relay initial setup--------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)



def read_ina219():
    try:
        print('Bus Voltage: {0:0.4f}V'.format(ina.voltage()))
        print('Bus Current: {0:0.2f}mA'.format(ina.current()))
        print('Power: {0:0.2f}mW'.format(ina.power()))
        print('Shunt Voltage: {0:0.2f}mV\n'.format(ina.shunt_voltage()))
    except DeviceRangeError as e:
        print(e)

def control_relay():

while 1:
    read_ina219()
    sleep(1)