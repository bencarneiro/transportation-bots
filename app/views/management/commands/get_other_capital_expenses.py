from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1992,2024):
            years += [str(x)]
        expense_other = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2024-10/2023%20TS3.1%20Capital%20Expenditures%20Time%20Series.xlsx', sheet_name="Other", engine="openpyxl")
        expense_other[years] = expense_other[years].fillna(0)
        expense_other[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = expense_other[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in expense_other.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_other['NTD ID'][x], legacy_ntd_id=expense_other['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=expense_other['Last Report Year'][x],
                    ntd_id = expense_other['NTD ID'][x],
                    legacy_ntd_id = expense_other['Legacy NTD ID'][x],
                    agency_name = expense_other['Agency Name'][x],
                    agency_status = expense_other['Agency Status'][x],
                    reporter_type = expense_other['Reporter Type'][x],
                    reporting_module = expense_other['Reporting Module'][x],
                    city = expense_other['City'][x],
                    state = expense_other['State'][x],
                    census_year = expense_other['Census Year'][x],
                    uza_name = expense_other['UZA Name'][x],
                    uza = expense_other['UACE Code'][x],
                    uza_area_sqm = expense_other['UZA Area SQ Miles'][x],
                    uza_population = expense_other['UZA Population'][x],
                    # status_2021 = expense_other['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_other[year][x])
            expenses = []
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode_id = expense_other['Mode'][x],
                    service_id = "DO",
                    year_id = int(year),
                    expense_type_id = "OC",
                    expense = expense_other[year][x]
                )
                expenses += [new_transit_expense]
            TransitExpense.objects.bulk_create(expenses)