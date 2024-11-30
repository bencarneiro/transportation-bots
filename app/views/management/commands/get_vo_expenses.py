from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2024):
            years += [str(x)]
        expense_vo = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode.xlsx', sheet_name="OpExp VO", engine="openpyxl")
        expense_vo[years] = expense_vo[years].fillna(0)
        expense_vo[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = expense_vo[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in expense_vo.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_vo['NTD ID'][x], legacy_ntd_id=expense_vo['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=expense_vo['Last Report Year'][x],
                    ntd_id = expense_vo['NTD ID'][x],
                    legacy_ntd_id = expense_vo['Legacy NTD ID'][x],
                    agency_name = expense_vo['Agency Name'][x],
                    agency_status = expense_vo['Agency Status'][x],
                    reporter_type = expense_vo['Reporter Type'][x],
                    reporting_module = expense_vo['Reporting Module'][x],
                    city = expense_vo['City'][x],
                    state = expense_vo['State'][x],
                    census_year = expense_vo['Census Year'][x],
                    uza_name = expense_vo['Primary UZA Name'][x],
                    uza = expense_vo['UACE Code'][x],
                    uza_area_sqm = expense_vo['UZA Area SQ Miles'][x],
                    uza_population = expense_vo['UZA Population'][x],
                    # status_2021 = expense_vo['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_vo[year][x])
            expenses = []
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode_id = expense_vo['Mode'][x],
                    service_id = expense_vo['Service'][x],
                    year_id = int(year),
                    expense_type_id = "VO",
                    expense = expense_vo[year][x]
                )
                expenses += [new_transit_expense]
            TransitExpense.objects.bulk_create(expenses)