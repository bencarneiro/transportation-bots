from django.core.management.base import BaseCommand
from views.models import PassengerMilesTraveled, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2022):
            years += [str(x)]
        pmt = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode_0.xlsx', sheet_name="PMT", engine="openpyxl")
        pmt[years] = pmt[years].fillna(0)
        pmt[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = pmt[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
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
                    uza_name = pmt['UZA Name'][x],
                    uza = pmt['UZA'][x],
                    uza_area_sqm = pmt['UZA Area SQ Miles'][x],
                    uza_population = pmt['UZA Population'][x],
                    status_2021 = pmt['2021 Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(pmt[year][x])
            for year in years:
                new_transit_expense = PassengerMilesTraveled(
                    transit_agency=transit_agency,
                    mode_id = pmt['Mode'][x],
                    service_id = pmt['Service'][x],
                    year = int(year),
                    pmt = pmt[year][x]
                ).save()