from django.core.management.base import BaseCommand
from views.models import Fares, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        
        for x in range(2015,2025):
            years += [str(x)]
        fares = pd.read_excel('/root/opexp_2024.xlsx', sheet_name="Fares", engine="openpyxl")
        fares[years] = fares[years].fillna(0)
        fares[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = fares[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in fares.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=fares['NTD ID'][x])
            if len(transit_agencies) < 1:
                try: 
                    census = int(fares['Census Year'][x])
                except:
                    census = None
                transit_agency = TransitAgency(
                    last_report_year=fares['Last Report Year'][x],
                    ntd_id = fares['NTD ID'][x],
                    agency_name = fares['Agency Name'][x],
                    agency_status = fares['Agency Status'][x],
                    reporter_type = fares['Reporter Type'][x],
                    reporting_module = fares['Reporting Module'][x],
                    city = fares['City'][x],
                    state = fares['State'][x],
                    census_year = census,
                    uza_name = fares['Primary UZA Name'][x],
                    uza = fares['UACE Code'][x],
                    uza_area_sqm = fares['UZA Area SQ Miles'][x],
                    uza_population = fares['UZA Population'][x],
                    # status_2021 = fares['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            
            trips = []
            for year in years:
                year_of_trips = Fares(
                    transit_agency=transit_agency,
                    mode_id = fares['Mode'][x],
                    service_id = fares['Type of Service'][x],
                    year_id = int(year),
                    fares = fares[year][x]
                )
                trips += [year_of_trips]
            Fares.objects.bulk_create(trips)