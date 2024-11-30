#!/bin/bash

python3 manage.py delete_all_transit_data
echo "everything deleted"

python3 manage.py fill_cpi_table
echo "cpi done"
python3 manage.py fill_mode_tables
echo "modes done"

python3 manage.py get_vo_expenses
echo "done with vo opexp"
python3 manage.py get_vm_expenses
echo "done with vm opexp"
python3 manage.py get_nvm_expenses
echo "done with nvm opexp"
python3 manage.py get_ga_expenses
echo "done with ga opexp"

python3 manage.py get_rolling_stock_expense
echo "done with rs capexp"
python3 manage.py get_facilities_expenses
echo "done with fac capexp"
python3 manage.py get_other_capital_expenses
echo "done with other capexp"

python3 manage.py get_fares
echo "done with fares"

python3 manage.py get_upt
echo "done with upt"
python3 manage.py get_pmt
echo "done with pmt"
python3 manage.py get_vrh
echo "done with vrh"
python3 manage.py get_vrm
echo "done with vrm"
python3 manage.py get_voms
echo "done with voms"
python3 manage.py get_drm
echo "done with drm"

python3 manage.py get_monthly_upt
echo "done with monthly upt"
python3 manage.py get_monthly_vrh
echo "done with monthly vrh"
python3 manage.py get_monthly_vrm
echo "done with monthly vrm"
python3 manage.py get_monthly_voms
echo "done with monthly voms"

python3 manage.py rewrite_transit_agency
echo "done reqriting transit agency to shapefiles"