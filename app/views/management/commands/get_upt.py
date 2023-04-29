from django.core.management.base import BaseCommand
from views.models import UnlinkedPassengerTrips, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2022):
            years += [str(x)]
        upt = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode_0.xlsx', sheet_name="UPT", engine="openpyxl")
        upt[years] = upt[years].fillna(0)
        upt[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = upt[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in upt.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=upt['NTD ID'][x], legacy_ntd_id=upt['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=upt['Last Report Year'][x],
                    ntd_id = upt['NTD ID'][x],
                    legacy_ntd_id = upt['Legacy NTD ID'][x],
                    agency_name = upt['Agency Name'][x],
                    agency_status = upt['Agency Status'][x],
                    reporter_type = upt['Reporter Type'][x],
                    reporting_module = upt['Reporting Module'][x],
                    city = upt['City'][x],
                    state = upt['State'][x],
                    census_year = upt['Census Year'][x],
                    uza_name = upt['UZA Name'][x],
                    uza = upt['UZA'][x],
                    uza_area_sqm = upt['UZA Area SQ Miles'][x],
                    uza_population = upt['UZA Population'][x],
                    status_2021 = upt['2021 Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(upt[year][x])
            for year in years:
                new_transit_expense = UnlinkedPassengerTrips(
                    transit_agency=transit_agency,
                    mode_id = upt['Mode'][x],
                    service_id = upt['Service'][x],
                    year = int(year),
                    upt = upt[year][x]
                ).save()