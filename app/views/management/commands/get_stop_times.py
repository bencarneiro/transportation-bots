from django.core.management.base import BaseCommand
from views.models import TransitAgency, StopTimes, Trips, Stops
import requests
import requests, zipfile, io
from datetime import datetime



class Command(BaseCommand):
    cmta = TransitAgency.objects.get(ntd_id=60048)
    q = requests.get("https://data.texas.gov/download/r4v4-vz24/application%2Fzip")
    gtfs = zipfile.ZipFile(io.BytesIO(q.content))   
    cmta = TransitAgency.objects.get(ntd_id=60048)
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


# trip_id,arrival_time,departure_time,stop_id,stop_sequence,pickup_type,drop_off_type,shape_dist_traveled,timepoint
# 2710222_0001,04:41:00,04:41:00,554,1,0,0,0.0000,1