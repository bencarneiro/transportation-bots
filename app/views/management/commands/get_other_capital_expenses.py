from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1992,2022):
            years += [str(x)]
        expense_other_capital = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS3.1%20Capital%20Expenditures%20Time%20Series_0.xlsx', sheet_name="Other", engine="openpyxl")
        expense_other_capital[years] = expense_other_capital[years].fillna(0)
        expense_other_capital[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = expense_other_capital[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in expense_other_capital.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_other_capital['NTD ID'][x], legacy_ntd_id=expense_other_capital['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=expense_other_capital['Last Report Year'][x],
                    ntd_id = expense_other_capital['NTD ID'][x],
                    legacy_ntd_id = expense_other_capital['Legacy NTD ID'][x],
                    agency_name = expense_other_capital['Agency Name'][x],
                    agency_status = expense_other_capital['Agency Status'][x],
                    reporter_type = expense_other_capital['Reporter Type'][x],
                    reporting_module = expense_other_capital['Reporting Module'][x],
                    city = expense_other_capital['City'][x],
                    state = expense_other_capital['State'][x],
                    census_year = expense_other_capital['Census Year'][x],
                    uza_name = expense_other_capital['UZA Name'][x],
                    uza = expense_other_capital['UZA'][x],
                    uza_area_sqm = expense_other_capital['UZA Area SQ Miles'][x],
                    uza_population = expense_other_capital['UZA Population'][x],
                    status_2021 = expense_other_capital['2021 Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_other_capital[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode = expense_other_capital['Mode'][x],
                    service = "DO",
                    year = int(year),
                    expense_type = "OC",
                    expense = expense_other_capital[year][x]
                ).save()