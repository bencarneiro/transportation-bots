from django.core.management.base import BaseCommand
from views.models import TransitExpense
import requests
import pandas as pd


class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
    #     parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2022):
            years += [str(x)]
        expense_vo = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode_0.xlsx', sheet_name="OpExp VO", engine="openpyxl")
        expense_vo[years] = expense_vo[years].fillna(0)
        for x in expense_vo.index:
            print(x)
            # print(expense_vo[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
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
                    uza_name = expense_vo['UZA Name'][x],
                    uza = expense_vo['UZA'][x],
                    uza_area_sqm = expense_vo['UZA Area SQ Miles'][x],
                    uza_population = expense_vo['UZA Population'][x],
                    status_2021 = expense_vo['2021 Status'][x],
                    mode = expense_vo['Mode'][x],
                    service = expense_vo['Service'][x],
                    status_mode = expense_vo['Mode Status'][x],
                    year = int(year),
                    expense_type = "VO",
                    expense = expense_vo[year][x]
                ).save()
            break