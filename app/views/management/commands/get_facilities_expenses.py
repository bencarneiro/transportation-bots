from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1992,2022):
            years += [str(x)]
        expense_facilities = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS3.1%20Capital%20Expenditures%20Time%20Series_0.xlsx', sheet_name="Facilities", engine="openpyxl")
        expense_facilities[years] = expense_facilities[years].fillna(0)
        expense_facilities[['UZA', 'UZA Area SQ Miles', 'UZA Population']] = expense_facilities[['UZA', 'UZA Area SQ Miles', 'UZA Population']].fillna(0)
        for x in expense_facilities.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_facilities['NTD ID'][x], legacy_ntd_id=expense_facilities['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=expense_facilities['Last Report Year'][x],
                    ntd_id = expense_facilities['NTD ID'][x],
                    legacy_ntd_id = expense_facilities['Legacy NTD ID'][x],
                    agency_name = expense_facilities['Agency Name'][x],
                    agency_status = expense_facilities['Agency Status'][x],
                    reporter_type = expense_facilities['Reporter Type'][x],
                    reporting_module = expense_facilities['Reporting Module'][x],
                    city = expense_facilities['City'][x],
                    state = expense_facilities['State'][x],
                    census_year = expense_facilities['Census Year'][x],
                    uza_name = expense_facilities['UZA Name'][x],
                    uza = expense_facilities['UZA'][x],
                    uza_area_sqm = expense_facilities['UZA Area SQ Miles'][x],
                    uza_population = expense_facilities['UZA Population'][x],
                    status_2021 = expense_facilities['2021 Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_facilities[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency_id=transit_agency,
                    mode = expense_facilities['Mode'][x],
                    service = "DO"
                    year = int(year),
                    expense_type = "FC",
                    expense = expense_facilities[year][x]
                ).save()