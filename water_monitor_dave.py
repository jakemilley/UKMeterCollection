#!/usr/bin/env python2.7
import os
import sys
import json
import subprocess
import time
from pyModbusTCP.client import ModbusClient
c = ModbusClient(host="192.168.2.124", port=502)
c.write_single_register(10,1)

# PS: Let's kill any other instances that may be running
val1 = os.system("killall -KILL rtlamr")    
val2 = os.system("killall -KILL rtl_tcp")    

time.sleep(2)

listenersproc = subprocess.Popen('rtl_tcp')


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
    

        except KeyboardInterrupt:
            print("interrupted!")
            val1 = os.system("killall -KILL rtlamr")    
            val2 = os.system("killall -KILL rtl_tcp")
            
    val1 = os.system("killall -KILL rtlamr")  
    time.sleep(1)
exit(0)
