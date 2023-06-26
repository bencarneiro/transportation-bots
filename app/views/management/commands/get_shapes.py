from django.core.management.base import BaseCommand
from views.models import TransitAgency, Shapes
import requests
import requests, zipfile, io



class Command(BaseCommand):
    cmta = TransitAgency.objects.get(ntd_id=60048)
    q = requests.get("https://data.texas.gov/download/r4v4-vz24/application%2Fzip")
    gtfs = zipfile.ZipFile(io.BytesIO(q.content))   
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