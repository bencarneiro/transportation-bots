from django.core.management.base import BaseCommand
from views.models import VehicleRevenueHours, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2024):
            years += [str(x)]
        vrh = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode.xlsx', sheet_name="VRH", engine="openpyxl")
        vrh[years] = vrh[years].fillna(0)
        vrh[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = vrh[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in vrh.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=vrh['NTD ID'][x], legacy_ntd_id=vrh['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=vrh['Last Report Year'][x],
                    ntd_id = vrh['NTD ID'][x],
                    legacy_ntd_id = vrh['Legacy NTD ID'][x],
                    agency_name = vrh['Agency Name'][x],
                    agency_status = vrh['Agency Status'][x],
                    reporter_type = vrh['Reporter Type'][x],
                    reporting_module = vrh['Reporting Module'][x],
                    city = vrh['City'][x],
                    state = vrh['State'][x],
                    census_year = vrh['Census Year'][x],
                    uza_name = vrh['Primary UZA Name'][x],
                    uza = vrh['UACE Code'][x],
                    uza_area_sqm = vrh['UZA Area SQ Miles'][x],
                    uza_population = vrh['UZA Population'][x],
                    # status_2021 = vrh['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            
            trips = []
            for year in years:
                year_of_trips = VehicleRevenueHours(
                    transit_agency=transit_agency,
                    mode_id = vrh['Mode'][x],
                    service_id = vrh['Service'][x],
                    year = int(year),
                    vrh = vrh[year][x]
                )
                trips += [year_of_trips]
            VehicleRevenueHours.objects.bulk_create(trips)