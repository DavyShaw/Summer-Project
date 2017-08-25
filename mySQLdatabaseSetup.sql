create table cleangps(LineID int(3), stopID int(4), time int(2), 
day int(2),temp float(3,3),hum float(2,2),pres float(4,1), diff int(4));

create table stops(stopid int(4), shortname varchar(60), latitude long, longitude long, route varchar(8), direction int(1));

create table routes(route_id varchar(5), route_name varchar(60), routename_and_id varchar(60));

load data local infile 'cleangps.csv'
into table cleangps
fields terminated by ','
lines terminated by '\n'
;

load data local infile 'stops.csv'
into table stops
fields terminated by ','
lines terminated by '\n'
;

load data local infile 'routes.csv'
into table routes
fields terminated by ','
lines terminated by '\n'
;