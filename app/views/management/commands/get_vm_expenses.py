from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency
import pandas as pd


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        years = []
        for x in range(2015,2025):
            years += [str(x)]

        
        expense_vm = pd.read_excel('/root/opexp_2024.xlsx', sheet_name="OpExp VM", engine="openpyxl")
        expense_vm[years] = expense_vm[years].fillna(0)
        expense_vm[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']] = expense_vm[['UACE Code', 'UZA Area SQ Miles', 'UZA Population', 'NTD ID']].fillna(0)
        for x in expense_vm.index: 
            transit_agencies = TransitAgency.objects.filter(ntd_id=expense_vm['NTD ID'][x])
            if len(transit_agencies) < 1:
                try: 
                    census = int(expense_vm['Census Year'][x])
                except:
                    census = None
                transit_agency = TransitAgency(
                    last_report_year=expense_vm['Last Report Year'][x],
                    ntd_id = expense_vm['NTD ID'][x],
                    agency_name = expense_vm['Agency Name'][x],
                    agency_status = expense_vm['Agency Status'][x],
                    reporter_type = expense_vm['Reporter Type'][x],
                    reporting_module = expense_vm['Reporting Module'][x],
                    city = expense_vm['City'][x],
                    state = expense_vm['State'][x],
                    census_year = census,
                    uza_name = expense_vm['Primary UZA Name'][x],
                    uza = expense_vm['UACE Code'][x],
                    uza_area_sqm = expense_vm['UZA Area SQ Miles'][x],
                    uza_population = expense_vm['UZA Population'][x],
                    # status_2021 = expense_vm['Agency Status'][x],
                )
                transit_agency.save()
            else:
                transit_agency = transit_agencies[0]
            print(x)
            # print(expense_vm[year][x])
            expenses = []
            for year in years:
                new_transit_expense = TransitExpense(
                    transit_agency=transit_agency,
                    mode_id = expense_vm['Mode'][x],
                    service_id = expense_vm['Type of Service'][x],
                    year_id = int(year),
                    expense_type_id = "VM",
                    expense = expense_vm[year][x]
                )
                expenses += [new_transit_expense]
            TransitExpense.objects.bulk_create(expenses)