from django.core.management.base import BaseCommand
from views.models import MonthlyVehicleRevenueHours, TransitAgency
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
        vrh = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2023-05/March%202023%20Complete%20Monthly%20Ridership%20%28with%20adjustments%20and%20estimates%29.xlsx', sheet_name="VRH", engine="openpyxl")
        vrh[dates] = vrh[dates].fillna(0)
        vrh[['UZA', 'NTD ID']] = vrh[['UZA', 'NTD ID']].fillna(0)

        for x in vrh.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=vrh['NTD ID'][x], legacy_ntd_id=vrh['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    ntd_id = vrh['NTD ID'][x],
                    legacy_ntd_id = vrh['Legacy NTD ID'][x],
                    agency_name = vrh['Agency'][x],
                    agency_status = vrh['Status'][x],
                    reporter_type = vrh['Reporter Type'][x],
                    uza_name = vrh['UZA Name'][x],
                    uza = vrh['UZA'][x]
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            # print(x)
            # print(vrh[year][x])
            for date in dates:
                date_split = date.split("/")
                month = date_split[0]
                year = date_split[1]
                new_transit_expense = MonthlyVehicleRevenueHours(
                    transit_agency=transit_agency,
                    mode_id = vrh['Mode'][x],
                    service_id = vrh['TOS'][x],
                    year = int(year),
                    month = int(month),
                    date =  datetime.datetime(day=1,month=int(month),year=int(year)),
                    vrh = vrh[date][x]
                ).save()