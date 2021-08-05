import time
import csv
global Measurement
from datetime import datetime
Measurement = 'm3'

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

while(1):
    csvLogger(10000, 10000)
    time.sleep(1)