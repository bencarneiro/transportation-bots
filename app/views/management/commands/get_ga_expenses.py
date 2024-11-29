from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2024):
            years += [str(x)]
        expense_ga = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode.xlsx', sheet_name="OpExp GA", engine="openpyxl")
        expense_ga[years] = expense_ga[years].fillna(0)
        expense_ga[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = expense_ga[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in expense_ga.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_ga['NTD ID'][x], legacy_ntd_id=expense_ga['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=expense_ga['Last Report Year'][x],
                    ntd_id = expense_ga['NTD ID'][x],
                    legacy_ntd_id = expense_ga['Legacy NTD ID'][x],
                    agency_name = expense_ga['Agency Name'][x],
                    agency_status = expense_ga['Agency Status'][x],
                    reporter_type = expense_ga['Reporter Type'][x],
                    reporting_module = expense_ga['Reporting Module'][x],
                    city = expense_ga['City'][x],
                    state = expense_ga['State'][x],
                    census_year = expense_ga['Census Year'][x],
                    uza_name = expense_ga['Primary UZA Name'][x],
                    uza = expense_ga['UACE Code'][x],
                    uza_area_sqm = expense_ga['UZA Area SQ Miles'][x],
                    uza_population = expense_ga['UZA Population'][x],
                    # status_2021 = expense_ga['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_ga[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode_id = expense_ga['Mode'][x],
                    service_id = expense_ga['Service'][x],
                    year_id = int(year),
                    expense_type_id = "GA",
                    expense = expense_ga[year][x]
                ).save()