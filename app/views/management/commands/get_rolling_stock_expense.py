from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1992,2024):
            years += [str(x)]
        expense_rs = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS3.1%20Capital%20Expenditures%20Time%20Series.xlsx', sheet_name="Rolling Stock", engine="openpyxl")
        expense_rs[years] = expense_rs[years].fillna(0)
        expense_rs[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = expense_rs[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in expense_rs.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_rs['NTD ID'][x], legacy_ntd_id=expense_rs['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=expense_rs['Last Report Year'][x],
                    ntd_id = expense_rs['NTD ID'][x],
                    legacy_ntd_id = expense_rs['Legacy NTD ID'][x],
                    agency_name = expense_rs['Agency Name'][x],
                    agency_status = expense_rs['Agency Status'][x],
                    reporter_type = expense_rs['Reporter Type'][x],
                    reporting_module = expense_rs['Reporting Module'][x],
                    city = expense_rs['City'][x],
                    state = expense_rs['State'][x],
                    census_year = expense_rs['Census Year'][x],
                    uza_name = expense_rs['UZA Name'][x],
                    uza = expense_rs['UACE Code'][x],
                    uza_area_sqm = expense_rs['UZA Area SQ Miles'][x],
                    uza_population = expense_rs['UZA Population'][x],
                    # status_2021 = expense_rs['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_rs[year][x])
            expenses = []
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode_id = expense_rs['Mode'][x],
                    service_id = "DO",
                    year_id = int(year),
                    expense_type_id = "RS",
                    expense = expense_rs[year][x]
                )
                expenses += [new_transit_expense]
            TransitExpense.objects.bulk_create(expenses)