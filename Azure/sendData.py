import RPi.GPIO as GPIO
import datetime
import csv
import time
import sys
import Adafruit_DHT
from ina219 import INA219, DeviceRangeError
from time import sleep
from datetime import datetime
from azure.iot.device import IoTHubDeviceClient, Message

#----az iot string---
CONNECTION_STRING = "HostName=wagglesTest.azure-devices.net;DeviceId=raspberrypiTes    t;SharedAccessKey=b3Mglcv0uIYfu2bQmKlp6ENq1iJsAdz/qEXBmhC8KnM="
MSG_TXT = '{{"temperature": {temperature},"humidity": {humidity}}}'


#----------GPIO SETTINGS------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
#-----------HEATING PIN SETTINGS------------
heatPIN = 14
GPIO.setup(heatPIN, GPIO.OUT)
#-----------FAN PIN SETTINGS------------
fanPIN = 15
GPIO.setup(fanPIN, GPIO.OUT)
#-----------MINI FAN PIN SETTINGS------------
minifanPIN = 18
GPIO.setup(minifanPIN, GPIO.OUT)

#----------INA SETTING------------
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 2.0
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
ina.configure(ina.RANGE_16V)
#-----------Global Var-------------------------
fanStatus = 0
heatStatus = 0
time_interval = 600
now = datetime.now()
fname = "result"+ str(now.month) + str(now.day) + ".csv"

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print ( "IoT Hub device sending periodic messages, press Ctrl-C to exit" )
        while True:
            msg_txt_formatted = MSG_TXT.format("2","2")
            message = Message(msg_txt_formatted)
    except KeyboardInterrupt:
        print("#######IoTHub Client stopped!!#######")

def main():
    iothub_client_telemetry_sample_run()
    timeDelta = 0
    f = open(fname,"w",newline="")
    csv_writer = csv.writer(f)
    csv_writer.writerow(['Time','Humidity','Temperature','Voltage','Current','Power','fan','heat'])
    f.close()
    while True:
        H, T = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302,'4')
        bus_voltage = ina.voltage()
        bus_power = ina.power()
        bus_current = ina.current()
        now = datetime.now()
        currentTime = str(now.month) +"/" + str(now.day) +" " + str(now.hour) + ":" + str(now.minute)

                #check the condition
        if(T < 15):
            GPIO.output(fanPIN, GPIO.HIGH)
            GPIO.output(heatPIN, GPIO.LOW)
            GPIO.output(minifanPIN, GPIO.LOW)
            fanStatus = 0
            heatStatus = 1
#print("T < 15")
        elif(T > 35):
            GPIO.output(fanPIN, GPIO.LOW)
            GPIO.output(heatPIN, GPIO.HIGH)
            GPIO.output(minifanPIN, GPIO.LOW)
            fanStatus = 1
            heatStatus = 0
#           print("T > 35")

        else:
            if(H < 60):
                GPIO.output(fanPIN, GPIO.HIGH)
                GPIO.output(heatPIN, GPIO.HIGH)
                GPIO.output(minifanPIN, GPIO.HIGH)
                fanStatus = 0
                heatStatus = 0
#               print("15 < T < 35, H < 60")
            else:
                GPIO.output(fanPIN, GPIO.LOW)
                GPIO.output(heatPIN, GPIO.HIGH)
                GPIO.output(minifanPIN, GPIO.LOW)
                fanStatus = 1
                heatStatus = 0
#               print("15 < T < 35, H > 60")
#write on CSV
        f = open(fname,"a", newline="")
        csv_writer = csv.writer(f)
        timeDelta = timeDelta + time_interval/60
        csv_writer.writerow([round(timeDelta,2), round(H,2), round(T,2), round(bus_voltage,2), round(bus_current,2), round(bus_power,2), fanStatus, heatStatus])
        f.close()
        time.sleep(time_interval)


if __name__ == "__main__":
    print ( "IoT Hub Quickstart #1 - Simulated device" )
    print ( "Press Ctrl-C to exit" )
    main()