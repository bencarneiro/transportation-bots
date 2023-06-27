from django.core.management.base import BaseCommand
from views.models import TransitAgency, Routes, Trips
import requests
import requests, zipfile, io



class Command(BaseCommand):
    q = requests.get("https://data.texas.gov/download/r4v4-vz24/application%2Fzip")
    gtfs = zipfile.ZipFile(io.BytesIO(q.content))
    cmta = TransitAgency.objects.get(ntd_id=60048)
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