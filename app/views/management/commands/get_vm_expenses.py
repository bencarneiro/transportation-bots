from django.core.management.base import BaseCommand
from views.models import TransitExpense
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2022):
            years += [str(x)]
        expense_vm = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode_0.xlsx', sheet_name="OpExp VM", engine="openpyxl")
        expense_vm[years] = expense_vm[years].fillna(0)
        expense_vm[['UZA', 'UZA Area SQ Miles', 'UZA Population']] = expense_vm[['UZA', 'UZA Area SQ Miles', 'UZA Population']].fillna(0)
        for x in expense_vm.index:
            print(x)
            # print(expense_vm[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
                    last_report_year=expense_vm['Last Report Year'][x],
                    ntd_id = expense_vm['NTD ID'][x],
                    legacy_ntd_id = expense_vm['Legacy NTD ID'][x],
                    agency_name = expense_vm['Agency Name'][x],
                    agency_status = expense_vm['Agency Status'][x],
                    reporter_type = expense_vm['Reporter Type'][x],
                    reporting_module = expense_vm['Reporting Module'][x],
                    city = expense_vm['City'][x],
                    state = expense_vm['State'][x],
                    census_year = expense_vm['Census Year'][x],
                    uza_name = expense_vm['UZA Name'][x],
                    uza = expense_vm['UZA'][x],
                    uza_area_sqm = expense_vm['UZA Area SQ Miles'][x],
                    uza_population = expense_vm['UZA Population'][x],
                    status_2021 = expense_vm['2021 Status'][x],
                    mode = expense_vm['Mode'][x],
                    service = expense_vm['Service'][x],
                    status_mode = expense_vm['Mode Status'][x],
                    year = int(year),
                    expense_type = "VM",
                    expense = expense_vm[year][x]
                ).save()