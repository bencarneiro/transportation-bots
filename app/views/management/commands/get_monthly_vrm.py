from django.core.management.base import BaseCommand
from views.models import MonthlyVehicleRevenueMiles, TransitAgency
import pandas as pd
import datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        storage_options = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"} 
        MonthlyVehicleRevenueMiles.objects.all().delete()
        dates = []
        for year in range(2002,2026):
        #     print(z)
            for month in range(12):
        #         print(x + 1)
                date = str((month + 1)) + "/" + str(year)
                if year == 2025 and month == 11:
                    break
                dates += [date]
        vrm = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2026-01/November%20Complete%20Monthly%20Ridership%20%28with%20adjustments%20and%20estimates%29_260102.xlsx', storage_options=storage_options, sheet_name="VRM", engine="openpyxl")
        vrm[dates] = vrm[dates].fillna(0)
        vrm[['UACE CD', 'NTD ID']] = vrm[['UACE CD', 'NTD ID']].fillna(0)

        for x in vrm.index: 
            print(x)
            transit_agencies = TransitAgency.objects.filter(ntd_id=vrm['NTD ID'][x], legacy_ntd_id=vrm['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    ntd_id = vrm['NTD ID'][x],
                    legacy_ntd_id = vrm['Legacy NTD ID'][x],
                    agency_name = vrm['Agency'][x],
                    # agency_status = vrm['Status'][x],
                    reporter_type = vrm['Reporter Type'][x],
                    uza_name = vrm['UZA Name'][x],
                    uza = vrm['UACE CD'][x]
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            # print(x)
            # print(vrm[year][x])
            new_data = []
            for date in dates:
                date_split = date.split("/")
                month = date_split[0]
                year = date_split[1]
                new_transit_expense = MonthlyVehicleRevenueMiles(
                    transit_agency=transit_agency,
                    mode_id = vrm['Mode'][x],
                    service_id = vrm['TOS'][x],
                    year = int(year),
                    month = int(month),
                    date =  datetime.datetime(day=1,month=int(month),year=int(year)),
                    vrm = vrm[date][x]
                )
                new_data += [new_transit_expense]
            MonthlyVehicleRevenueMiles.objects.bulk_create(new_data)