from django.core.management.base import BaseCommand
from views.models import MonthlyVehiclesOperatedMaximumService, TransitAgency
import pandas as pd
import datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        dates = []
        for year in range(2002,2024):
        #     print(z)
            for month in range(12):
        #         print(x + 1)
                date = str((month + 1)) + "/" + str(year)
                if year == 2023 and month == 3:
                    break
                dates += [date]
        voms = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2023-05/March%202023%20Complete%20Monthly%20Ridership%20%28with%20adjustments%20and%20estimates%29.xlsx', sheet_name="VOMS", engine="openpyxl")
        voms[dates] = voms[dates].fillna(0)
        voms[['UZA', 'NTD ID']] = voms[['UZA', 'NTD ID']].fillna(0)

        for x in voms.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=voms['NTD ID'][x], legacy_ntd_id=voms['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    ntd_id = voms['NTD ID'][x],
                    legacy_ntd_id = voms['Legacy NTD ID'][x],
                    agency_name = voms['Agency'][x],
                    agency_status = voms['Status'][x],
                    reporter_type = voms['Reporter Type'][x],
                    uza_name = voms['UZA Name'][x],
                    uza = voms['UZA'][x]
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            # print(x)
            # print(voms[year][x])
            for date in dates:
                date_split = date.split("/")
                month = date_split[0]
                year = date_split[1]
                new_transit_expense = MonthlyVehiclesOperatedMaximumService(
                    transit_agency=transit_agency,
                    mode_id = voms['Mode'][x],
                    service_id = voms['TOS'][x],
                    year = int(year),
                    month = int(month),
                    date =  datetime.datetime(day=1,month=int(month),year=int(year)),
                    voms = voms[date][x]
                ).save()