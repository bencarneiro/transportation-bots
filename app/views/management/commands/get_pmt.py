from django.core.management.base import BaseCommand
from views.models import PassengerMilesTraveled, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2024):
            years += [str(x)]
        pmt = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode.xlsx', sheet_name="PMT", engine="openpyxl")
        pmt[years] = pmt[years].fillna(0)
        pmt[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = pmt[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in pmt.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=pmt['NTD ID'][x], legacy_ntd_id=pmt['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=pmt['Last Report Year'][x],
                    ntd_id = pmt['NTD ID'][x],
                    legacy_ntd_id = pmt['Legacy NTD ID'][x],
                    agency_name = pmt['Agency Name'][x],
                    agency_status = pmt['Agency Status'][x],
                    reporter_type = pmt['Reporter Type'][x],
                    reporting_module = pmt['Reporting Module'][x],
                    city = pmt['City'][x],
                    state = pmt['State'][x],
                    census_year = pmt['Census Year'][x],
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
                    service_id = pmt['Service'][x],
                    year = int(year),
                    pmt = pmt[year][x]
                )
                trips += [year_of_trips]
            PassengerMilesTraveled.objects.bulk_create(trips)