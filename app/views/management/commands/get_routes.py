from django.core.management.base import BaseCommand
from views.models import TransitAgency, Routes
import requests
import requests, zipfile, io



class Command(BaseCommand):
    q = requests.get("https://data.texas.gov/download/r4v4-vz24/application%2Fzip")
    gtfs = zipfile.ZipFile(io.BytesIO(q.content))
    cmta = TransitAgency.objects.get(ntd_id=60048)
    shapes = gtfs.open("routes.txt")
    for x in shapes.readlines():
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