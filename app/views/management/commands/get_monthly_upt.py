from django.core.management.base import BaseCommand
from views.models import MonthlyUnlinkedPassengerTrips, TransitAgency
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
        upt = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2023-05/March%202023%20Complete%20Monthly%20Ridership%20%28with%20adjustments%20and%20estimates%29.xlsx', sheet_name="UPT", engine="openpyxl")
        upt[dates] = upt[dates].fillna(0)
        upt[['UZA', 'NTD ID']] = upt[['UZA', 'NTD ID']].fillna(0)

        for x in upt.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=upt['NTD ID'][x], legacy_ntd_id=upt['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    ntd_id = upt['NTD ID'][x],
                    legacy_ntd_id = upt['Legacy NTD ID'][x],
                    agency_name = upt['Agency'][x],
                    agency_status = upt['Status'][x],
                    reporter_type = upt['Reporter Type'][x],
                    uza_name = upt['UZA Name'][x],
                    uza = upt['UZA'][x]
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            # print(x)
            # print(upt[year][x])
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
                ).save()