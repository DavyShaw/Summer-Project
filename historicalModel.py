import pandas as pd
import numpy as np
import random as rnd

import matplotlib.pyplot as plt
from datetime import date
from _datetime import datetime

df = pd.read_csv('bus41Week3.csv')   #('busTest41Rev2.csv')
df['TIMESTAMP'] = pd.to_datetime(df.TIMESTAMP)
print(df.info())

df_out = pd.read_csv('Outbound41.csv')
df_in = pd.read_csv('Inbound41.csv')


#User Input
travel_day = str(input("Enter the day you want to leave: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday"))
direction = int(input("Enter bus direction (From Town = 0, To Town = 1): "))

#Obtain travel times, travel direction, corresponding Vehicle Journey ID & Bus stop numbers
if direction == 0:
    print('Direction is from town')
    travel_time = input("Enter a bus time (08:30, 08:55, 09:20, 9:40, 10:00, 10:30, 11:00, 11:20, 11:25, 11:50, 12:10, 12:30, 12:50, 12:55, 13:05, 13:10, 13:30, 13:50, 14:50, 14:55): ")
    bus = (df_out[(df_out.Time == travel_time)])
    route = bus.VJID
    start_stop_ID = '288'   #O'Connell Street
    end_stop_ID = '3679'    #Swords Main Street
elif direction == 1:
    print('Direction is to town')
    travel_time = input("Enter a bus time (08:20, 08:30, 08:45, 09:10, 09:30, 10:15, 10:45, 11:05, 11:30, 11:55, 12:15, 12:35, 13:05, 13:25, 13:40, 13:45, 14:05, 14:25, 14:45): ")
    bus = (df_in[(df_in.Time == travel_time)])
    route = bus.VJID
    start_stop_ID = '3689'  #Swords Main Street
    end_stop_ID = '277'     #Irish Life Mall


#Obtain dataframe rows containing the starting point and end point
start_point = (df[(df.VJID == int(route)) 
                  & (df.StopID == start_stop_ID)
                  & (df.TIMESTAMP.dt.weekday_name == travel_day)
                  #& (df.Week == 1)
                  & (df.AtStop == 1)])
                    
go = start_point.tail(1)

end_point = (df[(df.VJID == int(route))
                & (df.StopID == end_stop_ID)
                & (df.TIMESTAMP.dt.weekday_name == travel_day)
                #& (df.Week == 1)
                & (df.AtStop == 1)])
end = end_point.head(1)
print()
scheduled_go_time = pd.to_datetime(travel_time)
print('The scheduled departure time was: ',scheduled_go_time)
go_time = go.TIMESTAMP #Starting time
#go_time = go.Time
print('The actual departure time was: ', go_time)
end_time = end.TIMESTAMP #Finishing time
#end_time = end.Time
print('The arrival time was: ', end_time)
strend_time = str(end_time)

#Calculate time between start and end of journey
ep_go = int(go_time.view('int64')) 
#print ('epoch start: ', ep_go)
ep_end = int(end_time.view('int64'))
#print ('epoch end: ', ep_end)
diff = ((ep_end-ep_go)/1000000000)
print()
print ('The travel time was: ', diff, 'seconds or', diff/60, 'minutes')


#ep_go_hour = go_time.dt.hour
#ep_go_minute = go_time.dt.minute
#ep_go_second = go_time.dt.second
#print("Go Hour", ep_go_hour)
#print("Go Minute", ep_go_minute)
#print("Go Minute", ep_go_second)
#ep_end_hour = end_time.dt.hour
#ep_end_minute = end_time.dt.minute
#ep_end_second = end_time.dt.second
#print("End Hour", ep_end_hour)
#print("End Minute", ep_end_minute)
#print("End Minute", ep_end_second)