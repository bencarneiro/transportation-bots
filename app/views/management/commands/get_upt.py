from django.core.management.base import BaseCommand
from views.models import UnlinkedPassengerTrips, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        storage_options = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"} 
        for x in range(2015,2025):
            years += [str(x)]
        upt = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2025-10/2024%20TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode.xlsx', storage_options=storage_options, sheet_name="UPT", engine="openpyxl")
        upt[years] = upt[years].fillna(0)
        upt[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = upt[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in upt.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=upt['NTD ID'][x])
            if len(transit_agencies) < 1:
                try: 
                    census = int(upt['Census Year'][x])
                except:
                    census = None
                transit_agency = TransitAgency(
                    last_report_year=upt['Last Report Year'][x],
                    ntd_id = upt['NTD ID'][x],
                    agency_name = upt['Agency Name'][x],
                    agency_status = upt['Agency Status'][x],
                    reporter_type = upt['Reporter Type'][x],
                    reporting_module = upt['Reporting Module'][x],
                    city = upt['City'][x],
                    state = upt['State'][x],
                    census_year = census,
                    uza_name = upt['Primary UZA Name'][x],
                    uza = upt['UACE Code'][x],
                    uza_area_sqm = upt['UZA Area SQ Miles'][x],
                    uza_population = upt['UZA Population'][x],
                    # status_2021 = upt['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(upt[year][x])
            trips = []
            for year in years:
                year_of_trips = UnlinkedPassengerTrips(
                    transit_agency=transit_agency,
                    mode_id = upt['Mode'][x],
                    service_id = upt['Type of Service'][x],
                    year = int(year),
                    upt = upt[year][x]
                )
                trips += [year_of_trips]
            UnlinkedPassengerTrips.objects.bulk_create(trips)