from django.core.management.base import BaseCommand
from views.models import DirectionalRouteMiles, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        
        for x in range(2015,2025):
            years += [str(x)]
        drm = pd.read_excel('/root/opexp_2024.xlsx', sheet_name="DRM", engine="openpyxl")
        drm[years] = drm[years].fillna(0)
        drm[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = drm[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in drm.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=drm['NTD ID'][x])
            if len(transit_agencies) < 1:
                try: 
                    census = int(drm['Census Year'][x])
                except:
                    census = None
                transit_agency = TransitAgency(
                    last_report_year=drm['Last Report Year'][x],
                    ntd_id = drm['NTD ID'][x],
                    agency_name = drm['Agency Name'][x],
                    agency_status = drm['Agency Status'][x],
                    reporter_type = drm['Reporter Type'][x],
                    reporting_module = drm['Reporting Module'][x],
                    city = drm['City'][x],
                    state = drm['State'][x],
                    census_year = census,
                    uza_name = drm['Primary UZA Name'][x],
                    uza = drm['UACE Code'][x],
                    uza_area_sqm = drm['UZA Area SQ Miles'][x],
                    uza_population = drm['UZA Population'][x],
                    # status_2021 = drm['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            
            trips = []
            for year in years:
                year_of_trips = DirectionalRouteMiles(
                    transit_agency=transit_agency,
                    mode_id = drm['Mode'][x],
                    service_id = drm['Type of Service'][x],
                    year = int(year),
                    drm = drm[year][x]
                )
                trips += [year_of_trips]
            DirectionalRouteMiles.objects.bulk_create(trips)