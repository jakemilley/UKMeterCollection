#!/usr/bin/env python2.7
import os
import sys
import json
import subprocess
import time
import csv
from pyModbusTCP.client import ModbusClient
from datetime import datetime
global Measurement
Measurement = 'm3'

c = ModbusClient(host="192.168.2.124", port=502)
c.write_single_register(10,1)

# PS: Let's kill any other instances that may be running
val1 = os.system("killall -KILL rtlamr")    
val2 = os.system("killall -KILL rtl_tcp")    

time.sleep(2)

listenersproc = subprocess.Popen('rtl_tcp')

def csvLogger(MeterNumber, Value):
    
    current_time = time.time()
    today = datetime.now()
    Timestamp = today.strftime("%Y-%m-%dT%H:%M:%S")
    minutes = str(int(current_time/60))
    seconds = str(int(current_time % 60))
    milliseconds = str(int(((current_time-int(current_time))*1000)))
    csvfile = open('MeterConsumption.csv', 'a', newline ='', encoding='utf-8')
    c = csv.writer(csvfile)
    data_to_save = [MeterNumber, Measurement, Timestamp, Value]
    c.writerow(data_to_save)
    csvfile.close()


# def listToString(s):
#     str1 = ""
#     for ele in s:
#         str1 += ele
#     return str1
    
while True:
    time.sleep(1)
    proc = subprocess.Popen('~/go/bin/rtlamr -format=json',stdout=subprocess.PIPE, shell=True)
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
                print(meterID)
                print(consumption)
                number_of_points+=1
                csvLogger(meterID, consumption)

        except KeyboardInterrupt:
            print("interrupted!")
            val1 = os.system("killall -KILL rtlamr")    
            val2 = os.system("killall -KILL rtl_tcp")
        
    val1 = os.system("killall -KILL rtlamr")
    time.sleep(1)
    proc = subprocess.Popen('~/go/bin/rtlamr -msgtype=scm+ -format=json',stdout=subprocess.PIPE, shell=True)
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
                print(meterID)
                print(consumption)
                csvLogger(meterID, consumption)
    

        except KeyboardInterrupt:
            print("interrupted!")
            val1 = os.system("killall -KILL rtlamr")    
            val2 = os.system("killall -KILL rtl_tcp")
            
    val1 = os.system("killall -KILL rtlamr")  
    time.sleep(1)
exit(0)
