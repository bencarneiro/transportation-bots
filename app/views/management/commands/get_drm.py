from django.core.management.base import BaseCommand
from views.models import DirectionalRouteMiles, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2024):
            years += [str(x)]
        drm = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode.xlsx', sheet_name="DRM", engine="openpyxl")
        drm[years] = drm[years].fillna(0)
        drm[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = drm[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in drm.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=drm['NTD ID'][x], legacy_ntd_id=drm['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=drm['Last Report Year'][x],
                    ntd_id = drm['NTD ID'][x],
                    legacy_ntd_id = drm['Legacy NTD ID'][x],
                    agency_name = drm['Agency Name'][x],
                    agency_status = drm['Agency Status'][x],
                    reporter_type = drm['Reporter Type'][x],
                    reporting_module = drm['Reporting Module'][x],
                    city = drm['City'][x],
                    state = drm['State'][x],
                    census_year = drm['Census Year'][x],
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
                    service_id = drm['Service'][x],
                    year = int(year),
                    drm = drm[year][x]
                )
                trips += [year_of_trips]
            DirectionalRouteMiles.objects.bulk_create(trips)