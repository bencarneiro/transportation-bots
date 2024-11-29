from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1992,2024):
            years += [str(x)]
        expense_fc = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS3.1%20Capital%20Expenditures%20Time%20Series.xlsx', sheet_name="Facilities", engine="openpyxl")
        expense_fc[years] = expense_fc[years].fillna(0)
        expense_fc[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = expense_fc[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in expense_fc.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_fc['NTD ID'][x], legacy_ntd_id=expense_fc['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=expense_fc['Last Report Year'][x],
                    ntd_id = expense_fc['NTD ID'][x],
                    legacy_ntd_id = expense_fc['Legacy NTD ID'][x],
                    agency_name = expense_fc['Agency Name'][x],
                    agency_status = expense_fc['Agency Status'][x],
                    reporter_type = expense_fc['Reporter Type'][x],
                    reporting_module = expense_fc['Reporting Module'][x],
                    city = expense_fc['City'][x],
                    state = expense_fc['State'][x],
                    census_year = expense_fc['Census Year'][x],
                    uza_name = expense_fc['UZA Name'][x],
                    uza = expense_fc['UACE Code'][x],
                    uza_area_sqm = expense_fc['UZA Area SQ Miles'][x],
                    uza_population = expense_fc['UZA Population'][x],
                    # status_2021 = expense_fc['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_fc[year][x])
            expenses = []
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode_id = expense_fc['Mode'][x],
                    service_id = "DO",
                    year_id = int(year),
                    expense_type_id = "FC",
                    expense = expense_fc[year][x]
                )
                expenses += [new_transit_expense]
            TransitExpense.objects.bulk_create(expenses)