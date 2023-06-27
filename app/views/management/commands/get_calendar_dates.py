from django.core.management.base import BaseCommand
from views.models import TransitAgency, CalendarDates
from datetime import datetime
import requests
import requests, zipfile, io



class Command(BaseCommand):
    cmta = TransitAgency.objects.get(ntd_id=60048)
    q = requests.get("https://data.texas.gov/download/r4v4-vz24/application%2Fzip")
    gtfs = zipfile.ZipFile(io.BytesIO(q.content))   
    dates = gtfs.open("calendar_dates.txt")
    cmta = TransitAgency.objects.get(ntd_id=60048)
    for x in dates.readlines():
        results = x.decode()
        results = results.split(',')
        if "service_id" not in results[0]:
            print(results)
            print(results[1][0:4])
            print(results[1][4:6])
            print(results[1][6:])
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