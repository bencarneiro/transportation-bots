from django.core.management.base import BaseCommand
from views.models import VehicleRevenueMiles, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2024):
            years += [str(x)]
        vrm = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode.xlsx', sheet_name="VRM", engine="openpyxl")
        vrm[years] = vrm[years].fillna(0)
        vrm[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = vrm[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in vrm.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=vrm['NTD ID'][x], legacy_ntd_id=vrm['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=vrm['Last Report Year'][x],
                    ntd_id = vrm['NTD ID'][x],
                    legacy_ntd_id = vrm['Legacy NTD ID'][x],
                    agency_name = vrm['Agency Name'][x],
                    agency_status = vrm['Agency Status'][x],
                    reporter_type = vrm['Reporter Type'][x],
                    reporting_module = vrm['Reporting Module'][x],
                    city = vrm['City'][x],
                    state = vrm['State'][x],
                    census_year = vrm['Census Year'][x],
                    uza_name = vrm['Primary UZA Name'][x],
                    uza = vrm['UACE Code'][x],
                    uza_area_sqm = vrm['UZA Area SQ Miles'][x],
                    uza_population = vrm['UZA Population'][x],
                    # status_2021 = vrm['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            
            trips = []
            for year in years:
                year_of_trips = VehicleRevenueMiles(
                    transit_agency=transit_agency,
                    mode_id = vrm['Mode'][x],
                    service_id = vrm['Service'][x],
                    year = int(year),
                    vrm = vrm[year][x]
                )
                trips += [year_of_trips]
            VehicleRevenueMiles.objects.bulk_create(trips)