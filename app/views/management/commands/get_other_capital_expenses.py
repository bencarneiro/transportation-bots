from django.core.management.base import BaseCommand
from views.models import TransitExpense
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1992,2022):
            years += [str(x)]
        expense_capital_other = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS3.1%20Capital%20Expenditures%20Time%20Series_0.xlsx', sheet_name="Other", engine="openpyxl")
        expense_capital_other[years] = expense_capital_other[years].fillna(0)
        for x in expense_capital_other.index:
            print(x)
            # print(expense_capital_other[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
                    last_report_year=expense_capital_other['Last Report Year'][x],
                    ntd_id = expense_capital_other['NTD ID'][x],
                    legacy_ntd_id = expense_capital_other['Legacy NTD ID'][x],
                    agency_name = expense_capital_other['Agency Name'][x],
                    agency_status = expense_capital_other['Agency Status'][x],
                    reporter_type = expense_capital_other['Reporter Type'][x],
                    reporting_module = expense_capital_other['Reporting Module'][x],
                    city = expense_capital_other['City'][x],
                    state = expense_capital_other['State'][x],
                    census_year = expense_capital_other['Census Year'][x],
                    uza_name = expense_capital_other['UZA Name'][x],
                    uza = expense_capital_other['UZA'][x],
                    uza_area_sqm = expense_capital_other['UZA Area SQ Miles'][x],
                    uza_population = expense_capital_other['UZA Population'][x],
                    status_2021 = expense_capital_other['2021 Status'][x],
                    mode = expense_capital_other['Mode'][x],
                    service = "DO",
                    year = int(year),
                    expense_type = "OC",
                    expense = expense_capital_other[year][x]
                ).save()