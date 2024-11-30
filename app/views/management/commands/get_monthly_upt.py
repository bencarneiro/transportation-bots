from django.core.management.base import BaseCommand
from views.models import MonthlyUnlinkedPassengerTrips, TransitAgency
import pandas as pd
import datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        MonthlyUnlinkedPassengerTrips.objects.all().delete()
        dates = []
        for year in range(2002,2025):
        #     print(z)
            for month in range(12):
        #         print(x + 1)
                date = str((month + 1)) + "/" + str(year)
                if year == 2024 and month == 9:
                    break
                dates += [date]
        upt = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-11/September%202024%20Complete%20Monthly%20Ridership%20%28with%20adjustments%20and%20estimates%29_241101.xlsx', sheet_name="UPT", engine="openpyxl")
        upt[dates] = upt[dates].fillna(0)
        upt[['UACE CD', 'NTD ID']] = upt[['UACE CD', 'NTD ID']].fillna(0)

        for x in upt.index: 
            print(x)
            transit_agencies = TransitAgency.objects.filter(ntd_id=upt['NTD ID'][x], legacy_ntd_id=upt['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    ntd_id = upt['NTD ID'][x],
                    legacy_ntd_id = upt['Legacy NTD ID'][x],
                    agency_name = upt['Agency'][x],
                    # agency_status = upt['Status'][x],
                    reporter_type = upt['Reporter Type'][x],
                    uza_name = upt['UZA Name'][x],
                    uza = upt['UACE CD'][x]
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            # print(x)
            # print(upt[year][x])
            new_data = []
            for date in dates:
                date_split = date.split("/")
                month = date_split[0]
                year = date_split[1]
                new_transit_expense = MonthlyUnlinkedPassengerTrips(
                    transit_agency=transit_agency,
                    mode_id = upt['Mode'][x],
                    service_id = upt['TOS'][x],
                    year = int(year),
                    month = int(month),
                    date =  datetime.datetime(day=1,month=int(month),year=int(year)),
                    upt = upt[date][x]
                )
                new_data += [new_transit_expense]
            MonthlyUnlinkedPassengerTrips.objects.bulk_create(new_data)