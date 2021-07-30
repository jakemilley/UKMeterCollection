#!/usr/bin/env python2.7
import os
import sys
import json
import subprocess
import time

# PS: Let's kill any other instances that may be running
val1 = os.system("killall -KILL rtlamr")    
val2 = os.system("killall -KILL rtl_tcp")    

time.sleep(2)

listenersproc = subprocess.Popen('rtl_tcp')

# Delay. Totally a hack, but we need to wait for the listener to start.
time.sleep(2)

proc = subprocess.Popen('~/go/bin/rtlamr', shell=True)


try:
  while True:
    line = proc.stdout.readline()
    if not line:
        break
    
    try:
        data=json.loads(line.decode("utf-8"))
    except ValueError:
        print("Error")
    else:
        reading = str( int(data['Message']['Consumption']) / 100)
        leakflag = data['Message']['Leak']
        leaknowflag = data['Message']['LeakNow']		
        backflowflag = data['Message']['BackFlow']
        nouseflag = data['Message']['NoUse']

        output = "Carmack water reading detected! Consumption is [{}], Leak [{}], LeakNow [{}], BlackFlow [{}], NoUse [{}]".format(reading, leakflag, leaknowflag, backflowflag, nouseflag)
        print(output)
		
		#PS: Break out of our loop once we've reading our values (comment out below 3 lines to keep it repeating indefinitely)
        os.system("taskkill /f /im ~/go/bin/rtlamr")
        os.system("taskkill /f /im rtl_tcp")
        break

except KeyboardInterrupt:
  print("interrupted!")
  os.system("taskkill /f /im ~/go/bin/rtlamr")
  os.system("taskkill /f /im rtl_tcp")
  
  
exit(0)