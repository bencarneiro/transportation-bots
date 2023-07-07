


select * from stop_times where trip_id in
(select id from trips where service_id in 
(select service_id from calendar_dates where date = 20230627)
and route_id = 137)
and departure_time > "1970-01-01 18:54:00"
and stop_id in (select id from stops where stop_id in (4152, 1260));

select time(now());


select * from trips where id in (32143,32200);


SELECT * FROM stops
order by SQRT(POWER(ABS(longitude - (-97.72022063254802)), 2) + POWER(ABS(latitude - (30.314065874794284)), 2)) ASC
LIMIT 10;

select * from stop_times 
left join trips on trips.id = stop_times.trip_id
left join routes on trips.route_id = routes.id
where stop_times.trip_id in
(select id from trips where service_id in 
(select service_id from calendar_dates where date = 20230629))
and departure_time > "1970-01-01 09:40:00"
and departure_time < "1970-01-01 10:50:00"
and stop_times.stop_id in (
SELECT id FROM stops
where SQRT(POWER(ABS(longitude - (-97.72022063254802)), 2) + POWER(ABS(latitude - (30.314065874794284)), 2)) < .005
order by SQRT(POWER(ABS(longitude - (-97.72022063254802)), 2) + POWER(ABS(latitude - (30.314065874794284)), 2)) ASC);


select time(stop_times.departure_time) as departs,
trip_headsign,
stops.stop_id,
trips.shape_id,
trips.trip_id
from stop_times
left join trips on trips.id = stop_times.trip_id
left join routes on trips.route_id = routes.id
LEFT JOIN stops on stop_times.stop_id = stops.id
where stop_times.trip_id in
(select id from trips where service_id in 
(select service_id from calendar_dates where date = 20230629))
and departure_time > "1970-01-01 09:40:00"
and departure_time < "1970-01-01 10:50:00"
and stop_times.stop_id in (
SELECT id FROM stops
where SQRT(POWER(ABS(longitude - (-97.72022063254802)), 2) + POWER(ABS(latitude - (30.314065874794284)), 2)) < .005
order by SQRT(POWER(ABS(longitude - (-97.72022063254802)), 2) + POWER(ABS(latitude - (30.314065874794284)), 2)) ASC)
order by stop_times.departure_time;
