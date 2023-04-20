from django.core.management.base import BaseCommand
from views.models import TransitExpense
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1992,2022):
            years += [str(x)]
        expense_rolling_stock = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS3.1%20Capital%20Expenditures%20Time%20Series_0.xlsx', sheet_name="Rolling Stock", engine="openpyxl")
        expense_rolling_stock[years] = expense_rolling_stock[years].fillna(0)
        for x in expense_rolling_stock.index:
            print(x)
            # print(expense_rolling_stock[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
                    last_report_year=expense_rolling_stock['Last Report Year'][x],
                    ntd_id = expense_rolling_stock['NTD ID'][x],
                    legacy_ntd_id = expense_rolling_stock['Legacy NTD ID'][x],
                    agency_name = expense_rolling_stock['Agency Name'][x],
                    agency_status = expense_rolling_stock['Agency Status'][x],
                    reporter_type = expense_rolling_stock['Reporter Type'][x],
                    reporting_module = expense_rolling_stock['Reporting Module'][x],
                    city = expense_rolling_stock['City'][x],
                    state = expense_rolling_stock['State'][x],
                    census_year = expense_rolling_stock['Census Year'][x],
                    uza_name = expense_rolling_stock['UZA Name'][x],
                    uza = expense_rolling_stock['UZA'][x],
                    uza_area_sqm = expense_rolling_stock['UZA Area SQ Miles'][x],
                    uza_population = expense_rolling_stock['UZA Population'][x],
                    status_2021 = expense_rolling_stock['2021 Status'][x],
                    mode = expense_rolling_stock['Mode'][x],
                    service = "DO",
                    year = int(year),
                    expense_type = "RS",
                    expense = expense_rolling_stock[year][x]
                ).save()