from django.core.management.base import BaseCommand
from views.models import VehiclesOperatedMaximumService, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2022):
            years += [str(x)]
        voms = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode_0.xlsx', sheet_name="VOMS", engine="openpyxl")
        voms[years] = voms[years].fillna(0)
        voms[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = voms[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in voms.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=voms['NTD ID'][x], legacy_ntd_id=voms['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=voms['Last Report Year'][x],
                    ntd_id = voms['NTD ID'][x],
                    legacy_ntd_id = voms['Legacy NTD ID'][x],
                    agency_name = voms['Agency Name'][x],
                    agency_status = voms['Agency Status'][x],
                    reporter_type = voms['Reporter Type'][x],
                    reporting_module = voms['Reporting Module'][x],
                    city = voms['City'][x],
                    state = voms['State'][x],
                    census_year = voms['Census Year'][x],
                    uza_name = voms['UZA Name'][x],
                    uza = voms['UZA'][x],
                    uza_area_sqm = voms['UZA Area SQ Miles'][x],
                    uza_population = voms['UZA Population'][x],
                    status_2021 = voms['2021 Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(voms[year][x])
            for year in years:
                new_transit_expense = VehiclesOperatedMaximumService(
                    transit_agency=transit_agency,
                    mode = voms['Mode'][x],
                    service = voms['Service'][x],
                    year = int(year),
                    voms = voms[year][x]
                ).save()