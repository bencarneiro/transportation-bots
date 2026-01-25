from django.core.management.base import BaseCommand
from views.models import MonthlyVehiclesOperatedMaximumService, TransitAgency
import pandas as pd
import datetime


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        MonthlyVehiclesOperatedMaximumService.objects.all().delete()
        dates = []
        for year in range(2002,2026):
        #     print(z)
            for month in range(12):
        #         print(x + 1)
                date = str((month + 1)) + "/" + str(year)
                if year == 2025 and month == 11:
                    break
                dates += [date]
        voms = pd.read_excel('/root/monthly.xlsx', sheet_name="VOMS", engine="openpyxl")
        voms[dates] = voms[dates].fillna(0)
        voms[['UACE CD', 'NTD ID']] = voms[['UACE CD', 'NTD ID']].fillna(0)

        for x in voms.index: 
            print(x)
            transit_agencies = TransitAgency.objects.filter(ntd_id=voms['NTD ID'][x], legacy_ntd_id=voms['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    ntd_id = voms['NTD ID'][x],
                    legacy_ntd_id = voms['Legacy NTD ID'][x],
                    agency_name = voms['Agency'][x],
                    # agency_status = voms['Status'][x],
                    reporter_type = voms['Reporter Type'][x],
                    uza_name = voms['UZA Name'][x],
                    uza = voms['UACE CD'][x]
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            # print(x)
            # print(voms[year][x])
            new_data = []
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
                )
                new_data += [new_transit_expense]
            MonthlyVehiclesOperatedMaximumService.objects.bulk_create(new_data)