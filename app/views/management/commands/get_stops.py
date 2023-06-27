from django.core.management.base import BaseCommand
from views.models import TransitAgency, Stops
import requests
import requests, zipfile, io



class Command(BaseCommand):
    cmta = TransitAgency.objects.get(ntd_id=60048)
    q = requests.get("https://data.texas.gov/download/r4v4-vz24/application%2Fzip")
    gtfs = zipfile.ZipFile(io.BytesIO(q.content))   
    cmta = TransitAgency.objects.get(ntd_id=60048)
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


# stop_id,at_street,corner_placement,heading,location_type,on_street,parent_station,stop_code,stop_desc,stop_lat,stop_lon,stop_name,stop_position,stop_timezone,stop_url,wheelchair_boarding,zone_id
# 1002,Burton,SW,144,0,Riverside,,1002,002021 Riverside & Burton,30.240341,-97.727308,Riverside/Burton,N,,https://www.capmetro.org/stopdetail/index.php?stop=1002,0,