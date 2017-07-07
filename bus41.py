import pandas as pd
import numpy as np
import random as rnd

import matplotlib.pyplot as plt
from datetime import date
from _datetime import datetime

av_peak_delay_out = 0
peak_count_out = 0
av_peak_delay_in = 0
peak_count_in = 0

df = pd.read_csv('busTest41Rev1.csv')
df['TIMESTAMP'] = pd.to_datetime(df.TIMESTAMP)

df_out = pd.read_csv('Outbound41.csv')
df_in = pd.read_csv('Inbound41.csv')

#bus_no = int(input("Enter a bus number (41 or 41): "))
#if bus_no != 41:
#    bus_no = int(input("Enter a bus number (41 or 41): "))
#print('Bus no.:', bus_no)

#User Input
direction = int(input("Enter bus direction (From Town = 0, To Town = 1): "))
if direction == 0:
    print('Direction is from town')
    myTime = input("Enter a bus time (08:30, 08:55, 09:20): ")
    bus = (df_out[(df_out.Time == myTime)])
    route = bus.VJID
    start_stop_ID = '288'
    end_stop_ID = '4957'
elif direction == 1:
    print('Direction is to town')
    myTime = input("Enter a bus time (08:20, 08:30, 08:45): ")
    bus = (df_in[(df_in.Time == myTime)])
    route = bus.VJID
    start_stop_ID = '4957'
    end_stop_ID = '288'

print()
print('The bus route Vehicle Journey ID is: ', route)
print()
print('start bus stop ID: ', start_stop_ID, ' , ', 'end bus stop ID', end_stop_ID)
print()

start_point = (df[(df.VJID == int(route)) 
                  & (df.StopID == start_stop_ID) 
                  & (df.AtStop == 1)])
go = start_point.tail(1)

end_point = (df[(df.VJID == int(route)) 
                & (df.StopID == end_stop_ID) 
                & (df.AtStop == 1)])
end = end_point.head(1)

delay = int(end.Delay)
if delay > 0:
    print('Delay was: ', delay, ' seconds', '(', delay/60, 'minutes)')
elif delay<0:
    print('Bus was ahead of schedule by: ', delay, ' seconds ', '(', delay/60, ' minutes)')
else:
    print('There was no delay, bus was on time! ')

print()
go_time = go.TIMESTAMP
print('The departure time was: ', go_time)
print()
scheduled_go_time = pd.to_datetime(myTime)
print('The scheduled departure time was: ',scheduled_go_time)
print()
end_time = end.TIMESTAMP
print('The arrival time was: ', end_time)
print()

#Need to update number of days recorded & store in database
if direction == 0:
    av_peak_delay_out += delay
    peak_count_out +=1
    print("The average delay outbound is: ", av_peak_delay_out/peak_count_out)
elif direction == 1:
    av_peak_delay_in += delay
    peak_count_in +=1
    print("The average delay inbound is: ", av_peak_delay_in/peak_count_in)