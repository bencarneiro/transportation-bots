from django.core.management.base import BaseCommand
from views.models import TransitAgency, CalendarDates, Routes, Trips, Stops, StopTimes, Shapes
from datetime import datetime
import requests
import requests, zipfile, io



class Command(BaseCommand):

    # calendar Dates
    cmta = TransitAgency.objects.get(ntd_id=60048)
    q = requests.get("https://data.texas.gov/download/r4v4-vz24/application%2Fzip")

    gtfs = zipfile.ZipFile(io.BytesIO(q.content))   

    StopTimes.objects.all().delete()

    Trips.objects.all().delete()
    CalendarDates.objects.all().delete()
    Shapes.objects.all().delete()
    # Routes.objects.all().delete()

    Stops.objects.all().delete()

    dates = gtfs.open("calendar_dates.txt")
    for x in dates.readlines():
        results = x.decode()
        results = results.split(',')
        if "service_id" not in results[0]:
            date = datetime(
                year=int(results[1][0:4]),
                month=int(results[1][4:6]),
                day=int(results[1][6:])
            )
            print(date)
            new_date = CalendarDates(
                transit_agency=cmta,
                service_id=results[0],
                date=date,
                exception_type=int(results[2][:-1])
            )
            new_date.save()
            print(f"saved the date data for {results[1]}")

    #routes
   
    routes = gtfs.open("routes.txt")
    for x in routes.readlines():
        results = x.decode()
        results = results.split(',')
        if results[0] != "route_id":
            print(results)
            route = Routes(
                route_id = int(results[0]),
                transit_agency = cmta,
                route_short_name = results[2],
                route_long_name = results[3],
                route_type = int(results[4]),
                route_url = results[5],
                route_color =  results[6],
                route_text_color =  results[7][:-1]
            )
            route.save()
            print(f"Route #{results[0]} written")

    #shapes
    shapes = gtfs.open("shapes.txt")
    for x in shapes.readlines():
        results = x.decode()
        results = results.split(',')
        if results[0] != "shape_id":
            shape = Shapes(
                shape_id = int(results[0]),
                transit_agency = cmta,
                shape_pt_lat = float(results[1]),
                shape_pt_lon = float(results[2]),
                shape_pt_sequence = int(results[3]),
                shape_dist_traveled = float(results[4][0:-1])
            )
            shape.save()
            print(f"Point #{results[3]} of shape #{results[0]} is written")

    
    # stops
    stops = gtfs.open("stops.txt")
    for x in stops.readlines():
        results = x.decode()
        results = results.split(',')
        if results[6]:
            parent_station = results[6]
        else:
            parent_station = None
        if "stop_id" not in results[0]:
            print(results)
            stop = Stops(
                stop_id = int(results[0]),
                transit_agency = cmta,
                at_street = results[1],
                corner_placement = results[2],
                heading = int(results[3]),
                location_type= int(results[4]),
                on_street = results[5],
                parent_station = parent_station,
                stop_code = int(results[7]),
                stop_desc = results[8],
                latitude = float(results[9]),
                longitude = float(results[10]),
                stop_name = results[11],
                stop_position = results[12],
                stop_timezone = results[13],
                stop_url = results[14],
                wheelchair_boarding = int(results[15])
            )
            stop.save()
            print(f"stop #{results[0]} is written")
        
    #trips
    trips = gtfs.open("trips.txt")
    for x in trips.readlines():
        results = x.decode()
        results = results.split(',')
        if "route_id" not in results[0]:
            # print(results)
            route = Routes.objects.get(route_id=int(results[0]))
            trip = Trips(
                trip_id = results[2],
                transit_agency = cmta,
                route = route,
                service_id = results[1],
                trip_headsign  = results[3],
                direction_id = int(results[4]),
                block_id = results[5],
                shape_id = int(results[6]),
                scheduled_trip_id = int(results[7]),
                trip_short_name = results[8],
                wheelchair_accessible = int(results[9]),
                bikes_allowed = int(results[10][:-1])
            )
            # print(int(results[10][:-1]))
            trip.save()
            print(f"trips #{results[2]} written")

    #stoptimes
    stoptimes = gtfs.open("stop_times.txt")
    for x in stoptimes.readlines():
        results = x.decode()
        results = results.split(',')

        if "trip_id" not in results[0]:
            trip = Trips.objects.get(trip_id=results[0])
            try:
                stop = Stops.objects.get(stop_id=int(results[3]))
            except: 
                print(f" stop_id #{results[3]} not found- stop time not written")
                continue
            if int(results[1][0:2]) > 23:
                arrival_time = datetime(
                    day=2,
                    month=1,
                    year=1970,
                    hour=(int(results[1][0:2]) - 24),
                    minute=int(results[1][3:5]),
                    second=int(results[1][6:8]) 
                )
            else:
                arrival_time = datetime(
                    day=1,
                    month=1,
                    year=1970,
                    hour=int(results[1][0:2]),
                    minute=int(results[1][3:5]),
                    second=int(results[1][6:8])
                )
            if int(results[2][0:2]) > 23:
                departure_time = datetime(
                    day=2,
                    month=1,
                    year=1970,
                    hour=(int(results[2][0:2]) - 24),
                    minute=int(results[2][3:5]),
                    second=int(results[2][6:8])
                )               
            else:
                departure_time = datetime(
                    day=1,
                    month=1,
                    year=1970,
                    hour=int(results[2][0:2]),
                    minute=int(results[2][3:5]),
                    second=int(results[2][6:8])
                )
            print(results)
            stoptime = StopTimes(
                transit_agency = cmta,
                trip = trip,
                stop = stop,
                arrival_time = arrival_time,
                departure_time = departure_time,
                stop_sequence = int(results[4]),
                pickup_type = int(results[5]),
                drop_off_type = int(results[6]),
                shape_dist_traveled = float(results[7]),
                timepoint = int(results[8][:-1])
            )
            stoptime.save()
            print(f"trip #{results[0]}, stop sequence #{results[4]} is written")
