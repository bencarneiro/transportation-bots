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
    rs = Routes.objects.all()
    for r in rs:
        try:
            r.delete()
        except:
            print("no")
    StopTimes.objects.all().delete()

    Trips.objects.all().delete()

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
