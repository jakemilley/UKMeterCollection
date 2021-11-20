
#!/usr/bin/env python2.7
import os
import sys
import json
import subprocess
import time
import csv
import RPi.GPIO as GPIO
import signal
import os.path
from datetime import datetime
global PreviousTime
PreviousTime = 0
global meterList
meterList = []

#GPIO Initialization
global button
global RedLED
global greenLED
button = 21
RedLED = 23
greenLED = 24
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(RedLED,GPIO.OUT)
GPIO.setup(greenLED,GPIO.OUT)

# PS: Let's kill any other instances that may be running
val1 = os.system("killall -KILL rtlamr")    
val2 = os.system("killall -KILL rtl_tcp")    

time.sleep(2)

listenersproc = subprocess.Popen('rtl_tcp')

def signal_handler(sig, frame):
    GPIO.cleanup()
    sys.exit(0)

def button_pressed_callback(channel):
    print("Button pressed!")
    GPIO.output(greenLED,GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(greenLED,GPIO.LOW)
    
def csvLogger(MeterNumber, Value, Type):
    
    current_time = time.time()
    today = datetime.now()
    Timestamp = today.strftime("%Y-%m-%dT%H:%M")
    filename = "/home/pi/Desktop/UKMeterCollection/MeterIDs/"+str(MeterNumber)+".csv"
    try:
        csvfile = open(filename, 'a', newline ='', encoding='utf-8')
        c = csv.writer(csvfile)
        data_to_save = [Timestamp, Value, Type]
        c.writerow(data_to_save)
        csvfile.close()
    except:
        csvfile = open(filename, 'w', newline ='',encoding='utf-8')
        c = csv.writer(csvfile)
        data_to_save = [Timestamp, Value, Type]
        c.writerow(data_to_save)
        csvfile.close()
   

def getCurrentTime():
    current_time = time.time()
    today = datetime.now()
    Timestamp = today.strftime("%Y-%m-%dT%H:%M")
    return Timestamp

def storeData(identity,usage,meterType):
    global PreviousTime
    if (getCurrentTime() == PreviousTime and not identity in meterList):
            GPIO.output(greenLED,GPIO.HIGH)
            print(identity)
            print(usage)
            PreviousTime= getCurrentTime()
            csvLogger(identity, usage, meterType)
            time.sleep(0.1)
            GPIO.output(greenLED,GPIO.LOW)
            meterList.append(identity)
    elif (getCurrentTime() != PreviousTime):
            meterList.clear()
            GPIO.output(greenLED,GPIO.HIGH)
            print(identity)
            print(usage)
            PreviousTime= getCurrentTime()
            csvLogger(identity, usage, meterType)
            time.sleep(0.1)
            GPIO.output(greenLED,GPIO.LOW)
            meterList.append(identity)
    
while True:
    GPIO.output(RedLED,GPIO.HIGH)
    time.sleep(1)
    proc = subprocess.Popen('/home/pi/go/bin/rtlamr -format=json',stdout=subprocess.PIPE, shell=True)
    time.sleep(1)
    number_of_points=0
    for number_of_points in range(5):
        try:
            try:
                line = proc.stdout.readline()
            except:
                print("No data!")
            
            try:
                #print(line)
                data=json.loads(line.decode("utf-8"))
                #print(data)
            except ValueError:
                print("Json error")
                number_of_points+=1
                data = False
            if data:
                meterID = str( int(data['Message']['ID']))
                consumption = str( int(data['Message']['Consumption']))
                metertype = str(data['Message']['Type'])
                storeData(meterID,consumption,metertype)
                  
                
 
        except KeyboardInterrupt:
            print("interrupted!")
            val1 = os.system("killall -KILL rtlamr")    
            val2 = os.system("killall -KILL rtl_tcp")
        
    val1 = os.system("killall -KILL rtlamr")
    time.sleep(1)
    proc = subprocess.Popen('/home/pi/go/bin/rtlamr -msgtype=scm+ -format=json',stdout=subprocess.PIPE, shell=True)
    time.sleep(1)
    number_of_points=0
    for number_of_points in range(5):
        try:
            try:
                line = proc.stdout.readline()
            except:
                print("No data!")
            
            try:
                #print(line)
                data=json.loads(line.decode("utf-8"))
                #print(data)
            except ValueError:
                print("Json error")
                data = False
            if data:
                meterID = str( int(data['Message']['EndpointID']))
                consumption = str( int(data['Message']['Consumption']))
                metertype = str(data['Message']['EndpointType'])
                storeData(meterID,consumption,metertype)
    

        except KeyboardInterrupt:
            
            print("interrupted!")
            GPIO.output(RedLED,GPIO.LOW)
            GPIO.output(greenLED,GPIO.LOW)
            val1 = os.system("killall -KILL rtlamr")    
            val2 = os.system("killall -KILL rtl_tcp")
            
    val1 = os.system("killall -KILL rtlamr")  
    time.sleep(1)
exit(0)
