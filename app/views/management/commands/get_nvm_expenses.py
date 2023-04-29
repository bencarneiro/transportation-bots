from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(1991,2022):
            years += [str(x)]
        expense_nvm = pd.read_excel('https://www.transit.dot.gov/sites/fta.dot.gov/files/2022-10/TS2.1%20Service%20Data%20and%20Operating%20Expenses%20Time%20Series%20by%20Mode_0.xlsx', sheet_name="OpExp NVM", engine="openpyxl")
        expense_nvm[years] = expense_nvm[years].fillna(0)
        expense_nvm[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = expense_nvm[['UZA', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in expense_nvm.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_nvm['NTD ID'][x], legacy_ntd_id=expense_nvm['Legacy NTD ID'][x])
            if len(transit_agencies) < 1:
                transit_agency = TransitAgency(
                    last_report_year=expense_nvm['Last Report Year'][x],
                    ntd_id = expense_nvm['NTD ID'][x],
                    legacy_ntd_id = expense_nvm['Legacy NTD ID'][x],
                    agency_name = expense_nvm['Agency Name'][x],
                    agency_status = expense_nvm['Agency Status'][x],
                    reporter_type = expense_nvm['Reporter Type'][x],
                    reporting_module = expense_nvm['Reporting Module'][x],
                    city = expense_nvm['City'][x],
                    state = expense_nvm['State'][x],
                    census_year = expense_nvm['Census Year'][x],
                    uza_name = expense_nvm['UZA Name'][x],
                    uza = expense_nvm['UZA'][x],
                    uza_area_sqm = expense_nvm['UZA Area SQ Miles'][x],
                    uza_population = expense_nvm['UZA Population'][x],
                    status_2021 = expense_nvm['2021 Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_nvm[year][x])
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode_id = expense_nvm['Mode'][x],
                    service_id = expense_nvm['Service'][x],
                    year_id = int(year),
                    expense_type_id = "NVM",
                    expense = expense_nvm[year][x]
                ).save()