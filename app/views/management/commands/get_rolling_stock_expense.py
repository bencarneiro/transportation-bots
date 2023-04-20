from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1992,2022):
            years += [str(x)]
        expense_ga = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS3.1%20Capital%20Expenditures%20Time%20Series_0.xlsx', sheet_name="Rolling Stock", engine="openpyxl")
        expense_ga[years] = expense_ga[years].fillna(0)
        expense_ga[['UZA', 'UZA Area SQ Miles', 'UZA Population']] = expense_ga[['UZA', 'UZA Area SQ Miles', 'UZA Population']].fillna(0)
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
                    uza_name = expense_ga['UZA Name'][x],
                    uza = expense_ga['UZA'][x],
                    uza_area_sqm = expense_ga['UZA Area SQ Miles'][x],
                    uza_population = expense_ga['UZA Population'][x],
                    status_2021 = expense_ga['2021 Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_ga[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode = expense_ga['Mode'][x],
                    service = "DO",
                    year = int(year),
                    expense_type = "RS",
                    expense = expense_ga[year][x]
                ).save()