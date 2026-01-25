from django.core.management.base import BaseCommand
from views.models import VehicleRevenueHours, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        
        for x in range(2015,2025):
            years += [str(x)]
        vrh = pd.read_excel('/root/opexp_2024.xlsx', sheet_name="VRH", engine="openpyxl")
        vrh[years] = vrh[years].fillna(0)
        vrh[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = vrh[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in vrh.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=vrh['NTD ID'][x])
            if len(transit_agencies) < 1:
                try: 
                    census = int(vrh['Census Year'][x])
                except:
                    census = None
                transit_agency = TransitAgency(
                    last_report_year=vrh['Last Report Year'][x],
                    ntd_id = vrh['NTD ID'][x],
                    agency_name = vrh['Agency Name'][x],
                    agency_status = vrh['Agency Status'][x],
                    reporter_type = vrh['Reporter Type'][x],
                    reporting_module = vrh['Reporting Module'][x],
                    city = vrh['City'][x],
                    state = vrh['State'][x],
                    census_year = census,
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
                    service_id = vrh['Type of Service'][x],
                    year = int(year),
                    vrh = vrh[year][x]
                )
                trips += [year_of_trips]
            VehicleRevenueHours.objects.bulk_create(trips)