from django.core.management.base import BaseCommand
from views.models import PassengerMilesTraveled, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        storage_options = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"} 
        for x in range(2015,2025):
            years += [str(x)]
        pmt = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2025-10/2024%20TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode.xlsx', storage_options=storage_options, sheet_name="PMT", engine="openpyxl")
        pmt[years] = pmt[years].fillna(0)
        pmt[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = pmt[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in pmt.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=pmt['NTD ID'][x])
            if len(transit_agencies) < 1:
                try: 
                    census = int(pmt['Census Year'][x])
                except:
                    census = None
                transit_agency = TransitAgency(
                    last_report_year=pmt['Last Report Year'][x],
                    ntd_id = pmt['NTD ID'][x],
                    agency_name = pmt['Agency Name'][x],
                    agency_status = pmt['Agency Status'][x],
                    reporter_type = pmt['Reporter Type'][x],
                    reporting_module = pmt['Reporting Module'][x],
                    city = pmt['City'][x],
                    state = pmt['State'][x],
                    census_year = census,
                    uza_name = pmt['Primary UZA Name'][x],
                    uza = pmt['UACE Code'][x],
                    uza_area_sqm = pmt['UZA Area SQ Miles'][x],
                    uza_population = pmt['UZA Population'][x],
                    # status_2021 = pmt['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            
            trips = []
            for year in years:
                year_of_trips = PassengerMilesTraveled(
                    transit_agency=transit_agency,
                    mode_id = pmt['Mode'][x],
                    service_id = pmt['Type of Service'][x],
                    year = int(year),
                    pmt = pmt[year][x]
                )
                trips += [year_of_trips]
            PassengerMilesTraveled.objects.bulk_create(trips)