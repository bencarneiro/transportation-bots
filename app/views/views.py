from django.shortcuts import render
from views.models import Crash, TransitAgency, TransitExpense, MonthlyUnlinkedPassengerTrips, UnlinkedPassengerTrips, Fares, PassengerMilesTraveled, MonthlyVehicleRevenueHours, VehicleRevenueHours, MonthlyVehicleRevenueMiles, VehicleRevenueMiles, VehiclesOperatedMaximumService, MonthlyVehiclesOperatedMaximumService, DirectionalRouteMiles, Stops, StopTimes, Routes, Trips, Shapes, CalendarDates, RoutePerformance

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum, Count, Q, F, Avg, Value
import folium
from django.db.models.functions import Round
from app.settings import DEBUG
import datetime
from dateutil import tz
import requests
import json
# from shapely.geometry import LineString

"""
HI it's ben, the amateurish developer!

this file is going to cointain a lot of views which return timeseries data, all for different key performance and expenditure metrics for public transit. 
They're all going to take the same parameters
Think of it as "one endpoint per chart"

"""

# Create your views here.

def save_crash(incident):
    crash_id = incident['crash_id']
    crash_fatal_fl = False
    if "crash_fatal_fl" in incident and incident['crash_fatal_fl'] == "Y":
        crash_fatal_fl = True
    crash_date = incident['crash_date']
    case_id = None
    if "case_id" in incident:
        case_id = incident['case_id']
    rpt_latitude = None
    if "rpt_latitude" in incident:
        rpt_latitude = float(incident['rpt_latitude'])
    rpt_longitude = None
    if "rpt_longitude" in incident:
        rpt_longitude = float(incident['rpt_longitude'])
    rpt_block_num = None
    if "rpt_block_num" in incident:
        rpt_block_num = incident['rpt_block_num']
    rpt_street_pfx = None
    if "rpt_street_pfx" in incident:
        rpt_street_pfx = incident['rpt_street_pfx']
    rpt_street_name = None
    if "rpt_street_name" in incident:
        rpt_street_name = incident['rpt_street_name']
    rpt_street_sfx = None
    if "rpt_street_sfx" in incident:
        rpt_street_sfx = incident['rpt_street_sfx']
    crash_speed_limit = None
    if "crash_speed_limit" in incident:
        crash_speed_limit = incident['crash_speed_limit']
    road_constr_zone_fl = False
    if "road_constr_zone_fl" in incident and incident['road_constr_zone_fl'] == "Y":
        road_constr_zone_fl = True
    latitude = None
    if "latitude" in incident:
        latitude = float(incident['latitude'])
    longitude = None
    if "longitude" in incident:
        longitude = float(incident['longitude'])
    street_name = None
    if "street_name" in incident:
        street_name = incident['street_name']
    street_nbr = None
    if "street_nbr" in incident:
        street_nbr = incident['street_nbr']
    street_name_2 = None
    if "street_name_2" in incident:
        street_name_2 = incident['street_name_2']
    street_nbr_2 = None
    if "street_nbr_2" in incident:
        street_nbr_2 = incident['street_nbr_2']
    crash_sev_id = None
    if "crash_sev_id" in incident:
        crash_sev_id = int(incident['crash_sev_id'])
    # sus_serious_injry_cnt
    sus_serious_injry_cnt = 0
    if "sus_serious_injry_cnt" in incident:
        sus_serious_injry_cnt = int(incident['sus_serious_injry_cnt'])
    # nonincap_injry_cnt
    nonincap_injry_cnt = 0
    if "nonincap_injry_cnt" in incident:
        nonincap_injry_cnt = int(incident['nonincap_injry_cnt'])
    # poss_injry_cnt
    poss_injry_cnt = 0
    if "poss_injry_cnt" in incident:
        poss_injry_cnt = int(incident['poss_injry_cnt'])
    # non_injry_cnt
    non_injry_cnt = 0
    if "non_injry_cnt" in incident:
        non_injry_cnt = int(incident['non_injry_cnt'])
    # unkn_injry_cnt
    unkn_injry_cnt = 0
    if "unkn_injry_cnt" in incident:
        unkn_injry_cnt = int(incident['unkn_injry_cnt'])
    # tot_injry_cnt
    tot_injry_cnt = 0
    if "tot_injry_cnt" in incident:
        tot_injry_cnt = int(incident['tot_injry_cnt'])
    # death_cnt
    death_cnt = 0
    if "death_cnt" in incident:
        death_cnt = int(incident['death_cnt'])
    # contrib_factr_p1_id
    contrib_factr_p1_id = None
    if "contrib_factr_p1_id" in incident:
        contrib_factr_p1_id = int(incident['contrib_factr_p1_id'])
    # contrib_factr_p2_id
    contrib_factr_p2_id = None
    if "contrib_factr_p2_id" in incident:
        contrib_factr_p2_id = int(incident['contrib_factr_p2_id'])
    # units_involved
    units_involved = None
    if "units_involved" in incident:
        units_involved = incident['units_involved']

    # atd_mode_category_metadata
    atd_mode_category_metadata = None
    if "atd_mode_category_metadata" in incident:
        atd_mode_category_metadata = incident['atd_mode_category_metadata']
    
    # pedestrian_fl
    pedestrian_fl = False
    if "pedestrian_fl" in incident and incident['pedestrian_fl'] == "Y":
        pedestrian_fl = True
    # motor_vehicle_fl
    motor_vehicle_fl = False
    if "motor_vehicle_fl" in incident and incident['motor_vehicle_fl'] == "Y":
        motor_vehicle_fl = True
    # motorcycle_fl
    motorcycle_fl = False
    if "motorcycle_fl" in incident and incident['motorcycle_fl'] == "Y":
        motorcycle_fl = True
    # bicycle_fl
    bicycle_fl = False
    if "bicycle_fl" in incident and incident['bicycle_fl'] == "Y":
        bicycle_fl = True
    # other_fl
    other_fl = False
    if "other_fl" in incident and incident['other_fl'] == "Y":
        other_fl = True

    # point
    point = None
    if "point" in incident:
        point = incident['point']
    # apd_confirmed_fatality
    apd_confirmed_fatality = False
    if "apd_confirmed_fatality" in incident and incident['apd_confirmed_fatality'] == "Y":
        apd_confirmed_fatality = True

    # apd_confirmed_death_count
    apd_confirmed_death_count = 0
    if "apd_confirmed_death_count" in incident:
        apd_confirmed_death_count = int(incident['apd_confirmed_death_count'])
    # motor_vehicle_death_count
    motor_vehicle_death_count = 0
    if "motor_vehicle_death_count" in incident:
        motor_vehicle_death_count = int(incident['motor_vehicle_death_count'])
    # motor_vehicle_serious_injury_count
    motor_vehicle_serious_injury_count = 0
    if "motor_vehicle_serious_injury_count" in incident:
        motor_vehicle_serious_injury_count = int(incident['motor_vehicle_serious_injury_count'])
    # bicycle_death_count
    bicycle_death_count = 0
    if "bicycle_death_count" in incident:
        bicycle_death_count = int(incident['bicycle_death_count'])
    # bicycle_serious_injury_count
    bicycle_serious_injury_count = 0
    if "bicycle_serious_injury_count" in incident:
        bicycle_serious_injury_count = int(incident['bicycle_serious_injury_count'])
    # pedestrian_death_count
    pedestrian_death_count = 0
    if "pedestrian_death_count" in incident:
        pedestrian_death_count = int(incident['pedestrian_death_count'])
    # pedestrian_serious_injury_count
    pedestrian_serious_injury_count = 0
    if "pedestrian_serious_injury_count" in incident:
        pedestrian_serious_injury_count = int(incident['pedestrian_serious_injury_count'])
    # motorcycle_death_count
    motorcycle_death_count = 0
    if "motorcycle_death_count" in incident:
        motorcycle_death_count = int(incident['motorcycle_death_count'])
    # motorcycle_serious_injury_count
    motorcycle_serious_injury_count = 0
    if "motorcycle_serious_injury_count" in incident:
        motorcycle_serious_injury_count = int(incident['motorcycle_serious_injury_count'])
    # other_death_count
    other_death_count = 0
    if "other_death_count" in incident:
        other_death_count = int(incident['other_death_count'])
    # other_serious_injury_count
    other_serious_injury_count = 0
    if "other_serious_injury_count" in incident:
        other_serious_injury_count = int(incident['other_serious_injury_count'])
    # onsys_fl
    onsys_fl = False
    if "onsys_fl" in incident and incident['onsys_fl'] == "Y":
        onsys_fl = True
    # private_dr_fl 
    private_dr_fl = False
    if "private_dr_fl" in incident and incident['private_dr_fl'] == "Y":
        private_dr_fl = True

    new_crash = Crash(
        crash_id=crash_id,
        crash_fatal_fl=crash_fatal_fl,
        crash_date=crash_date,
        case_id=case_id,
        rpt_latitude=rpt_latitude,
        rpt_longitude=rpt_longitude,
        rpt_block_num=rpt_block_num,
        rpt_street_pfx=rpt_street_pfx,
        rpt_street_name=rpt_street_name,
        rpt_street_sfx=rpt_street_sfx,
        crash_speed_limit=crash_speed_limit,
        road_constr_zone_fl=road_constr_zone_fl,
        latitude=latitude,
        longitude=longitude,
        street_name=street_name,
        street_nbr=street_nbr,
        street_name_2=street_name_2,
        street_nbr_2=street_nbr_2,
        crash_sev_id=crash_sev_id,
        sus_serious_injry_cnt=sus_serious_injry_cnt,
        nonincap_injry_cnt=nonincap_injry_cnt,
        poss_injry_cnt=poss_injry_cnt,
        non_injry_cnt=non_injry_cnt,
        unkn_injry_cnt=unkn_injry_cnt,
        tot_injry_cnt=tot_injry_cnt,
        death_cnt=death_cnt,
        contrib_factr_p1_id=contrib_factr_p1_id,
        contrib_factr_p2_id=contrib_factr_p2_id,
        units_involved=units_involved,
        atd_mode_category_metadata=atd_mode_category_metadata,
        pedestrian_fl=pedestrian_fl,
        motor_vehicle_fl=motor_vehicle_fl,
        motorcycle_fl=motorcycle_fl,
        bicycle_fl=bicycle_fl,
        other_fl=other_fl,
        point=point,
        apd_confirmed_fatality=apd_confirmed_fatality,
        apd_confirmed_death_count=apd_confirmed_death_count,
        motor_vehicle_death_count=motor_vehicle_death_count,
        motor_vehicle_serious_injury_count=motor_vehicle_serious_injury_count,
        bicycle_death_count=bicycle_death_count,
        bicycle_serious_injury_count=bicycle_serious_injury_count,
        pedestrian_death_count=pedestrian_death_count,
        pedestrian_serious_injury_count=pedestrian_serious_injury_count,
        motorcycle_death_count=motorcycle_death_count,
        motorcycle_serious_injury_count=motorcycle_serious_injury_count,
        other_death_count=other_death_count,
        other_serious_injury_count=other_serious_injury_count,
        onsys_fl=onsys_fl,
        private_dr_fl=private_dr_fl
    )
    new_crash.save()
    print(f"SUCCESSFULLY SAVED CRASH_ID {incident['crash_id']}")


def process_params(params):

    filters = {}
    q = Q()

    if "transit_agency_id" in params and params['transit_agency_id']:
        filters['transit_agency_id'] = params['transit_agency_id']
        transit_agency_id_list = params['transit_agency_id'].split(",")
        q &= Q(transit_agency_id=transit_agency_id_list)

    if "mode" in params and params["mode"]:
        filters['mode'] = params["mode"]
        mode_list = params['mode'].split(",")
        q &= Q(mode__in=mode_list)

    if "service" in params and params['service']:
        filters['service'] = params['service']
        service_list = params['service'].split(",")
        q &= Q(service=service_list)

    # if "budget_type" in params:
    #     if params['budget_type'] == "operating":
    #         q &= Q(expense_type_id__in=["VO", "VM", "NVM", "GA"]), 
    #         filters['budget_type'] = "operating"
    #     if params['budget_type'] == "capital":
    #         q &= Q(expense_type_id__in=["RS", "FC", "OC"]),
    #         filters['budget_type'] = "capital"
            
    if "expense_type" in params and params['expense_type']:
        filters['expense_type'] = params['expense_type']
        expense_type_list = params['expense_type'].split(",")
        q &= Q(expense_type_id__in=expense_type_list)
    

    # Filter Fields on the Transit Agency model

    if "ntd_id" in params and params['ntd_id']:
        filters['ntd_id'] = params['ntd_id']
        ntd_id_list = params['ntd_id'].split(",")
        q &= Q(transit_agency_id__ntd_id__in=ntd_id_list)
        
    if "agency" in params and params['agency']:
        filters['agency'] = params['agency']
        id_list = params['agency'].split(",")
        q &= Q(transit_agency_id__in=id_list)

    if "uza" in params and params['uza']:
        filters['uza'] = params['uza']
        uza_id_list = params['uza'].split(",")
        q &= Q(transit_agency_id__uza__in=uza_id_list)

    # if "city" in params and params['city']:
    #     filters['city'] = params['city']
    #     q &= Q(transit_agency_id__city=params['city'])

    if "state" in params and params['state']:
        filters['state'] = params['state']
        state_list = params['state'].split(",")
        q &= Q(transit_agency_id__state__in=state_list)
    
    if "uza_population__gte" in params and params['uza_population__gte']:
        filters['uza_population__gte'] = params['uza_population__gte']
        q &= Q(transit_agency_id__uza_population__gte=params['uza_population__gte'])

    if "uza_population__lte" in params and params['uza_population__lte']:
        filters['uza_population__lte'] = params['uza_population__lte']
        q &= Q(transit_agency_id__uza_population__lte=params['uza_population__lte'])
    
    return filters, q



# SPENDING DASHBOARD API ENDPOINTS

@csrf_exempt
def spending_by_budget(request):

    filters, q = process_params(request.GET)
    ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating"))), \
                                 capexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Capital")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def spending_by_category(request):
    filters, q = process_params(request.GET)
    ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(vehicle_operations=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id="VO"))), \
                                 vehicle_maintenance=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id="VM"))), \
                                 non_vehicle_maintenance=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id="NVM"))), \
                                 general_administration=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id="GA"))), \
                                 rolling_stock=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id="RS"))), \
                                 facilities=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id="FC"))), \
                                 other_capital=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id="OC")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def spending_by_mode_type(request):
    filters, q = process_params(request.GET)
    ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(bus=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id__type="Bus"))), \
                                 rail=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id__type="Rail"))), \
                                 microtransit=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id__type="MicroTransit"))), \
                                 ferry=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id__type="Ferry"))), \
                                 other=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id__type="Other")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def spending_by_mode(request):
    filters, q = process_params(request.GET)
    ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(mb=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="MB"))), \
                                 cb=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="CB"))), \
                                 rb=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="RB"))), \
                                 tb=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="TB"))), \
                                 pb=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="PB"))), \
                                 hr=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="HR"))), \
                                 lr=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="LR"))), \
                                 cr=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="CR"))), \
                                 yr=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="YR"))), \
                                 sr=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="SR"))), \
                                 cc=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="CC"))), \
                                 mg=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="MG"))), \
                                 ip=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="IP"))), \
                                 ar=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="AR"))), \
                                 other_rail=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="OR"))), \
                                 dr=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="DR"))), \
                                 dt=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="DT"))), \
                                 vp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="VP"))), \
                                 jt=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="JT"))), \
                                 fb=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="FB"))), \
                                 tr=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id="TR"))), \
                                 ot=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')

    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def opexp_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(directly_operated=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(service_id="DO"))), \
                                 purchased_transportation=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(service_id="PT"))), \
                                 taxi=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(service_id="TX"))), \
                                 other=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(service_id="OT")))) \
        .order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))


# SERVICE DASHBOARD API ENDPOINTS

@csrf_exempt
def fares(request):
    filters, q = process_params(request.GET)
    ts = Fares.objects.filter(q).values("year").annotate(upt=Round(Sum("fares"))).order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def upt(request):
    filters, q = process_params(request.GET)
    ts = UnlinkedPassengerTrips.objects.filter(q).values("year").annotate(upt=Round(Sum("upt"))).order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def pmt(request):
    filters, q = process_params(request.GET)
    ts = PassengerMilesTraveled.objects.filter(q).values("year").annotate(pmt=Round(Sum("pmt"))).order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def vrm(request):
    filters, q = process_params(request.GET)
    ts = VehicleRevenueMiles.objects.filter(q).values("year").annotate(vrm=Round(Sum("vrm"))).order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def vrh(request):
    filters, q = process_params(request.GET)
    ts = VehicleRevenueHours.objects.filter(q).values("year").annotate(vrh=Round(Sum("vrh"))).order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def drm(request):
    filters, q = process_params(request.GET)
    ts = DirectionalRouteMiles.objects.filter(q).values("year").annotate(drm=Round(Sum("drm"))).order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def voms(request):
    filters, q = process_params(request.GET)
    ts = VehiclesOperatedMaximumService.objects.filter(q).values("year").annotate(voms=Round(Sum("voms"))).order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # return(JsonResponse({}))

@csrf_exempt
def upt_by_mode_type(request):
    filters, q = process_params(request.GET)
    ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(bus=Round(Sum(F('upt'), filter=Q(mode_id__type="Bus"))), \
                                 rail=Round(Sum(F('upt'), filter=Q(mode_id__type="Rail"))), \
                                 microtransit=Round(Sum(F('upt'), filter=Q(mode_id__type="MicroTransit"))), \
                                 ferry=Round(Sum(F('upt'), filter=Q(mode_id__type="Ferry"))), \
                                 other=Round(Sum(F('upt'), filter=Q(mode_id__type="Other")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_by_mode_type(request):
    filters, q = process_params(request.GET)
    ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(bus=Round(Sum(F('pmt'), filter=Q(mode_id__type="Bus"))), \
                                 rail=Round(Sum(F('pmt'), filter=Q(mode_id__type="Rail"))), \
                                 microtransit=Round(Sum(F('pmt'), filter=Q(mode_id__type="MicroTransit"))), \
                                 ferry=Round(Sum(F('pmt'), filter=Q(mode_id__type="Ferry"))), \
                                 other=Round(Sum(F('pmt'), filter=Q(mode_id__type="Other")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def vrm_by_mode_type(request):
    filters, q = process_params(request.GET)
    ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(bus=Round(Sum(F('vrm'), filter=Q(mode_id__type="Bus"))), \
                                 rail=Round(Sum(F('vrm'), filter=Q(mode_id__type="Rail"))), \
                                 microtransit=Round(Sum(F('vrm'), filter=Q(mode_id__type="MicroTransit"))), \
                                 ferry=Round(Sum(F('vrm'), filter=Q(mode_id__type="Ferry"))), \
                                 other=Round(Sum(F('vrm'), filter=Q(mode_id__type="Other")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def vrh_by_mode_type(request):
    filters, q = process_params(request.GET)
    ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(bus=Round(Sum(F('vrh'), filter=Q(mode_id__type="Bus"))), \
                                 rail=Round(Sum(F('vrh'), filter=Q(mode_id__type="Rail"))), \
                                 microtransit=Round(Sum(F('vrh'), filter=Q(mode_id__type="MicroTransit"))), \
                                 ferry=Round(Sum(F('vrh'), filter=Q(mode_id__type="Ferry"))), \
                                 other=Round(Sum(F('vrh'), filter=Q(mode_id__type="Other")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def drm_by_mode_type(request):
    filters, q = process_params(request.GET)
    ts = DirectionalRouteMiles.objects.filter(q)\
        .values("year").annotate(bus=Round(Sum(F('drm'), filter=Q(mode_id__type="Bus"))), \
                                 rail=Round(Sum(F('drm'), filter=Q(mode_id__type="Rail"))), \
                                 microtransit=Round(Sum(F('drm'), filter=Q(mode_id__type="MicroTransit"))), \
                                 ferry=Round(Sum(F('drm'), filter=Q(mode_id__type="Ferry"))), \
                                 other=Round(Sum(F('drm'), filter=Q(mode_id__type="Other")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def voms_by_mode_type(request):
    filters, q = process_params(request.GET)
    ts = VehiclesOperatedMaximumService.objects.filter(q)\
        .values("year").annotate(bus=Round(Sum(F('voms'), filter=Q(mode_id__type="Bus"))), \
                                 rail=Round(Sum(F('voms'), filter=Q(mode_id__type="Rail"))), \
                                 microtransit=Round(Sum(F('voms'), filter=Q(mode_id__type="MicroTransit"))), \
                                 ferry=Round(Sum(F('voms'), filter=Q(mode_id__type="Ferry"))), \
                                 other=Round(Sum(F('voms'), filter=Q(mode_id__type="Other")))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(directly_operated=Round(Sum(F('upt'), filter=Q(service_id="DO"))), \
                                 purchased_transportation=Round(Sum(F('upt'), filter=Q(service_id="PT"))), \
                                 taxi=Round(Sum(F('upt'), filter=Q(service_id="TX"))), \
                                 other=Round(Sum(F('upt'), filter=Q(service_id="OT")))) \
        .order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(directly_operated=Round(Sum(F('pmt'), filter=Q(service_id="DO"))), \
                                 purchased_transportation=Round(Sum(F('pmt'), filter=Q(service_id="PT"))), \
                                 taxi=Round(Sum(F('pmt'), filter=Q(service_id="TX"))), \
                                 other=Round(Sum(F('pmt'), filter=Q(service_id="OT")))) \
        .order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def vrm_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(directly_operated=Round(Sum(F('vrm'), filter=Q(service_id="DO"))), \
                                 purchased_transportation=Round(Sum(F('vrm'), filter=Q(service_id="PT"))), \
                                 taxi=Round(Sum(F('vrm'), filter=Q(service_id="TX"))), \
                                 other=Round(Sum(F('vrm'), filter=Q(service_id="OT")))) \
        .order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def vrh_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(directly_operated=Round(Sum(F('vrh'), filter=Q(service_id="DO"))), \
                                 purchased_transportation=Round(Sum(F('vrh'), filter=Q(service_id="PT"))), \
                                 taxi=Round(Sum(F('vrh'), filter=Q(service_id="TX"))), \
                                 other=Round(Sum(F('vrh'), filter=Q(service_id="OT")))) \
        .order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def drm_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    ts = DirectionalRouteMiles.objects.filter(q)\
        .values("year").annotate(directly_operated=Round(Sum(F('drm'), filter=Q(service_id="DO"))), \
                                 purchased_transportation=Round(Sum(F('drm'), filter=Q(service_id="PT"))), \
                                 taxi=Round(Sum(F('drm'), filter=Q(service_id="TX"))), \
                                 other=Round(Sum(F('drm'), filter=Q(service_id="OT")))) \
        .order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def voms_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    ts = VehiclesOperatedMaximumService.objects.filter(q)\
        .values("year").annotate(directly_operated=Round(Sum(F('voms'), filter=Q(service_id="DO"))), \
                                 purchased_transportation=Round(Sum(F('voms'), filter=Q(service_id="PT"))), \
                                 taxi=Round(Sum(F('voms'), filter=Q(service_id="TX"))), \
                                 other=Round(Sum(F('voms'), filter=Q(service_id="OT")))) \
        .order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_by_mode(request):
    filters, q = process_params(request.GET)
    ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(mb=Round(Sum(F('upt'), filter=Q(mode_id="MB"))), \
                                 cb=Round(Sum(F('upt'), filter=Q(mode_id="CB"))), \
                                 rb=Round(Sum(F('upt'), filter=Q(mode_id="RB"))), \
                                 tb=Round(Sum(F('upt'), filter=Q(mode_id="TB"))), \
                                 pb=Round(Sum(F('upt'), filter=Q(mode_id="PB"))), \
                                 hr=Round(Sum(F('upt'), filter=Q(mode_id="HR"))), \
                                 lr=Round(Sum(F('upt'), filter=Q(mode_id="LR"))), \
                                 cr=Round(Sum(F('upt'), filter=Q(mode_id="CR"))), \
                                 yr=Round(Sum(F('upt'), filter=Q(mode_id="YR"))), \
                                 sr=Round(Sum(F('upt'), filter=Q(mode_id="SR"))), \
                                 cc=Round(Sum(F('upt'), filter=Q(mode_id="CC"))), \
                                 mg=Round(Sum(F('upt'), filter=Q(mode_id="MG"))), \
                                 ip=Round(Sum(F('upt'), filter=Q(mode_id="IP"))), \
                                 ar=Round(Sum(F('upt'), filter=Q(mode_id="AR"))), \
                                 other_rail=Round(Sum(F('upt'), filter=Q(mode_id="OR"))), \
                                 dr=Round(Sum(F('upt'), filter=Q(mode_id="DR"))), \
                                 dt=Round(Sum(F('upt'), filter=Q(mode_id="DT"))), \
                                 vp=Round(Sum(F('upt'), filter=Q(mode_id="VP"))), \
                                 jt=Round(Sum(F('upt'), filter=Q(mode_id="JT"))), \
                                 fb=Round(Sum(F('upt'), filter=Q(mode_id="FB"))), \
                                 tr=Round(Sum(F('upt'), filter=Q(mode_id="TR"))), \
                                 ot=Round(Sum(F('upt'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_by_mode(request):
    filters, q = process_params(request.GET)
    ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(mb=Round(Sum(F('pmt'), filter=Q(mode_id="MB"))), \
                                 cb=Round(Sum(F('pmt'), filter=Q(mode_id="CB"))), \
                                 rb=Round(Sum(F('pmt'), filter=Q(mode_id="RB"))), \
                                 tb=Round(Sum(F('pmt'), filter=Q(mode_id="TB"))), \
                                 pb=Round(Sum(F('pmt'), filter=Q(mode_id="PB"))), \
                                 hr=Round(Sum(F('pmt'), filter=Q(mode_id="HR"))), \
                                 lr=Round(Sum(F('pmt'), filter=Q(mode_id="LR"))), \
                                 cr=Round(Sum(F('pmt'), filter=Q(mode_id="CR"))), \
                                 yr=Round(Sum(F('pmt'), filter=Q(mode_id="YR"))), \
                                 sr=Round(Sum(F('pmt'), filter=Q(mode_id="SR"))), \
                                 cc=Round(Sum(F('pmt'), filter=Q(mode_id="CC"))), \
                                 mg=Round(Sum(F('pmt'), filter=Q(mode_id="MG"))), \
                                 ip=Round(Sum(F('pmt'), filter=Q(mode_id="IP"))), \
                                 ar=Round(Sum(F('pmt'), filter=Q(mode_id="AR"))), \
                                 other_rail=Round(Sum(F('pmt'), filter=Q(mode_id="OR"))), \
                                 dr=Round(Sum(F('pmt'), filter=Q(mode_id="DR"))), \
                                 dt=Round(Sum(F('pmt'), filter=Q(mode_id="DT"))), \
                                 vp=Round(Sum(F('pmt'), filter=Q(mode_id="VP"))), \
                                 jt=Round(Sum(F('pmt'), filter=Q(mode_id="JT"))), \
                                 fb=Round(Sum(F('pmt'), filter=Q(mode_id="FB"))), \
                                 tr=Round(Sum(F('pmt'), filter=Q(mode_id="TR"))), \
                                 ot=Round(Sum(F('pmt'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def vrm_by_mode(request):
    filters, q = process_params(request.GET)
    ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(mb=Round(Sum(F('vrm'), filter=Q(mode_id="MB"))), \
                                 cb=Round(Sum(F('vrm'), filter=Q(mode_id="CB"))), \
                                 rb=Round(Sum(F('vrm'), filter=Q(mode_id="RB"))), \
                                 tb=Round(Sum(F('vrm'), filter=Q(mode_id="TB"))), \
                                 pb=Round(Sum(F('vrm'), filter=Q(mode_id="PB"))), \
                                 hr=Round(Sum(F('vrm'), filter=Q(mode_id="HR"))), \
                                 lr=Round(Sum(F('vrm'), filter=Q(mode_id="LR"))), \
                                 cr=Round(Sum(F('vrm'), filter=Q(mode_id="CR"))), \
                                 yr=Round(Sum(F('vrm'), filter=Q(mode_id="YR"))), \
                                 sr=Round(Sum(F('vrm'), filter=Q(mode_id="SR"))), \
                                 cc=Round(Sum(F('vrm'), filter=Q(mode_id="CC"))), \
                                 mg=Round(Sum(F('vrm'), filter=Q(mode_id="MG"))), \
                                 ip=Round(Sum(F('vrm'), filter=Q(mode_id="IP"))), \
                                 ar=Round(Sum(F('vrm'), filter=Q(mode_id="AR"))), \
                                 other_rail=Round(Sum(F('vrm'), filter=Q(mode_id="OR"))), \
                                 dr=Round(Sum(F('vrm'), filter=Q(mode_id="DR"))), \
                                 dt=Round(Sum(F('vrm'), filter=Q(mode_id="DT"))), \
                                 vp=Round(Sum(F('vrm'), filter=Q(mode_id="VP"))), \
                                 jt=Round(Sum(F('vrm'), filter=Q(mode_id="JT"))), \
                                 fb=Round(Sum(F('vrm'), filter=Q(mode_id="FB"))), \
                                 tr=Round(Sum(F('vrm'), filter=Q(mode_id="TR"))), \
                                 ot=Round(Sum(F('vrm'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def vrh_by_mode(request):
    filters, q = process_params(request.GET)
    ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(mb=Round(Sum(F('vrh'), filter=Q(mode_id="MB"))), \
                                 cb=Round(Sum(F('vrh'), filter=Q(mode_id="CB"))), \
                                 rb=Round(Sum(F('vrh'), filter=Q(mode_id="RB"))), \
                                 tb=Round(Sum(F('vrh'), filter=Q(mode_id="TB"))), \
                                 pb=Round(Sum(F('vrh'), filter=Q(mode_id="PB"))), \
                                 hr=Round(Sum(F('vrh'), filter=Q(mode_id="HR"))), \
                                 lr=Round(Sum(F('vrh'), filter=Q(mode_id="LR"))), \
                                 cr=Round(Sum(F('vrh'), filter=Q(mode_id="CR"))), \
                                 yr=Round(Sum(F('vrh'), filter=Q(mode_id="YR"))), \
                                 sr=Round(Sum(F('vrh'), filter=Q(mode_id="SR"))), \
                                 cc=Round(Sum(F('vrh'), filter=Q(mode_id="CC"))), \
                                 mg=Round(Sum(F('vrh'), filter=Q(mode_id="MG"))), \
                                 ip=Round(Sum(F('vrh'), filter=Q(mode_id="IP"))), \
                                 ar=Round(Sum(F('vrh'), filter=Q(mode_id="AR"))), \
                                 other_rail=Round(Sum(F('vrh'), filter=Q(mode_id="OR"))), \
                                 dr=Round(Sum(F('vrh'), filter=Q(mode_id="DR"))), \
                                 dt=Round(Sum(F('vrh'), filter=Q(mode_id="DT"))), \
                                 vp=Round(Sum(F('vrh'), filter=Q(mode_id="VP"))), \
                                 jt=Round(Sum(F('vrh'), filter=Q(mode_id="JT"))), \
                                 fb=Round(Sum(F('vrh'), filter=Q(mode_id="FB"))), \
                                 tr=Round(Sum(F('vrh'), filter=Q(mode_id="TR"))), \
                                 ot=Round(Sum(F('vrh'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def drm_by_mode(request):
    filters, q = process_params(request.GET)
    ts = DirectionalRouteMiles.objects.filter(q)\
        .values("year").annotate(mb=Round(Sum(F('drm'), filter=Q(mode_id="MB"))), \
                                 cb=Round(Sum(F('drm'), filter=Q(mode_id="CB"))), \
                                 rb=Round(Sum(F('drm'), filter=Q(mode_id="RB"))), \
                                 tb=Round(Sum(F('drm'), filter=Q(mode_id="TB"))), \
                                 pb=Round(Sum(F('drm'), filter=Q(mode_id="PB"))), \
                                 hr=Round(Sum(F('drm'), filter=Q(mode_id="HR"))), \
                                 lr=Round(Sum(F('drm'), filter=Q(mode_id="LR"))), \
                                 cr=Round(Sum(F('drm'), filter=Q(mode_id="CR"))), \
                                 yr=Round(Sum(F('drm'), filter=Q(mode_id="YR"))), \
                                 sr=Round(Sum(F('drm'), filter=Q(mode_id="SR"))), \
                                 cc=Round(Sum(F('drm'), filter=Q(mode_id="CC"))), \
                                 mg=Round(Sum(F('drm'), filter=Q(mode_id="MG"))), \
                                 ip=Round(Sum(F('drm'), filter=Q(mode_id="IP"))), \
                                 ar=Round(Sum(F('drm'), filter=Q(mode_id="AR"))), \
                                 other_rail=Round(Sum(F('drm'), filter=Q(mode_id="OR"))), \
                                 dr=Round(Sum(F('drm'), filter=Q(mode_id="DR"))), \
                                 dt=Round(Sum(F('drm'), filter=Q(mode_id="DT"))), \
                                 vp=Round(Sum(F('drm'), filter=Q(mode_id="VP"))), \
                                 jt=Round(Sum(F('drm'), filter=Q(mode_id="JT"))), \
                                 fb=Round(Sum(F('drm'), filter=Q(mode_id="FB"))), \
                                 tr=Round(Sum(F('drm'), filter=Q(mode_id="TR"))), \
                                 ot=Round(Sum(F('drm'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def voms_by_mode(request):
    filters, q = process_params(request.GET)
    ts = VehiclesOperatedMaximumService.objects.filter(q)\
        .values("year").annotate(mb=Round(Sum(F('voms'), filter=Q(mode_id="MB"))), \
                                 cb=Round(Sum(F('voms'), filter=Q(mode_id="CB"))), \
                                 rb=Round(Sum(F('voms'), filter=Q(mode_id="RB"))), \
                                 tb=Round(Sum(F('voms'), filter=Q(mode_id="TB"))), \
                                 pb=Round(Sum(F('voms'), filter=Q(mode_id="PB"))), \
                                 hr=Round(Sum(F('voms'), filter=Q(mode_id="HR"))), \
                                 lr=Round(Sum(F('voms'), filter=Q(mode_id="LR"))), \
                                 cr=Round(Sum(F('voms'), filter=Q(mode_id="CR"))), \
                                 yr=Round(Sum(F('voms'), filter=Q(mode_id="YR"))), \
                                 sr=Round(Sum(F('voms'), filter=Q(mode_id="SR"))), \
                                 cc=Round(Sum(F('voms'), filter=Q(mode_id="CC"))), \
                                 mg=Round(Sum(F('voms'), filter=Q(mode_id="MG"))), \
                                 ip=Round(Sum(F('voms'), filter=Q(mode_id="IP"))), \
                                 ar=Round(Sum(F('voms'), filter=Q(mode_id="AR"))), \
                                 other_rail=Round(Sum(F('voms'), filter=Q(mode_id="OR"))), \
                                 dr=Round(Sum(F('voms'), filter=Q(mode_id="DR"))), \
                                 dt=Round(Sum(F('voms'), filter=Q(mode_id="DT"))), \
                                 vp=Round(Sum(F('voms'), filter=Q(mode_id="VP"))), \
                                 jt=Round(Sum(F('voms'), filter=Q(mode_id="JT"))), \
                                 fb=Round(Sum(F('voms'), filter=Q(mode_id="FB"))), \
                                 tr=Round(Sum(F('voms'), filter=Q(mode_id="TR"))), \
                                 ot=Round(Sum(F('voms'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in ts:
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)





# PERFORMANCE DASHBOARD APIS

@csrf_exempt
def cost_per_upt(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating")))\
        .order_by('year')
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(upt=Round(Sum("upt"))).order_by('year')
    data = []
    for x in spending_ts:
        cost = x['opexp']
        riders = upt_ts.get(year=x['year'])['upt']
        if riders == 0:
            cost_per_upt = 0
        else:
            cost_per_upt = round(cost/riders, 2)
        data += [{"year": x['year'], "cost_per_upt": cost_per_upt}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def cost_per_pmt(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating")))\
        .order_by('year')
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(pmt=Round(Sum("pmt"))).order_by('year')
    data = []
    for x in spending_ts:
        cost = x['opexp']
        riders = pmt_ts.get(year=x['year'])['pmt']
        if riders == 0:
            riders=1
        cost_per_pmt = round(cost/riders, 2)
        data += [{"year": x['year'], "cost_per_pmt": cost_per_pmt}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def frr(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating")))\
        .order_by('year')
    fares_ts = Fares.objects.filter(q)\
        .values("year").annotate(fares=Sum(F('fares')))\
        .order_by('year')
    data = []
    for x in spending_ts:
        cost = x['opexp']
        revenue = fares_ts.get(year=x['year'])['fares']
        if cost == 0:
            cost = 1
        frr = round(revenue/cost, 4)
        data += [{"year": x['year'], "frr": frr}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def cost_per_vrh(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating")))\
        .order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(vrh=Round(Sum("vrh"))).order_by('year')
    data = []
    for x in spending_ts:
        cost = x['opexp']
        riders = vrh_ts.get(year=x['year'])['vrh']
        if riders == 0:
            riders=1
        cost_per_vrh = round(cost/riders, 2)
        data += [{"year": x['year'], "cost_per_vrh": cost_per_vrh}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def cost_per_vrm(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating")))\
        .order_by('year')
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(vrm=Round(Sum("vrm"))).order_by('year')
    data = []
    for x in spending_ts:
        cost = x['opexp']
        riders = vrm_ts.get(year=x['year'])['vrm']
        if riders == 0:
            riders=1
        cost_per_vrm = round(cost/riders, 2)
        data += [{"year": x['year'], "cost_per_vrm": cost_per_vrm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def vrm_per_vrh(request):
    filters, q = process_params(request.GET)
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(vrm=Sum("vrm")).order_by("year")
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(vrh=Sum("vrh")).order_by("year")
    data = []
    for x in vrm_ts:
        vrm = x['vrm']
        vrh = vrh_ts.get(year=x['year'])['vrh']
        if vrh == 0:
            vrh = 1
        vrm_per_vrh = round(vrm/vrh,2)
        data += [{"year": x['year'], "vrm_per_vrh": vrm_per_vrh}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)


@csrf_exempt
def upt_per_vrh(request):
    filters, q = process_params(request.GET)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(upt=Sum("upt")).order_by("year")
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(vrh=Sum("vrh")).order_by("year")
    data = []
    for x in upt_ts:
        upt = x['upt']
        vrh = vrh_ts.get(year=x['year'])['vrh']
        if vrh == 0:
            vrh = 1
        upt_per_vrh = round(upt/vrh,2)
        data += [{"year": x['year'], "upt_per_vrh": upt_per_vrh}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_per_vrm(request):
    filters, q = process_params(request.GET)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(upt=Sum("upt")).order_by("year")
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(vrm=Sum("vrm")).order_by("year")
    data = []
    for x in upt_ts:
        upt = x['upt']
        vrm = vrm_ts.get(year=x['year'])['vrm']
        if vrm == 0:
            vrm = 1
        upt_per_vrm = round(upt/vrm,2)
        data += [{"year": x['year'], "upt_per_vrm": upt_per_vrm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_per_vrh(request):
    filters, q = process_params(request.GET)
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(pmt=Sum("pmt")).order_by("year")
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(vrh=Sum("vrh")).order_by("year")
    data = []
    for x in pmt_ts:
        pmt = x['pmt']
        vrh = vrh_ts.get(year=x['year'])['vrh']
        if vrh == 0:
            vrh = 1
        pmt_per_vrh = round(pmt/vrh,2)
        data += [{"year": x['year'], "pmt_per_vrh": pmt_per_vrh}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_per_vrm(request):
    filters, q = process_params(request.GET)
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(pmt=Sum("pmt")).order_by("year")
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(vrm=Sum("vrm")).order_by("year")
    data = []
    for x in pmt_ts:
        pmt = x['pmt']
        vrm = vrm_ts.get(year=x['year'])['vrm']
        if vrm == 0:
            vrm = 1
        pmt_per_vrm = round(pmt/vrm,2)
        data += [{"year": x['year'], "pmt_per_vrm": pmt_per_vrm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)





@csrf_exempt
def cost_per_upt_by_mode_type(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(
            bus_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="Bus")),
            rail_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="Rail")),
            microtransit_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="MicroTransit")),
            ferry_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="Ferry")),
            other_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="Other"))
        )\
        .order_by('year')
    print(spending_ts.query)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(
            bus_upt=Sum(F("upt"), filter=Q(mode_id__type="Bus")),
            rail_upt=Sum(F("upt"), filter=Q(mode_id__type="Rail")),
            microtransit_upt=Sum(F("upt"), filter=Q(mode_id__type="MicroTransit")),
            ferry_upt=Sum(F("upt"), filter=Q(mode_id__type="Ferry")),
            other_upt=Sum(F("upt"), filter=Q(mode_id__type="Other"))
        ).order_by('year')
    print(upt_ts.query)
    data = []
    for x in spending_ts:

        ridership = upt_ts.get(year=x['year'])

        if ridership['bus_upt'] and ridership['bus_upt'] > 0 and x['bus_opexp'] and x['bus_opexp'] > 0:
            bus_upt = ridership['bus_upt']
            bus_opexp = x['bus_opexp']
            bus_cpp = round(bus_opexp/bus_upt, 2)
        else:
            bus_cpp = 0
        if ridership['rail_upt'] and ridership['rail_upt'] > 0 and x['rail_opexp'] and x['rail_opexp'] > 0:
            rail_upt = ridership['rail_upt']
            rail_opexp = x['rail_opexp']
            rail_cpp = round(rail_opexp/rail_upt, 2)
        else:
            rail_cpp = 0
        if ridership['microtransit_upt'] and ridership['microtransit_upt'] > 0 and x['microtransit_opexp'] and x['microtransit_opexp'] > 0:
            microtransit_upt = ridership['microtransit_upt']
            microtransit_opexp = x['microtransit_opexp']
            microtransit_cpp = round(microtransit_opexp/microtransit_upt, 2)
        else:
            microtransit_cpp = 0
        if ridership['ferry_upt'] and ridership['ferry_upt'] > 0 and x['ferry_opexp'] and x['ferry_opexp'] > 0:
            ferry_opexp = x['ferry_opexp']
            ferry_upt = ridership['ferry_upt']
            ferry_cpp = round(ferry_opexp/ferry_upt, 2)
        else:
            ferry_cpp = 0
        if ridership['other_upt'] and ridership['other_upt'] > 0 and x['other_opexp'] and x['other_opexp'] > 0:
            other_upt = ridership['other_upt']
            other_opexp = x['other_opexp']
            other_cpp = round(other_opexp/other_upt, 2)
        else:
            other_cpp = 0

        data += [{"year": x['year'], "bus": bus_cpp, "rail": rail_cpp, "microtransit": microtransit_cpp, "ferry": ferry_cpp, "other": other_cpp}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def cost_per_pmt_by_mode_type(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(
            bus_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="Bus")),
            rail_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="Rail")),
            microtransit_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="MicroTransit")),
            ferry_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="Ferry")),
            other_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__type="Other"))
        )\
        .order_by('year')
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(
            bus_pmt=Sum(F("pmt"), filter=Q(mode_id__type="Bus")),
            rail_pmt=Sum(F("pmt"), filter=Q(mode_id__type="Rail")),
            microtransit_pmt=Sum(F("pmt"), filter=Q(mode_id__type="MicroTransit")),
            ferry_pmt=Sum(F("pmt"), filter=Q(mode_id__type="Ferry")),
            other_pmt=Sum(F("pmt"), filter=Q(mode_id__type="Other"))
        ).order_by('year')
    data = []
    for x in spending_ts:
        
        ridership = pmt_ts.get(year=x['year'])

        if ridership['bus_pmt'] and ridership['bus_pmt'] > 0 and x['bus_opexp'] and x['bus_opexp'] > 0:
            bus_pmt = ridership['bus_pmt']
            bus_opexp = x['bus_opexp']
            bus_cpp = round(bus_opexp/bus_pmt, 2)
        else:
            bus_cpp = 0

        if ridership['rail_pmt'] and ridership['rail_pmt'] > 0 and x['rail_opexp'] and x['rail_opexp'] > 0:
            rail_pmt = ridership['rail_pmt']
            rail_opexp = x['rail_opexp']
            rail_cpp = round(rail_opexp/rail_pmt, 2)
        else:
            rail_cpp = 0
            
        if ridership['microtransit_pmt'] and ridership['microtransit_pmt'] > 0 and x['microtransit_opexp'] and x['microtransit_opexp'] > 0:
            microtransit_pmt = ridership['microtransit_pmt']
            microtransit_opexp = x['microtransit_opexp']
            microtransit_cpp = round(microtransit_opexp/microtransit_pmt, 2)
        else:
            microtransit_cpp = 0

        if ridership['ferry_pmt'] and ridership['ferry_pmt'] > 0 and x['ferry_opexp'] and x['ferry_opexp'] > 0:
            ferry_pmt = ridership['ferry_pmt']
            ferry_opexp = x['ferry_opexp']
            ferry_cpp = round(ferry_opexp/ferry_pmt, 2)
        else:
            ferry_cpp = 0

        if ridership['other_pmt'] and ridership['other_pmt'] > 0 and x['other_opexp'] and x['other_opexp'] > 0:
            other_pmt = ridership['other_pmt']
            other_opexp = x['other_opexp']
            other_cpp = round(other_opexp/other_pmt, 2)
        else:
            other_cpp = 0

        data += [{"year": x['year'], "bus": bus_cpp, "rail": rail_cpp, "microtransit": microtransit_cpp, "ferry": ferry_cpp, "other": other_cpp}]
        
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def frr_by_mode_type(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(
            bus_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id__type="Bus")),
            rail_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id__type="Rail")),
            microtransit_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id__type="MicroTransit")),
            ferry_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id__type="Ferry")),
            other_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id__type="Other"))
        )\
        .order_by('year')
    fares_ts = Fares.objects.filter(q)\
        .values("year").annotate(
            bus_fares=Sum(F('fares'), filter=Q(mode_id__type="Bus")),
            rail_fares=Sum(F('fares'), filter=Q(mode_id__type="Rail")),
            microtransit_fares=Sum(F('fares'), filter=Q(mode_id__type="MicroTransit")),
            ferry_fares=Sum(F('fares'), filter=Q(mode_id__type="Ferry")),
            other_fares=Sum(F('fares'), filter=Q(mode_id__type="Other")),
        )\
        .order_by('year')
    data = []
    for x in spending_ts:
        revenue = fares_ts.get(year=x['year'])
        if x['bus_opexp'] and x['bus_opexp'] > 0 and revenue['bus_fares'] and revenue['bus_fares'] > 0:
            bus_opexp = x['bus_opexp']
            bus_fares=revenue['bus_fares']
            bus_frr = round(bus_fares/bus_opexp, 4)
        else:
            bus_frr = 0

        if x['rail_opexp'] and x['rail_opexp'] > 0 and revenue['rail_fares'] and revenue['rail_fares'] > 0:
            rail_opexp = x['rail_opexp']
            rail_fares=revenue['rail_fares']
            rail_frr = round(rail_fares/rail_opexp, 4)
        else: 
            rail_frr = 0

        if x['microtransit_opexp'] and x['microtransit_opexp'] > 0 and revenue['microtransit_fares'] and revenue['microtransit_fares'] > 0:
            microtransit_opexp = x['microtransit_opexp']
            microtransit_fares=revenue['microtransit_fares']
            microtransit_frr = round(microtransit_fares/microtransit_opexp, 4)
        else: 
            microtransit_frr = 0

        if x['ferry_opexp'] and x['ferry_opexp'] > 0 and revenue['ferry_fares'] and revenue['ferry_fares'] > 0:
            ferry_opexp = x['ferry_opexp']
            ferry_fares=revenue['ferry_fares']
            ferry_frr = round(ferry_fares/ferry_opexp, 4)
        else: 
            ferry_frr = 0

        if x['other_opexp'] and x['other_opexp'] > 0 and revenue['other_fares'] and revenue['other_fares'] > 0:
            other_opexp = x['other_opexp']
            other_fares=revenue['other_fares']
            other_frr = round(other_fares/other_opexp, 4)
        else: 
            other_frr = 0

        data += [{"year": x['year'], "bus": bus_frr, "rail": rail_frr, "microtransit": microtransit_frr, "ferry": ferry_frr, "other": other_frr}]

    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

# @csrf_exempt
# def cost_per_vrh_by_mode_type(request):
#     return(JsonResponse({}))

# @csrf_exempt
# def cost_per_vrm_by_mode_type(request):
#     return(JsonResponse({}))

@csrf_exempt
def vrm_per_vrh_by_mode_type(request):
    data = []
    filters, q = process_params(request.GET)
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('vrm'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('vrm'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('vrm'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('vrm'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('vrm'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('vrh'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('vrh'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('vrh'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('vrh'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('vrh'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    for x in vrh_ts:
        vrm = vrm_ts.get(year=x['year'])

        if x['bus'] and x["bus"] > 0 and vrm['bus'] and vrm['bus'] > 0:
            bus_vrh = x['bus']
            bus_vrm = vrm['bus']
            bus_mph = round(bus_vrm / bus_vrh, 2)
        else:
            bus_mph = 0

        if x['rail'] and x["rail"] > 0 and vrm['rail'] and vrm['rail'] > 0:
            rail_vrh = x['rail']
            rail_vrm = vrm['rail']
            rail_mph = round(rail_vrm / rail_vrh, 2)
        else:
            rail_mph = 0

        if x['microtransit'] and x["microtransit"] > 0 and vrm['microtransit'] and vrm['microtransit'] > 0:
            microtransit_vrh = x['microtransit']
            microtransit_vrm = vrm['microtransit']
            microtransit_mph = round(microtransit_vrm / microtransit_vrh, 2)
        else:
            microtransit_mph = 0
        if x['ferry'] and x["ferry"] > 0 and vrm['ferry'] and vrm['ferry'] > 0:
            ferry_vrh = x['ferry']
            ferry_vrm = vrm['ferry']
            ferry_mph = round(ferry_vrm / ferry_vrh, 2)
        else:
            ferry_mph = 0
        if x['other'] and x["other"] > 0 and vrm['other'] and vrm['other'] > 0:
            other_vrh = x['other']
            other_vrm = vrm['other']
            other_mph = round(other_vrm / other_vrh, 2)
        else:
            other_mph = 0
        
        data += [{"year": x['year'], "bus": bus_mph, "rail": rail_mph, "microtransit": microtransit_mph, "ferry": ferry_mph, "other": other_mph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_per_vrh_by_mode_type(request):
    data = []
    filters, q = process_params(request.GET)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('upt'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('upt'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('upt'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('upt'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('upt'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('vrh'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('vrh'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('vrh'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('vrh'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('vrh'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    for x in vrh_ts:
        upt = upt_ts.get(year=x['year'])

        if x['bus'] and x["bus"] > 0 and upt['bus'] and upt['bus'] > 0:
            bus_vrh = x['bus']
            bus_upt = upt['bus']
            bus_pph = round(bus_upt / bus_vrh, 2)
        else:
            bus_pph = 0
        if x['rail'] and x["rail"] > 0 and upt['rail'] and upt['rail'] > 0:
            rail_vrh = x['rail']
            rail_upt = upt['rail']
            rail_pph = round(rail_upt / rail_vrh, 2)
        else:
            rail_pph = 0
        if x['microtransit'] and x["microtransit"] > 0 and upt['microtransit'] and upt['microtransit'] > 0:
            microtransit_vrh = x['microtransit']
            microtransit_upt = upt['microtransit']
            microtransit_pph = round(microtransit_upt / microtransit_vrh, 2)
        else:
            microtransit_pph = 0
        if x['ferry'] and x["ferry"] > 0 and upt['ferry'] and upt['ferry'] > 0:
            ferry_vrh = x['ferry']
            ferry_upt = upt['ferry']
            ferry_pph = round(ferry_upt / ferry_vrh, 2)
        else:
            ferry_pph = 0
        if x['other'] and x["other"] > 0 and upt['other'] and upt['other'] > 0:
            other_vrh = x['other']
            other_upt = upt['other']
            other_pph = round(other_upt / other_vrh, 2)
        else:
            other_pph = 0

        data += [{"year": x['year'], "bus": bus_pph, "rail": rail_pph, "microtransit": microtransit_pph, "ferry": ferry_pph, "other": other_pph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_per_vrm_by_mode_type(request):
    data = []
    filters, q = process_params(request.GET)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('upt'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('upt'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('upt'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('upt'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('upt'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('vrm'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('vrm'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('vrm'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('vrm'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('vrm'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    for x in vrm_ts:
        upt = upt_ts.get(year=x['year'])
        if x['bus'] and x["bus"] > 0 and upt['bus'] and upt['bus'] > 0:
            bus_vrm = x['bus']
            bus_upt = upt['bus']
            bus_ppm = round(bus_upt / bus_vrm, 2)
        else:
            bus_ppm = 0
        if x['rail'] and x["rail"] > 0 and upt['rail'] and upt['rail'] > 0:
            rail_vrm = x['rail']
            rail_upt = upt['rail']
            rail_ppm = round(rail_upt / rail_vrm, 2)
        else:
            rail_ppm = 0
        if x['microtransit'] and x["microtransit"] > 0 and upt['microtransit'] and upt['microtransit'] > 0:
            microtransit_vrm = x['microtransit']
            microtransit_upt = upt['microtransit']
            microtransit_ppm = round(microtransit_upt / microtransit_vrm, 2)
        else:
            microtransit_ppm = 0
        if x['ferry'] and x["ferry"] > 0 and upt['ferry'] and upt['ferry'] > 0:
            ferry_vrm = x['ferry']
            ferry_upt = upt['ferry']
            ferry_ppm = round(ferry_upt / ferry_vrm, 2)
        else:
            ferry_ppm = 0
        if x['other'] and x["other"] > 0 and upt['other'] and upt['other'] > 0:
            other_vrm = x['other']
            other_upt = upt['other']
            other_ppm = round(other_upt / other_vrm, 2)
        else:
            other_ppm = 0
            
        data += [{"year": x['year'], "bus": bus_ppm, "rail": rail_ppm, "microtransit": microtransit_ppm, "ferry": ferry_ppm, "other": other_ppm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_per_vrh_by_mode_type(request):
    data = []
    filters, q = process_params(request.GET)
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('pmt'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('pmt'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('pmt'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('pmt'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('pmt'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('vrh'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('vrh'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('vrh'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('vrh'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('vrh'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    for x in vrh_ts:
        pmt = pmt_ts.get(year=x['year'])
        if x['bus'] and x["bus"] > 0 and pmt['bus'] and pmt['bus'] > 0:
            bus_vrh = x['bus']
            bus_pmt = pmt['bus']
            bus_pmph = round(bus_pmt / bus_vrh, 2)
        else:
            bus_pmph = 0
        if x['rail'] and x["rail"] > 0 and pmt['rail'] and pmt['rail'] > 0:
            rail_vrh = x['rail']
            rail_pmt = pmt['rail']
            rail_pmph = round(rail_pmt / rail_vrh, 2)
        else:
            rail_pmph = 0
        if x['microtransit'] and x["microtransit"] > 0 and pmt['microtransit'] and pmt['microtransit'] > 0:
            microtransit_vrh = x['microtransit']
            microtransit_pmt = pmt['microtransit']
            microtransit_pmph = round(microtransit_pmt / microtransit_vrh, 2)
        else:
            microtransit_pmph =0
        if x['ferry'] and x["ferry"] > 0 and pmt['ferry'] and pmt['ferry'] > 0:
            ferry_vrh = x['ferry']
            ferry_pmt = pmt['ferry']
            ferry_pmph = round(ferry_pmt / ferry_vrh, 2)
        else:
            ferry_pmph = 0
        if x['other'] and x["other"] > 0 and pmt['other'] and pmt['other'] > 0:
            other_vrh = x['other']
            other_pmt = pmt['other']
            other_pmph = round(other_pmt / other_vrh, 2)
        else:
            other_pmph = 0
        
        data += [{"year": x['year'], "bus": bus_pmph, "rail": rail_pmph, "microtransit": microtransit_pmph, "ferry": ferry_pmph, "other": other_pmph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_per_vrm_by_mode_type(request):
    data = []
    filters, q = process_params(request.GET)
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('pmt'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('pmt'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('pmt'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('pmt'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('pmt'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
    .values("year").annotate(
        bus=Sum(F('vrm'), filter=Q(mode_id__type="Bus")),
        rail=Sum(F('vrm'), filter=Q(mode_id__type="Rail")),
        microtransit=Sum(F('vrm'), filter=Q(mode_id__type="MicroTransit")),
        ferry=Sum(F('vrm'), filter=Q(mode_id__type="Ferry")),
        other=Sum(F('vrm'), filter=Q(mode_id__type="Other"))
    )\
    .order_by('year')
    for x in vrm_ts:
        pmt = pmt_ts.get(year=x['year'])
        if x['bus'] and x["bus"] > 0 and pmt['bus'] and pmt['bus'] > 0:
            bus_vrm = x['bus']
            bus_pmt = pmt['bus']
            bus_pmpm = round(bus_pmt / bus_vrm, 2)
        else:
            bus_pmpm = 0
        if x['rail'] and x["rail"] > 0 and pmt['rail'] and pmt['rail'] > 0:
            rail_vrm = x['rail']
            rail_pmt = pmt['rail']
            rail_pmpm = round(rail_pmt / rail_vrm, 2)
        else:
            rail_pmpm = 0
        if x['microtransit'] and x["microtransit"] > 0 and pmt['microtransit'] and pmt['microtransit'] > 0:
            microtransit_vrm = x['microtransit']
            microtransit_pmt = pmt['microtransit']
            microtransit_pmpm = round(microtransit_pmt / microtransit_vrm, 2)
        else:
            microtransit_pmpm = 0
        if x['ferry'] and x["ferry"] > 0 and pmt['ferry'] and pmt['ferry'] > 0:
            ferry_vrm = x['ferry']
            ferry_pmt = pmt['ferry']
            ferry_pmpm = round(ferry_pmt / ferry_vrm, 2)
        else:
            ferry_pmpm = 0
        if x['other'] and x["other"] > 0 and pmt['other'] and pmt['other'] > 0:
            other_vrm = x['other']
            other_pmt = pmt['other']
            other_pmpm = round(other_pmt / other_vrm, 2)
        else:
            other_pmpm = 0
            
        data += [{"year": x['year'], "bus": bus_pmpm, "rail": rail_pmpm, "microtransit": microtransit_pmpm, "ferry": ferry_pmpm, "other": other_pmpm}]
    
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)





@csrf_exempt
def cost_per_upt_by_mode(request):
    filters, q = process_params(request.GET)
    opexp_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(mb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="MB"))), \
                                 cb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="CB"))), \
                                 rb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="RB"))), \
                                 tb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="TB"))), \
                                 pb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="PB"))), \
                                 hr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="HR"))), \
                                 lr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="LR"))), \
                                 cr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="CR"))), \
                                 yr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="YR"))), \
                                 sr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="SR"))), \
                                 cc_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="CC"))), \
                                 mg_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="MG"))), \
                                 ip_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="IP"))), \
                                 ar_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="AR"))), \
                                 other_rail_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="OR"))), \
                                 dr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="DR"))), \
                                 dt_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="DT"))), \
                                 vp_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="VP"))), \
                                 jt_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="JT"))), \
                                 fb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="FB"))), \
                                 tr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="TR"))), \
                                 ot_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__in=["OT", "nan"])))).\
        order_by('year')
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(mb_upt=Round(Sum(F('upt'), filter=Q(mode_id="MB"))), \
                                 cb_upt=Round(Sum(F('upt'), filter=Q(mode_id="CB"))), \
                                 rb_upt=Round(Sum(F('upt'), filter=Q(mode_id="RB"))), \
                                 tb_upt=Round(Sum(F('upt'), filter=Q(mode_id="TB"))), \
                                 pb_upt=Round(Sum(F('upt'), filter=Q(mode_id="PB"))), \
                                 hr_upt=Round(Sum(F('upt'), filter=Q(mode_id="HR"))), \
                                 lr_upt=Round(Sum(F('upt'), filter=Q(mode_id="LR"))), \
                                 cr_upt=Round(Sum(F('upt'), filter=Q(mode_id="CR"))), \
                                 yr_upt=Round(Sum(F('upt'), filter=Q(mode_id="YR"))), \
                                 sr_upt=Round(Sum(F('upt'), filter=Q(mode_id="SR"))), \
                                 cc_upt=Round(Sum(F('upt'), filter=Q(mode_id="CC"))), \
                                 mg_upt=Round(Sum(F('upt'), filter=Q(mode_id="MG"))), \
                                 ip_upt=Round(Sum(F('upt'), filter=Q(mode_id="IP"))), \
                                 ar_upt=Round(Sum(F('upt'), filter=Q(mode_id="AR"))), \
                                 other_rail_upt=Round(Sum(F('upt'), filter=Q(mode_id="OR"))), \
                                 dr_upt=Round(Sum(F('upt'), filter=Q(mode_id="DR"))), \
                                 dt_upt=Round(Sum(F('upt'), filter=Q(mode_id="DT"))), \
                                 vp_upt=Round(Sum(F('upt'), filter=Q(mode_id="VP"))), \
                                 jt_upt=Round(Sum(F('upt'), filter=Q(mode_id="JT"))), \
                                 fb_upt=Round(Sum(F('upt'), filter=Q(mode_id="FB"))), \
                                 tr_upt=Round(Sum(F('upt'), filter=Q(mode_id="TR"))), \
                                 ot_upt=Round(Sum(F('upt'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in opexp_ts:

        ridership = upt_ts.get(year=x['year'])

        if ridership['mb_upt'] and ridership['mb_upt'] > 0 and x['mb_opexp'] and x['mb_opexp'] > 0:
            mb_upt = ridership['mb_upt']
            mb_opexp = x['mb_opexp']
            mb_cpp = round(mb_opexp/mb_upt, 2)
        else:
            mb_cpp = 0

        if ridership['cb_upt'] and ridership['cb_upt'] > 0 and x['cb_opexp'] and x['cb_opexp'] > 0:
            cb_upt = ridership['cb_upt']
            cb_opexp = x['cb_opexp']
            cb_cpp = round(cb_opexp/cb_upt, 2)
        else:
            cb_cpp = 0

        if ridership['rb_upt'] and ridership['rb_upt'] > 0 and x['rb_opexp'] and x['rb_opexp'] > 0:
            rb_upt = ridership['rb_upt']
            rb_opexp = x['rb_opexp']
            rb_cpp = round(rb_opexp/rb_upt, 2)
        else:
            rb_cpp = 0

        if ridership['tb_upt'] and ridership['tb_upt'] > 0 and x['tb_opexp'] and x['tb_opexp'] > 0:
            tb_upt = ridership['tb_upt']
            tb_opexp = x['tb_opexp']
            tb_cpp = round(tb_opexp/tb_upt, 2)
        else:
            tb_cpp = 0

        if ridership['pb_upt'] and ridership['pb_upt'] > 0 and x['pb_opexp'] and x['pb_opexp'] > 0:
            pb_upt = ridership['pb_upt']
            pb_opexp = x['pb_opexp']
            pb_cpp = round(pb_opexp/pb_upt, 2)
        else:
            pb_cpp = 0

        if ridership['hr_upt'] and ridership['hr_upt'] > 0 and x['hr_opexp'] and x['hr_opexp'] > 0:
            hr_upt = ridership['hr_upt']
            hr_opexp = x['hr_opexp']
            hr_cpp = round(hr_opexp/hr_upt, 2)
        else:
            hr_cpp = 0

        if ridership['lr_upt'] and ridership['lr_upt'] > 0 and x['lr_opexp'] and x['lr_opexp'] > 0:
            lr_upt = ridership['lr_upt']
            lr_opexp = x['lr_opexp']
            lr_cpp = round(lr_opexp/lr_upt, 2)
        else:
            lr_cpp = 0

        if ridership['cr_upt'] and ridership['cr_upt'] > 0 and x['cr_opexp'] and x['cr_opexp'] > 0:
            cr_upt = ridership['cr_upt']
            cr_opexp = x['cr_opexp']
            cr_cpp = round(cr_opexp/cr_upt, 2)
        else:
            cr_cpp = 0

        if ridership['yr_upt'] and ridership['yr_upt'] > 0 and x['yr_opexp'] and x['yr_opexp'] > 0:
            yr_upt = ridership['yr_upt']
            yr_opexp = x['yr_opexp']
            yr_cpp = round(yr_opexp/yr_upt, 2)
        else:
            yr_cpp = 0

        if ridership['cc_upt'] and ridership['cc_upt'] > 0 and x['cc_opexp'] and x['cc_opexp'] > 0:
            cc_upt = ridership['cc_upt']
            cc_opexp = x['cc_opexp']
            cc_cpp = round(cc_opexp/cc_upt, 2)
        else:
            cc_cpp = 0

        if ridership['mg_upt'] and ridership['mg_upt'] > 0 and x['mg_opexp'] and x['mg_opexp'] > 0:
            mg_upt = ridership['mg_upt']
            mg_opexp = x['mg_opexp']
            mg_cpp = round(mg_opexp/mg_upt, 2)
        else:
            mg_cpp = 0

        if ridership['ip_upt'] and ridership['ip_upt'] > 0 and x['ip_opexp'] and x['ip_opexp'] > 0:
            ip_upt = ridership['ip_upt']
            ip_opexp = x['ip_opexp']
            ip_cpp = round(ip_opexp/ip_upt, 2)
        else:
            ip_cpp = 0

        if ridership['ar_upt'] and ridership['ar_upt'] > 0 and x['ar_opexp'] and x['ar_opexp'] > 0:
            ar_upt = ridership['ar_upt']
            ar_opexp = x['ar_opexp']
            ar_cpp = round(ar_opexp/ar_upt, 2)
        else:
            ar_cpp = 0

        if ridership['other_rail_upt'] and ridership['other_rail_upt'] > 0 and x['other_rail_opexp'] and x['other_rail_opexp'] > 0:
            other_rail_upt = ridership['other_rail_upt']
            other_rail_opexp = x['other_rail_opexp']
            other_rail_cpp = round(other_rail_opexp/other_rail_upt, 2)
        else:
            other_rail_cpp = 0

        if ridership['dr_upt'] and ridership['dr_upt'] > 0 and x['dr_opexp'] and x['dr_opexp'] > 0:
            dr_upt = ridership['dr_upt']
            dr_opexp = x['dr_opexp']
            dr_cpp = round(dr_opexp/dr_upt, 2)
        else:
            dr_cpp = 0

        if ridership['dt_upt'] and ridership['dt_upt'] > 0 and x['dt_opexp'] and x['dt_opexp'] > 0:
            dt_upt = ridership['dt_upt']
            dt_opexp = x['dt_opexp']
            dt_cpp = round(dt_opexp/dt_upt, 2)
        else:
            dt_cpp = 0

        if ridership['vp_upt'] and ridership['vp_upt'] > 0 and x['vp_opexp'] and x['vp_opexp'] > 0:
            vp_upt = ridership['vp_upt']
            vp_opexp = x['vp_opexp']
            vp_cpp = round(vp_opexp/vp_upt, 2)
        else:
            vp_cpp = 0

        if ridership['jt_upt'] and ridership['jt_upt'] > 0 and x['jt_opexp'] and x['jt_opexp'] > 0:
            jt_upt = ridership['jt_upt']
            jt_opexp = x['jt_opexp']
            jt_cpp = round(jt_opexp/jt_upt, 2)
        else:
            jt_cpp = 0

        if ridership['fb_upt'] and ridership['fb_upt'] > 0 and x['fb_opexp'] and x['fb_opexp'] > 0:
            fb_upt = ridership['fb_upt']
            fb_opexp = x['fb_opexp']
            fb_cpp = round(fb_opexp/fb_upt, 2)
        else:
            fb_cpp = 0

        if ridership['tr_upt'] and ridership['tr_upt'] > 0 and x['tr_opexp'] and x['tr_opexp'] > 0:
            tr_upt = ridership['tr_upt']
            tr_opexp = x['tr_opexp']
            tr_cpp = round(tr_opexp/tr_upt, 2)
        else:
            tr_cpp = 0

        if ridership['ot_upt'] and ridership['ot_upt'] > 0 and x['ot_opexp'] and x['ot_opexp'] > 0:
            ot_upt = ridership['ot_upt']
            ot_opexp = x['ot_opexp']
            ot_cpp = round(ot_opexp/ot_upt, 2)
        else:
            ot_cpp = 0

        data += [{"year": x['year'], "mb": mb_cpp, "cb": cb_cpp, "rb": rb_cpp, "tb": tb_cpp, "pb": pb_cpp, "hr": hr_cpp, "cr": cr_cpp, "lr": lr_cpp, "yr": yr_cpp, "cc": cc_cpp, "mg": mg_cpp, "ip": ip_cpp, "ar": ar_cpp, "other_rail": other_rail_cpp, "dr": dr_cpp, "dt": dt_cpp, "vp": vp_cpp, "jt": jt_cpp, "fb": fb_cpp, "tr": tr_cpp, "ot": ot_cpp}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def cost_per_pmt_by_mode(request):
    filters, q = process_params(request.GET)
    opexp_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(mb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="MB"))), \
                                 cb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="CB"))), \
                                 rb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="RB"))), \
                                 tb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="TB"))), \
                                 pb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="PB"))), \
                                 hr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="HR"))), \
                                 lr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="LR"))), \
                                 cr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="CR"))), \
                                 yr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="YR"))), \
                                 sr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="SR"))), \
                                 cc_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="CC"))), \
                                 mg_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="MG"))), \
                                 ip_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="IP"))), \
                                 ar_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="AR"))), \
                                 other_rail_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="OR"))), \
                                 dr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="DR"))), \
                                 dt_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="DT"))), \
                                 vp_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="VP"))), \
                                 jt_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="JT"))), \
                                 fb_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="FB"))), \
                                 tr_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id="TR"))), \
                                 ot_opexp=Round(Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", mode_id__in=["OT", "nan"])))).\
        order_by('year')
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(mb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="MB"))), \
                                 cb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CB"))), \
                                 rb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="RB"))), \
                                 tb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="TB"))), \
                                 pb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="PB"))), \
                                 hr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="HR"))), \
                                 lr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="LR"))), \
                                 cr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CR"))), \
                                 yr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="YR"))), \
                                 sr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="SR"))), \
                                 cc_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CC"))), \
                                 mg_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="MG"))), \
                                 ip_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="IP"))), \
                                 ar_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="AR"))), \
                                 other_rail_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="OR"))), \
                                 dr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="DR"))), \
                                 dt_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="DT"))), \
                                 vp_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="VP"))), \
                                 jt_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="JT"))), \
                                 fb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="FB"))), \
                                 tr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="TR"))), \
                                 ot_pmt=Round(Sum(F('pmt'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in opexp_ts:

        ridership = pmt_ts.get(year=x['year'])

        if ridership['mb_pmt'] and ridership['mb_pmt'] > 0 and x['mb_opexp'] and x['mb_opexp'] > 0:
            mb_pmt = ridership['mb_pmt']
            mb_opexp = x['mb_opexp']
            mb_cpm = round(mb_opexp/mb_pmt, 2)
        else:
            mb_cpm = 0

        if ridership['cb_pmt'] and ridership['cb_pmt'] > 0 and x['cb_opexp'] and x['cb_opexp'] > 0:
            cb_pmt = ridership['cb_pmt']
            cb_opexp = x['cb_opexp']
            cb_cpm = round(cb_opexp/cb_pmt, 2)
        else:
            cb_cpm = 0

        if ridership['rb_pmt'] and ridership['rb_pmt'] > 0 and x['rb_opexp'] and x['rb_opexp'] > 0:
            rb_pmt = ridership['rb_pmt']
            rb_opexp = x['rb_opexp']
            rb_cpm = round(rb_opexp/rb_pmt, 2)
        else:
            rb_cpm = 0

        if ridership['tb_pmt'] and ridership['tb_pmt'] > 0 and x['tb_opexp'] and x['tb_opexp'] > 0:
            tb_pmt = ridership['tb_pmt']
            tb_opexp = x['tb_opexp']
            tb_cpm = round(tb_opexp/tb_pmt, 2)
        else:
            tb_cpm = 0

        if ridership['pb_pmt'] and ridership['pb_pmt'] > 0 and x['pb_opexp'] and x['pb_opexp'] > 0:
            pb_pmt = ridership['pb_pmt']
            pb_opexp = x['pb_opexp']
            pb_cpm = round(pb_opexp/pb_pmt, 2)
        else:
            pb_cpm = 0

        if ridership['hr_pmt'] and ridership['hr_pmt'] > 0 and x['hr_opexp'] and x['hr_opexp'] > 0:
            hr_pmt = ridership['hr_pmt']
            hr_opexp = x['hr_opexp']
            hr_cpm = round(hr_opexp/hr_pmt, 2)
        else:
            hr_cpm = 0

        if ridership['lr_pmt'] and ridership['lr_pmt'] > 0 and x['lr_opexp'] and x['lr_opexp'] > 0:
            lr_pmt = ridership['lr_pmt']
            lr_opexp = x['lr_opexp']
            lr_cpm = round(lr_opexp/lr_pmt, 2)
        else:
            lr_cpm = 0

        if ridership['cr_pmt'] and ridership['cr_pmt'] > 0 and x['cr_opexp'] and x['cr_opexp'] > 0:
            cr_pmt = ridership['cr_pmt']
            cr_opexp = x['cr_opexp']
            cr_cpm = round(cr_opexp/cr_pmt, 2)
        else:
            cr_cpm = 0

        if ridership['yr_pmt'] and ridership['yr_pmt'] > 0 and x['yr_opexp'] and x['yr_opexp'] > 0:
            yr_pmt = ridership['yr_pmt']
            yr_opexp = x['yr_opexp']
            yr_cpm = round(yr_opexp/yr_pmt, 2)
        else:
            yr_cpm = 0

        if ridership['cc_pmt'] and ridership['cc_pmt'] > 0 and x['cc_opexp'] and x['cc_opexp'] > 0:
            cc_pmt = ridership['cc_pmt']
            cc_opexp = x['cc_opexp']
            cc_cpm = round(cc_opexp/cc_pmt, 2)
        else:
            cc_cpm = 0

        if ridership['mg_pmt'] and ridership['mg_pmt'] > 0 and x['mg_opexp'] and x['mg_opexp'] > 0:
            mg_pmt = ridership['mg_pmt']
            mg_opexp = x['mg_opexp']
            mg_cpm = round(mg_opexp/mg_pmt, 2)
        else:
            mg_cpm = 0

        if ridership['ip_pmt'] and ridership['ip_pmt'] > 0 and x['ip_opexp'] and x['ip_opexp'] > 0:
            ip_pmt = ridership['ip_pmt']
            ip_opexp = x['ip_opexp']
            ip_cpm = round(ip_opexp/ip_pmt, 2)
        else:
            ip_cpm = 0

        if ridership['ar_pmt'] and ridership['ar_pmt'] > 0 and x['ar_opexp'] and x['ar_opexp'] > 0:
            ar_pmt = ridership['ar_pmt']
            ar_opexp = x['ar_opexp']
            ar_cpm = round(ar_opexp/ar_pmt, 2)
        else:
            ar_cpm = 0

        if ridership['other_rail_pmt'] and ridership['other_rail_pmt'] > 0 and x['other_rail_opexp'] and x['other_rail_opexp'] > 0:
            other_rail_pmt = ridership['other_rail_pmt']
            other_rail_opexp = x['other_rail_opexp']
            other_rail_cpm = round(other_rail_opexp/other_rail_pmt, 2)
        else:
            other_rail_cpm = 0

        if ridership['dr_pmt'] and ridership['dr_pmt'] > 0 and x['dr_opexp'] and x['dr_opexp'] > 0:
            dr_pmt = ridership['dr_pmt']
            dr_opexp = x['dr_opexp']
            dr_cpm = round(dr_opexp/dr_pmt, 2)
        else:
            dr_cpm = 0

        if ridership['dt_pmt'] and ridership['dt_pmt'] > 0 and x['dt_opexp'] and x['dt_opexp'] > 0:
            dt_pmt = ridership['dt_pmt']
            dt_opexp = x['dt_opexp']
            dt_cpm = round(dt_opexp/dt_pmt, 2)
        else:
            dt_cpm = 0

        if ridership['vp_pmt'] and ridership['vp_pmt'] > 0 and x['vp_opexp'] and x['vp_opexp'] > 0:
            vp_pmt = ridership['vp_pmt']
            vp_opexp = x['vp_opexp']
            vp_cpm = round(vp_opexp/vp_pmt, 2)
        else:
            vp_cpm = 0

        if ridership['jt_pmt'] and ridership['jt_pmt'] > 0 and x['jt_opexp'] and x['jt_opexp'] > 0:
            jt_pmt = ridership['jt_pmt']
            jt_opexp = x['jt_opexp']
            jt_cpm = round(jt_opexp/jt_pmt, 2)
        else:
            jt_cpm = 0

        if ridership['fb_pmt'] and ridership['fb_pmt'] > 0 and x['fb_opexp'] and x['fb_opexp'] > 0:
            fb_pmt = ridership['fb_pmt']
            fb_opexp = x['fb_opexp']
            fb_cpm = round(fb_opexp/fb_pmt, 2)
        else:
            fb_cpm = 0

        if ridership['tr_pmt'] and ridership['tr_pmt'] > 0 and x['tr_opexp'] and x['tr_opexp'] > 0:
            tr_pmt = ridership['tr_pmt']
            tr_opexp = x['tr_opexp']
            tr_cpm = round(tr_opexp/tr_pmt, 2)
        else:
            tr_cpm = 0

        if ridership['ot_pmt'] and ridership['ot_pmt'] > 0 and x['ot_opexp'] and x['ot_opexp'] > 0:
            ot_pmt = ridership['ot_pmt']
            ot_opexp = x['ot_opexp']
            ot_cpm = round(ot_opexp/ot_pmt, 2)
        else:
            ot_cpm = 0

        data += [{"year": x['year'], "mb": mb_cpm, "cb": cb_cpm, "rb": rb_cpm, "tb": tb_cpm, "pb": pb_cpm, "hr": hr_cpm, "cr": cr_cpm, "lr": lr_cpm, "yr": yr_cpm, "cc": cc_cpm, "mg": mg_cpm, "ip": ip_cpm, "ar": ar_cpm, "other_rail": other_rail_cpm, "dr": dr_cpm, "dt": dt_cpm, "vp": vp_cpm, "jt": jt_cpm, "fb": fb_cpm, "tr": tr_cpm, "ot": ot_cpm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def frr_by_mode(request):

    filters, q = process_params(request.GET)
    opexp_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(mb_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="MB"))), \
                                 cb_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="CB"))), \
                                 rb_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="RB"))), \
                                 tb_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="TB"))), \
                                 pb_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="PB"))), \
                                 hr_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="HR"))), \
                                 lr_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="LR"))), \
                                 cr_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="CR"))), \
                                 yr_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="YR"))), \
                                 sr_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="SR"))), \
                                 cc_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="CC"))), \
                                 mg_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="MG"))), \
                                 ip_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="IP"))), \
                                 ar_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="AR"))), \
                                 other_rail_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="OR"))), \
                                 dr_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="DR"))), \
                                 dt_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="DT"))), \
                                 vp_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="VP"))), \
                                 jt_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="JT"))), \
                                 fb_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="FB"))), \
                                 tr_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id="TR"))), \
                                 ot_opexp=Round(Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", mode_id__in=["OT", "nan"])))).\
        order_by('year')
    fares_ts = Fares.objects.filter(q)\
        .values("year").annotate(mb_fares=Round(Sum(F('fares'), filter=Q(mode_id="MB"))), \
                                 cb_fares=Round(Sum(F('fares'), filter=Q(mode_id="CB"))), \
                                 rb_fares=Round(Sum(F('fares'), filter=Q(mode_id="RB"))), \
                                 tb_fares=Round(Sum(F('fares'), filter=Q(mode_id="TB"))), \
                                 pb_fares=Round(Sum(F('fares'), filter=Q(mode_id="PB"))), \
                                 hr_fares=Round(Sum(F('fares'), filter=Q(mode_id="HR"))), \
                                 lr_fares=Round(Sum(F('fares'), filter=Q(mode_id="LR"))), \
                                 cr_fares=Round(Sum(F('fares'), filter=Q(mode_id="CR"))), \
                                 yr_fares=Round(Sum(F('fares'), filter=Q(mode_id="YR"))), \
                                 sr_fares=Round(Sum(F('fares'), filter=Q(mode_id="SR"))), \
                                 cc_fares=Round(Sum(F('fares'), filter=Q(mode_id="CC"))), \
                                 mg_fares=Round(Sum(F('fares'), filter=Q(mode_id="MG"))), \
                                 ip_fares=Round(Sum(F('fares'), filter=Q(mode_id="IP"))), \
                                 ar_fares=Round(Sum(F('fares'), filter=Q(mode_id="AR"))), \
                                 other_rail_fares=Round(Sum(F('fares'), filter=Q(mode_id="OR"))), \
                                 dr_fares=Round(Sum(F('fares'), filter=Q(mode_id="DR"))), \
                                 dt_fares=Round(Sum(F('fares'), filter=Q(mode_id="DT"))), \
                                 vp_fares=Round(Sum(F('fares'), filter=Q(mode_id="VP"))), \
                                 jt_fares=Round(Sum(F('fares'), filter=Q(mode_id="JT"))), \
                                 fb_fares=Round(Sum(F('fares'), filter=Q(mode_id="FB"))), \
                                 tr_fares=Round(Sum(F('fares'), filter=Q(mode_id="TR"))), \
                                 ot_fares=Round(Sum(F('fares'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in opexp_ts:

        fares = fares_ts.get(year=x['year'])

        if fares['mb_fares'] and fares['mb_fares'] > 0 and x['mb_opexp'] and x['mb_opexp'] > 0:
            mb_fares = fares['mb_fares']
            mb_opexp = x['mb_opexp']
            mb_frr = round(mb_fares/mb_opexp, 2)
        else:
            mb_frr = 0

        if fares['cb_fares'] and fares['cb_fares'] > 0 and x['cb_opexp'] and x['cb_opexp'] > 0:
            cb_fares = fares['cb_fares']
            cb_opexp = x['cb_opexp']
            cb_frr = round(cb_fares/cb_opexp, 2)
        else:
            cb_frr = 0

        if fares['rb_fares'] and fares['rb_fares'] > 0 and x['rb_opexp'] and x['rb_opexp'] > 0:
            rb_fares = fares['rb_fares']
            rb_opexp = x['rb_opexp']
            rb_frr = round(rb_fares/rb_opexp, 2)
        else:
            rb_frr = 0

        if fares['tb_fares'] and fares['tb_fares'] > 0 and x['tb_opexp'] and x['tb_opexp'] > 0:
            tb_fares = fares['tb_fares']
            tb_opexp = x['tb_opexp']
            tb_frr = round(tb_fares/tb_opexp, 2)
        else:
            tb_frr = 0

        if fares['pb_fares'] and fares['pb_fares'] > 0 and x['pb_opexp'] and x['pb_opexp'] > 0:
            pb_fares = fares['pb_fares']
            pb_opexp = x['pb_opexp']
            pb_frr = round(pb_fares/pb_opexp, 2)
        else:
            pb_frr = 0

        if fares['hr_fares'] and fares['hr_fares'] > 0 and x['hr_opexp'] and x['hr_opexp'] > 0:
            hr_fares = fares['hr_fares']
            hr_opexp = x['hr_opexp']
            hr_frr = round(hr_fares/hr_opexp, 2)
        else:
            hr_frr = 0

        if fares['lr_fares'] and fares['lr_fares'] > 0 and x['lr_opexp'] and x['lr_opexp'] > 0:
            lr_fares = fares['lr_fares']
            lr_opexp = x['lr_opexp']
            lr_frr = round(lr_fares/lr_opexp, 2)
        else:
            lr_frr = 0

        if fares['cr_fares'] and fares['cr_fares'] > 0 and x['cr_opexp'] and x['cr_opexp'] > 0:
            cr_fares = fares['cr_fares']
            cr_opexp = x['cr_opexp']
            cr_frr = round(cr_fares/cr_opexp, 2)
        else:
            cr_frr = 0

        if fares['yr_fares'] and fares['yr_fares'] > 0 and x['yr_opexp'] and x['yr_opexp'] > 0:
            yr_fares = fares['yr_fares']
            yr_opexp = x['yr_opexp']
            yr_frr = round(yr_fares/yr_opexp, 2)
        else:
            yr_frr = 0

        if fares['cc_fares'] and fares['cc_fares'] > 0 and x['cc_opexp'] and x['cc_opexp'] > 0:
            cc_fares = fares['cc_fares']
            cc_opexp = x['cc_opexp']
            cc_frr = round(cc_fares/cc_opexp, 2)
        else:
            cc_frr = 0

        if fares['mg_fares'] and fares['mg_fares'] > 0 and x['mg_opexp'] and x['mg_opexp'] > 0:
            mg_fares = fares['mg_fares']
            mg_opexp = x['mg_opexp']
            mg_frr = round(mg_fares/mg_opexp, 2)
        else:
            mg_frr = 0

        if fares['ip_fares'] and fares['ip_fares'] > 0 and x['ip_opexp'] and x['ip_opexp'] > 0:
            ip_fares = fares['ip_fares']
            ip_opexp = x['ip_opexp']
            ip_frr = round(ip_fares/ip_opexp, 2)
        else:
            ip_frr = 0

        if fares['ar_fares'] and fares['ar_fares'] > 0 and x['ar_opexp'] and x['ar_opexp'] > 0:
            ar_fares = fares['ar_fares']
            ar_opexp = x['ar_opexp']
            ar_frr = round(ar_fares/ar_opexp, 2)
        else:
            ar_frr = 0

        if fares['other_rail_fares'] and fares['other_rail_fares'] > 0 and x['other_rail_opexp'] and x['other_rail_opexp'] > 0:
            other_rail_fares = fares['other_rail_fares']
            other_rail_opexp = x['other_rail_opexp']
            other_rail_frr = round(other_rail_fares/other_rail_opexp, 2)
        else:
            other_rail_frr = 0

        if fares['dr_fares'] and fares['dr_fares'] > 0 and x['dr_opexp'] and x['dr_opexp'] > 0:
            dr_fares = fares['dr_fares']
            dr_opexp = x['dr_opexp']
            dr_frr = round(dr_fares/dr_opexp, 2)
        else:
            dr_frr = 0

        if fares['dt_fares'] and fares['dt_fares'] > 0 and x['dt_opexp'] and x['dt_opexp'] > 0:
            dt_fares = fares['dt_fares']
            dt_opexp = x['dt_opexp']
            dt_frr = round(dt_fares/dt_opexp, 2)
        else:
            dt_frr = 0

        if fares['vp_fares'] and fares['vp_fares'] > 0 and x['vp_opexp'] and x['vp_opexp'] > 0:
            vp_fares = fares['vp_fares']
            vp_opexp = x['vp_opexp']
            vp_frr = round(vp_fares/vp_opexp, 2)
        else:
            vp_frr = 0

        if fares['jt_fares'] and fares['jt_fares'] > 0 and x['jt_opexp'] and x['jt_opexp'] > 0:
            jt_fares = fares['jt_fares']
            jt_opexp = x['jt_opexp']
            jt_frr = round(jt_fares/jt_opexp, 2)
        else:
            jt_frr = 0

        if fares['fb_fares'] and fares['fb_fares'] > 0 and x['fb_opexp'] and x['fb_opexp'] > 0:
            fb_fares = fares['fb_fares']
            fb_opexp = x['fb_opexp']
            fb_frr = round(fb_fares/fb_opexp, 2)
        else:
            fb_frr = 0

        if fares['tr_fares'] and fares['tr_fares'] > 0 and x['tr_opexp'] and x['tr_opexp'] > 0:
            tr_fares = fares['tr_fares']
            tr_opexp = x['tr_opexp']
            tr_frr = round(tr_fares/tr_opexp, 2)
        else:
            tr_frr = 0

        if fares['ot_fares'] and fares['ot_fares'] > 0 and x['ot_opexp'] and x['ot_opexp'] > 0:
            ot_fares = fares['ot_fares']
            ot_opexp = x['ot_opexp']
            ot_frr = round(ot_fares/ot_opexp, 2)
        else:
            ot_frr = 0

        data += [{"year": x['year'], "mb": mb_frr, "cb": cb_frr, "rb": rb_frr, "tb": tb_frr, "pb": pb_frr, "hr": hr_frr, "cr": cr_frr, "lr": lr_frr, "yr": yr_frr, "cc": cc_frr, "mg": mg_frr, "ip": ip_frr, "ar": ar_frr, "other_rail": other_rail_frr, "dr": dr_frr, "dt": dt_frr, "vp": vp_frr, "jt": jt_frr, "fb": fb_frr, "tr": tr_frr, "ot": ot_frr}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

# @csrf_exempt
# def cost_per_vrh_by_mode(request):
#     return(JsonResponse({}))

# @csrf_exempt
# def cost_per_vrm_by_mode(request):
#     return(JsonResponse({}))

@csrf_exempt
def vrm_per_vrh_by_mode(request):
    filters, q = process_params(request.GET)
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(mb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="MB"))), \
                                 cb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CB"))), \
                                 rb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="RB"))), \
                                 tb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="TB"))), \
                                 pb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="PB"))), \
                                 hr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="HR"))), \
                                 lr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="LR"))), \
                                 cr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CR"))), \
                                 yr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="YR"))), \
                                 sr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="SR"))), \
                                 cc_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CC"))), \
                                 mg_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="MG"))), \
                                 ip_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="IP"))), \
                                 ar_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="AR"))), \
                                 other_rail_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="OR"))), \
                                 dr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="DR"))), \
                                 dt_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="DT"))), \
                                 vp_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="VP"))), \
                                 jt_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="JT"))), \
                                 fb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="FB"))), \
                                 tr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="TR"))), \
                                 ot_vrm=Round(Sum(F('vrm'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(mb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="MB"))), \
                                 cb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CB"))), \
                                 rb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="RB"))), \
                                 tb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="TB"))), \
                                 pb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="PB"))), \
                                 hr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="HR"))), \
                                 lr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="LR"))), \
                                 cr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CR"))), \
                                 yr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="YR"))), \
                                 sr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="SR"))), \
                                 cc_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CC"))), \
                                 mg_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="MG"))), \
                                 ip_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="IP"))), \
                                 ar_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="AR"))), \
                                 other_rail_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="OR"))), \
                                 dr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="DR"))), \
                                 dt_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="DT"))), \
                                 vp_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="VP"))), \
                                 jt_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="JT"))), \
                                 fb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="FB"))), \
                                 tr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="TR"))), \
                                 ot_vrh=Round(Sum(F('vrh'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in vrh_ts:

        vrm = vrm_ts.get(year=x['year'])

        if vrm['mb_vrm'] and vrm['mb_vrm'] > 0 and x['mb_vrh'] and x['mb_vrh'] > 0:
            mb_vrm = vrm['mb_vrm']
            mb_vrh = x['mb_vrh']
            mb_mph = round(mb_vrm/mb_vrh, 2)
        else:
            mb_mph = 0

        if vrm['cb_vrm'] and vrm['cb_vrm'] > 0 and x['cb_vrh'] and x['cb_vrh'] > 0:
            cb_vrm = vrm['cb_vrm']
            cb_vrh = x['cb_vrh']
            cb_mph = round(cb_vrm/cb_vrh, 2)
        else:
            cb_mph = 0

        if vrm['rb_vrm'] and vrm['rb_vrm'] > 0 and x['rb_vrh'] and x['rb_vrh'] > 0:
            rb_vrm = vrm['rb_vrm']
            rb_vrh = x['rb_vrh']
            rb_mph = round(rb_vrm/rb_vrh, 2)
        else:
            rb_mph = 0

        if vrm['tb_vrm'] and vrm['tb_vrm'] > 0 and x['tb_vrh'] and x['tb_vrh'] > 0:
            tb_vrm = vrm['tb_vrm']
            tb_vrh = x['tb_vrh']
            tb_mph = round(tb_vrm/tb_vrh, 2)
        else:
            tb_mph = 0

        if vrm['pb_vrm'] and vrm['pb_vrm'] > 0 and x['pb_vrh'] and x['pb_vrh'] > 0:
            pb_vrm = vrm['pb_vrm']
            pb_vrh = x['pb_vrh']
            pb_mph = round(pb_vrm/pb_vrh, 2)
        else:
            pb_mph = 0

        if vrm['hr_vrm'] and vrm['hr_vrm'] > 0 and x['hr_vrh'] and x['hr_vrh'] > 0:
            hr_vrm = vrm['hr_vrm']
            hr_vrh = x['hr_vrh']
            hr_mph = round(hr_vrm/hr_vrh, 2)
        else:
            hr_mph = 0

        if vrm['lr_vrm'] and vrm['lr_vrm'] > 0 and x['lr_vrh'] and x['lr_vrh'] > 0:
            lr_vrm = vrm['lr_vrm']
            lr_vrh = x['lr_vrh']
            lr_mph = round(lr_vrm/lr_vrh, 2)
        else:
            lr_mph = 0

        if vrm['cr_vrm'] and vrm['cr_vrm'] > 0 and x['cr_vrh'] and x['cr_vrh'] > 0:
            cr_vrm = vrm['cr_vrm']
            cr_vrh = x['cr_vrh']
            cr_mph = round(cr_vrm/cr_vrh, 2)
        else:
            cr_mph = 0

        if vrm['yr_vrm'] and vrm['yr_vrm'] > 0 and x['yr_vrh'] and x['yr_vrh'] > 0:
            yr_vrm = vrm['yr_vrm']
            yr_vrh = x['yr_vrh']
            yr_mph = round(yr_vrm/yr_vrh, 2)
        else:
            yr_mph = 0

        if vrm['cc_vrm'] and vrm['cc_vrm'] > 0 and x['cc_vrh'] and x['cc_vrh'] > 0:
            cc_vrm = vrm['cc_vrm']
            cc_vrh = x['cc_vrh']
            cc_mph = round(cc_vrm/cc_vrh, 2)
        else:
            cc_mph = 0

        if vrm['mg_vrm'] and vrm['mg_vrm'] > 0 and x['mg_vrh'] and x['mg_vrh'] > 0:
            mg_vrm = vrm['mg_vrm']
            mg_vrh = x['mg_vrh']
            mg_mph = round(mg_vrm/mg_vrh, 2)
        else:
            mg_mph = 0

        if vrm['ip_vrm'] and vrm['ip_vrm'] > 0 and x['ip_vrh'] and x['ip_vrh'] > 0:
            ip_vrm = vrm['ip_vrm']
            ip_vrh = x['ip_vrh']
            ip_mph = round(ip_vrm/ip_vrh, 2)
        else:
            ip_mph = 0

        if vrm['ar_vrm'] and vrm['ar_vrm'] > 0 and x['ar_vrh'] and x['ar_vrh'] > 0:
            ar_vrm = vrm['ar_vrm']
            ar_vrh = x['ar_vrh']
            ar_mph = round(ar_vrm/ar_vrh, 2)
        else:
            ar_mph = 0

        if vrm['other_rail_vrm'] and vrm['other_rail_vrm'] > 0 and x['other_rail_vrh'] and x['other_rail_vrh'] > 0:
            other_rail_vrm = vrm['other_rail_vrm']
            other_rail_vrh = x['other_rail_vrh']
            other_rail_mph = round(other_rail_vrm/other_rail_vrh, 2)
        else:
            other_rail_mph = 0

        if vrm['dr_vrm'] and vrm['dr_vrm'] > 0 and x['dr_vrh'] and x['dr_vrh'] > 0:
            dr_vrm = vrm['dr_vrm']
            dr_vrh = x['dr_vrh']
            dr_mph = round(dr_vrm/dr_vrh, 2)
        else:
            dr_mph = 0

        if vrm['dt_vrm'] and vrm['dt_vrm'] > 0 and x['dt_vrh'] and x['dt_vrh'] > 0:
            dt_vrm = vrm['dt_vrm']
            dt_vrh = x['dt_vrh']
            dt_mph = round(dt_vrm/dt_vrh, 2)
        else:
            dt_mph = 0

        if vrm['vp_vrm'] and vrm['vp_vrm'] > 0 and x['vp_vrh'] and x['vp_vrh'] > 0:
            vp_vrm = vrm['vp_vrm']
            vp_vrh = x['vp_vrh']
            vp_mph = round(vp_vrm/vp_vrh, 2)
        else:
            vp_mph = 0

        if vrm['jt_vrm'] and vrm['jt_vrm'] > 0 and x['jt_vrh'] and x['jt_vrh'] > 0:
            jt_vrm = vrm['jt_vrm']
            jt_vrh = x['jt_vrh']
            jt_mph = round(jt_vrm/jt_vrh, 2)
        else:
            jt_mph = 0

        if vrm['fb_vrm'] and vrm['fb_vrm'] > 0 and x['fb_vrh'] and x['fb_vrh'] > 0:
            fb_vrm = vrm['fb_vrm']
            fb_vrh = x['fb_vrh']
            fb_mph = round(fb_vrm/fb_vrh, 2)
        else:
            fb_mph = 0

        if vrm['tr_vrm'] and vrm['tr_vrm'] > 0 and x['tr_vrh'] and x['tr_vrh'] > 0:
            tr_vrm = vrm['tr_vrm']
            tr_vrh = x['tr_vrh']
            tr_mph = round(tr_vrm/tr_vrh, 2)
        else:
            tr_mph = 0

        if vrm['ot_vrm'] and vrm['ot_vrm'] > 0 and x['ot_vrh'] and x['ot_vrh'] > 0:
            ot_vrm = vrm['ot_vrm']
            ot_vrh = x['ot_vrh']
            ot_mph = round(ot_vrm/ot_vrh, 2)
        else:
            ot_mph = 0

        data += [{"year": x['year'], "mb": mb_mph, "cb": cb_mph, "rb": rb_mph, "tb": tb_mph, "pb": pb_mph, "hr": hr_mph, "cr": cr_mph, "lr": lr_mph, "yr": yr_mph, "cc": cc_mph, "mg": mg_mph, "ip": ip_mph, "ar": ar_mph, "other_rail": other_rail_mph, "dr": dr_mph, "dt": dt_mph, "vp": vp_mph, "jt": jt_mph, "fb": fb_mph, "tr": tr_mph, "ot": ot_mph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_per_vrh_by_mode(request):
    filters, q = process_params(request.GET)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(mb_upt=Round(Sum(F('upt'), filter=Q(mode_id="MB"))), \
                                 cb_upt=Round(Sum(F('upt'), filter=Q(mode_id="CB"))), \
                                 rb_upt=Round(Sum(F('upt'), filter=Q(mode_id="RB"))), \
                                 tb_upt=Round(Sum(F('upt'), filter=Q(mode_id="TB"))), \
                                 pb_upt=Round(Sum(F('upt'), filter=Q(mode_id="PB"))), \
                                 hr_upt=Round(Sum(F('upt'), filter=Q(mode_id="HR"))), \
                                 lr_upt=Round(Sum(F('upt'), filter=Q(mode_id="LR"))), \
                                 cr_upt=Round(Sum(F('upt'), filter=Q(mode_id="CR"))), \
                                 yr_upt=Round(Sum(F('upt'), filter=Q(mode_id="YR"))), \
                                 sr_upt=Round(Sum(F('upt'), filter=Q(mode_id="SR"))), \
                                 cc_upt=Round(Sum(F('upt'), filter=Q(mode_id="CC"))), \
                                 mg_upt=Round(Sum(F('upt'), filter=Q(mode_id="MG"))), \
                                 ip_upt=Round(Sum(F('upt'), filter=Q(mode_id="IP"))), \
                                 ar_upt=Round(Sum(F('upt'), filter=Q(mode_id="AR"))), \
                                 other_rail_upt=Round(Sum(F('upt'), filter=Q(mode_id="OR"))), \
                                 dr_upt=Round(Sum(F('upt'), filter=Q(mode_id="DR"))), \
                                 dt_upt=Round(Sum(F('upt'), filter=Q(mode_id="DT"))), \
                                 vp_upt=Round(Sum(F('upt'), filter=Q(mode_id="VP"))), \
                                 jt_upt=Round(Sum(F('upt'), filter=Q(mode_id="JT"))), \
                                 fb_upt=Round(Sum(F('upt'), filter=Q(mode_id="FB"))), \
                                 tr_upt=Round(Sum(F('upt'), filter=Q(mode_id="TR"))), \
                                 ot_upt=Round(Sum(F('upt'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(mb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="MB"))), \
                                 cb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CB"))), \
                                 rb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="RB"))), \
                                 tb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="TB"))), \
                                 pb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="PB"))), \
                                 hr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="HR"))), \
                                 lr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="LR"))), \
                                 cr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CR"))), \
                                 yr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="YR"))), \
                                 sr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="SR"))), \
                                 cc_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CC"))), \
                                 mg_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="MG"))), \
                                 ip_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="IP"))), \
                                 ar_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="AR"))), \
                                 other_rail_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="OR"))), \
                                 dr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="DR"))), \
                                 dt_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="DT"))), \
                                 vp_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="VP"))), \
                                 jt_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="JT"))), \
                                 fb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="FB"))), \
                                 tr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="TR"))), \
                                 ot_vrh=Round(Sum(F('vrh'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in vrh_ts:

        upt = upt_ts.get(year=x['year'])

        if upt['mb_upt'] and upt['mb_upt'] > 0 and x['mb_vrh'] and x['mb_vrh'] > 0:
            mb_upt = upt['mb_upt']
            mb_vrh = x['mb_vrh']
            mb_pph = round(mb_upt/mb_vrh, 2)
        else:
            mb_pph = 0

        if upt['cb_upt'] and upt['cb_upt'] > 0 and x['cb_vrh'] and x['cb_vrh'] > 0:
            cb_upt = upt['cb_upt']
            cb_vrh = x['cb_vrh']
            cb_pph = round(cb_upt/cb_vrh, 2)
        else:
            cb_pph = 0

        if upt['rb_upt'] and upt['rb_upt'] > 0 and x['rb_vrh'] and x['rb_vrh'] > 0:
            rb_upt = upt['rb_upt']
            rb_vrh = x['rb_vrh']
            rb_pph = round(rb_upt/rb_vrh, 2)
        else:
            rb_pph = 0

        if upt['tb_upt'] and upt['tb_upt'] > 0 and x['tb_vrh'] and x['tb_vrh'] > 0:
            tb_upt = upt['tb_upt']
            tb_vrh = x['tb_vrh']
            tb_pph = round(tb_upt/tb_vrh, 2)
        else:
            tb_pph = 0

        if upt['pb_upt'] and upt['pb_upt'] > 0 and x['pb_vrh'] and x['pb_vrh'] > 0:
            pb_upt = upt['pb_upt']
            pb_vrh = x['pb_vrh']
            pb_pph = round(pb_upt/pb_vrh, 2)
        else:
            pb_pph = 0

        if upt['hr_upt'] and upt['hr_upt'] > 0 and x['hr_vrh'] and x['hr_vrh'] > 0:
            hr_upt = upt['hr_upt']
            hr_vrh = x['hr_vrh']
            hr_pph = round(hr_upt/hr_vrh, 2)
        else:
            hr_pph = 0

        if upt['lr_upt'] and upt['lr_upt'] > 0 and x['lr_vrh'] and x['lr_vrh'] > 0:
            lr_upt = upt['lr_upt']
            lr_vrh = x['lr_vrh']
            lr_pph = round(lr_upt/lr_vrh, 2)
        else:
            lr_pph = 0

        if upt['cr_upt'] and upt['cr_upt'] > 0 and x['cr_vrh'] and x['cr_vrh'] > 0:
            cr_upt = upt['cr_upt']
            cr_vrh = x['cr_vrh']
            cr_pph = round(cr_upt/cr_vrh, 2)
        else:
            cr_pph = 0

        if upt['yr_upt'] and upt['yr_upt'] > 0 and x['yr_vrh'] and x['yr_vrh'] > 0:
            yr_upt = upt['yr_upt']
            yr_vrh = x['yr_vrh']
            yr_pph = round(yr_upt/yr_vrh, 2)
        else:
            yr_pph = 0

        if upt['cc_upt'] and upt['cc_upt'] > 0 and x['cc_vrh'] and x['cc_vrh'] > 0:
            cc_upt = upt['cc_upt']
            cc_vrh = x['cc_vrh']
            cc_pph = round(cc_upt/cc_vrh, 2)
        else:
            cc_pph = 0

        if upt['mg_upt'] and upt['mg_upt'] > 0 and x['mg_vrh'] and x['mg_vrh'] > 0:
            mg_upt = upt['mg_upt']
            mg_vrh = x['mg_vrh']
            mg_pph = round(mg_upt/mg_vrh, 2)
        else:
            mg_pph = 0

        if upt['ip_upt'] and upt['ip_upt'] > 0 and x['ip_vrh'] and x['ip_vrh'] > 0:
            ip_upt = upt['ip_upt']
            ip_vrh = x['ip_vrh']
            ip_pph = round(ip_upt/ip_vrh, 2)
        else:
            ip_pph = 0

        if upt['ar_upt'] and upt['ar_upt'] > 0 and x['ar_vrh'] and x['ar_vrh'] > 0:
            ar_upt = upt['ar_upt']
            ar_vrh = x['ar_vrh']
            ar_pph = round(ar_upt/ar_vrh, 2)
        else:
            ar_pph = 0

        if upt['other_rail_upt'] and upt['other_rail_upt'] > 0 and x['other_rail_vrh'] and x['other_rail_vrh'] > 0:
            other_rail_upt = upt['other_rail_upt']
            other_rail_vrh = x['other_rail_vrh']
            other_rail_pph = round(other_rail_upt/other_rail_vrh, 2)
        else:
            other_rail_pph = 0

        if upt['dr_upt'] and upt['dr_upt'] > 0 and x['dr_vrh'] and x['dr_vrh'] > 0:
            dr_upt = upt['dr_upt']
            dr_vrh = x['dr_vrh']
            dr_pph = round(dr_upt/dr_vrh, 2)
        else:
            dr_pph = 0

        if upt['dt_upt'] and upt['dt_upt'] > 0 and x['dt_vrh'] and x['dt_vrh'] > 0:
            dt_upt = upt['dt_upt']
            dt_vrh = x['dt_vrh']
            dt_pph = round(dt_upt/dt_vrh, 2)
        else:
            dt_pph = 0

        if upt['vp_upt'] and upt['vp_upt'] > 0 and x['vp_vrh'] and x['vp_vrh'] > 0:
            vp_upt = upt['vp_upt']
            vp_vrh = x['vp_vrh']
            vp_pph = round(vp_upt/vp_vrh, 2)
        else:
            vp_pph = 0

        if upt['jt_upt'] and upt['jt_upt'] > 0 and x['jt_vrh'] and x['jt_vrh'] > 0:
            jt_upt = upt['jt_upt']
            jt_vrh = x['jt_vrh']
            jt_pph = round(jt_upt/jt_vrh, 2)
        else:
            jt_pph = 0

        if upt['fb_upt'] and upt['fb_upt'] > 0 and x['fb_vrh'] and x['fb_vrh'] > 0:
            fb_upt = upt['fb_upt']
            fb_vrh = x['fb_vrh']
            fb_pph = round(fb_upt/fb_vrh, 2)
        else:
            fb_pph = 0

        if upt['tr_upt'] and upt['tr_upt'] > 0 and x['tr_vrh'] and x['tr_vrh'] > 0:
            tr_upt = upt['tr_upt']
            tr_vrh = x['tr_vrh']
            tr_pph = round(tr_upt/tr_vrh, 2)
        else:
            tr_pph = 0

        if upt['ot_upt'] and upt['ot_upt'] > 0 and x['ot_vrh'] and x['ot_vrh'] > 0:
            ot_upt = upt['ot_upt']
            ot_vrh = x['ot_vrh']
            ot_pph = round(ot_upt/ot_vrh, 2)
        else:
            ot_pph = 0

        data += [{"year": x['year'], "mb": mb_pph, "cb": cb_pph, "rb": rb_pph, "tb": tb_pph, "pb": pb_pph, "hr": hr_pph, "cr": cr_pph, "lr": lr_pph, "yr": yr_pph, "cc": cc_pph, "mg": mg_pph, "ip": ip_pph, "ar": ar_pph, "other_rail": other_rail_pph, "dr": dr_pph, "dt": dt_pph, "vp": vp_pph, "jt": jt_pph, "fb": fb_pph, "tr": tr_pph, "ot": ot_pph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_per_vrm_by_mode(request):
    filters, q = process_params(request.GET)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(mb_upt=Round(Sum(F('upt'), filter=Q(mode_id="MB"))), \
                                 cb_upt=Round(Sum(F('upt'), filter=Q(mode_id="CB"))), \
                                 rb_upt=Round(Sum(F('upt'), filter=Q(mode_id="RB"))), \
                                 tb_upt=Round(Sum(F('upt'), filter=Q(mode_id="TB"))), \
                                 pb_upt=Round(Sum(F('upt'), filter=Q(mode_id="PB"))), \
                                 hr_upt=Round(Sum(F('upt'), filter=Q(mode_id="HR"))), \
                                 lr_upt=Round(Sum(F('upt'), filter=Q(mode_id="LR"))), \
                                 cr_upt=Round(Sum(F('upt'), filter=Q(mode_id="CR"))), \
                                 yr_upt=Round(Sum(F('upt'), filter=Q(mode_id="YR"))), \
                                 sr_upt=Round(Sum(F('upt'), filter=Q(mode_id="SR"))), \
                                 cc_upt=Round(Sum(F('upt'), filter=Q(mode_id="CC"))), \
                                 mg_upt=Round(Sum(F('upt'), filter=Q(mode_id="MG"))), \
                                 ip_upt=Round(Sum(F('upt'), filter=Q(mode_id="IP"))), \
                                 ar_upt=Round(Sum(F('upt'), filter=Q(mode_id="AR"))), \
                                 other_rail_upt=Round(Sum(F('upt'), filter=Q(mode_id="OR"))), \
                                 dr_upt=Round(Sum(F('upt'), filter=Q(mode_id="DR"))), \
                                 dt_upt=Round(Sum(F('upt'), filter=Q(mode_id="DT"))), \
                                 vp_upt=Round(Sum(F('upt'), filter=Q(mode_id="VP"))), \
                                 jt_upt=Round(Sum(F('upt'), filter=Q(mode_id="JT"))), \
                                 fb_upt=Round(Sum(F('upt'), filter=Q(mode_id="FB"))), \
                                 tr_upt=Round(Sum(F('upt'), filter=Q(mode_id="TR"))), \
                                 ot_upt=Round(Sum(F('upt'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(mb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="MB"))), \
                                 cb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CB"))), \
                                 rb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="RB"))), \
                                 tb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="TB"))), \
                                 pb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="PB"))), \
                                 hr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="HR"))), \
                                 lr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="LR"))), \
                                 cr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CR"))), \
                                 yr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="YR"))), \
                                 sr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="SR"))), \
                                 cc_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CC"))), \
                                 mg_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="MG"))), \
                                 ip_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="IP"))), \
                                 ar_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="AR"))), \
                                 other_rail_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="OR"))), \
                                 dr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="DR"))), \
                                 dt_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="DT"))), \
                                 vp_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="VP"))), \
                                 jt_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="JT"))), \
                                 fb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="FB"))), \
                                 tr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="TR"))), \
                                 ot_vrm=Round(Sum(F('vrm'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in vrm_ts:

        upt = upt_ts.get(year=x['year'])

        if upt['mb_upt'] and upt['mb_upt'] > 0 and x['mb_vrm'] and x['mb_vrm'] > 0:
            mb_upt = upt['mb_upt']
            mb_vrm = x['mb_vrm']
            mb_ppm = round(mb_upt/mb_vrm, 2)
        else:
            mb_ppm = 0

        if upt['cb_upt'] and upt['cb_upt'] > 0 and x['cb_vrm'] and x['cb_vrm'] > 0:
            cb_upt = upt['cb_upt']
            cb_vrm = x['cb_vrm']
            cb_ppm = round(cb_upt/cb_vrm, 2)
        else:
            cb_ppm = 0

        if upt['rb_upt'] and upt['rb_upt'] > 0 and x['rb_vrm'] and x['rb_vrm'] > 0:
            rb_upt = upt['rb_upt']
            rb_vrm = x['rb_vrm']
            rb_ppm = round(rb_upt/rb_vrm, 2)
        else:
            rb_ppm = 0

        if upt['tb_upt'] and upt['tb_upt'] > 0 and x['tb_vrm'] and x['tb_vrm'] > 0:
            tb_upt = upt['tb_upt']
            tb_vrm = x['tb_vrm']
            tb_ppm = round(tb_upt/tb_vrm, 2)
        else:
            tb_ppm = 0

        if upt['pb_upt'] and upt['pb_upt'] > 0 and x['pb_vrm'] and x['pb_vrm'] > 0:
            pb_upt = upt['pb_upt']
            pb_vrm = x['pb_vrm']
            pb_ppm = round(pb_upt/pb_vrm, 2)
        else:
            pb_ppm = 0

        if upt['hr_upt'] and upt['hr_upt'] > 0 and x['hr_vrm'] and x['hr_vrm'] > 0:
            hr_upt = upt['hr_upt']
            hr_vrm = x['hr_vrm']
            hr_ppm = round(hr_upt/hr_vrm, 2)
        else:
            hr_ppm = 0

        if upt['lr_upt'] and upt['lr_upt'] > 0 and x['lr_vrm'] and x['lr_vrm'] > 0:
            lr_upt = upt['lr_upt']
            lr_vrm = x['lr_vrm']
            lr_ppm = round(lr_upt/lr_vrm, 2)
        else:
            lr_ppm = 0

        if upt['cr_upt'] and upt['cr_upt'] > 0 and x['cr_vrm'] and x['cr_vrm'] > 0:
            cr_upt = upt['cr_upt']
            cr_vrm = x['cr_vrm']
            cr_ppm = round(cr_upt/cr_vrm, 2)
        else:
            cr_ppm = 0

        if upt['yr_upt'] and upt['yr_upt'] > 0 and x['yr_vrm'] and x['yr_vrm'] > 0:
            yr_upt = upt['yr_upt']
            yr_vrm = x['yr_vrm']
            yr_ppm = round(yr_upt/yr_vrm, 2)
        else:
            yr_ppm = 0

        if upt['cc_upt'] and upt['cc_upt'] > 0 and x['cc_vrm'] and x['cc_vrm'] > 0:
            cc_upt = upt['cc_upt']
            cc_vrm = x['cc_vrm']
            cc_ppm = round(cc_upt/cc_vrm, 2)
        else:
            cc_ppm = 0

        if upt['mg_upt'] and upt['mg_upt'] > 0 and x['mg_vrm'] and x['mg_vrm'] > 0:
            mg_upt = upt['mg_upt']
            mg_vrm = x['mg_vrm']
            mg_ppm = round(mg_upt/mg_vrm, 2)
        else:
            mg_ppm = 0

        if upt['ip_upt'] and upt['ip_upt'] > 0 and x['ip_vrm'] and x['ip_vrm'] > 0:
            ip_upt = upt['ip_upt']
            ip_vrm = x['ip_vrm']
            ip_ppm = round(ip_upt/ip_vrm, 2)
        else:
            ip_ppm = 0

        if upt['ar_upt'] and upt['ar_upt'] > 0 and x['ar_vrm'] and x['ar_vrm'] > 0:
            ar_upt = upt['ar_upt']
            ar_vrm = x['ar_vrm']
            ar_ppm = round(ar_upt/ar_vrm, 2)
        else:
            ar_ppm = 0

        if upt['other_rail_upt'] and upt['other_rail_upt'] > 0 and x['other_rail_vrm'] and x['other_rail_vrm'] > 0:
            other_rail_upt = upt['other_rail_upt']
            other_rail_vrm = x['other_rail_vrm']
            other_rail_ppm = round(other_rail_upt/other_rail_vrm, 2)
        else:
            other_rail_ppm = 0

        if upt['dr_upt'] and upt['dr_upt'] > 0 and x['dr_vrm'] and x['dr_vrm'] > 0:
            dr_upt = upt['dr_upt']
            dr_vrm = x['dr_vrm']
            dr_ppm = round(dr_upt/dr_vrm, 2)
        else:
            dr_ppm = 0

        if upt['dt_upt'] and upt['dt_upt'] > 0 and x['dt_vrm'] and x['dt_vrm'] > 0:
            dt_upt = upt['dt_upt']
            dt_vrm = x['dt_vrm']
            dt_ppm = round(dt_upt/dt_vrm, 2)
        else:
            dt_ppm = 0

        if upt['vp_upt'] and upt['vp_upt'] > 0 and x['vp_vrm'] and x['vp_vrm'] > 0:
            vp_upt = upt['vp_upt']
            vp_vrm = x['vp_vrm']
            vp_ppm = round(vp_upt/vp_vrm, 2)
        else:
            vp_ppm = 0

        if upt['jt_upt'] and upt['jt_upt'] > 0 and x['jt_vrm'] and x['jt_vrm'] > 0:
            jt_upt = upt['jt_upt']
            jt_vrm = x['jt_vrm']
            jt_ppm = round(jt_upt/jt_vrm, 2)
        else:
            jt_ppm = 0

        if upt['fb_upt'] and upt['fb_upt'] > 0 and x['fb_vrm'] and x['fb_vrm'] > 0:
            fb_upt = upt['fb_upt']
            fb_vrm = x['fb_vrm']
            fb_ppm = round(fb_upt/fb_vrm, 2)
        else:
            fb_ppm = 0

        if upt['tr_upt'] and upt['tr_upt'] > 0 and x['tr_vrm'] and x['tr_vrm'] > 0:
            tr_upt = upt['tr_upt']
            tr_vrm = x['tr_vrm']
            tr_ppm = round(tr_upt/tr_vrm, 2)
        else:
            tr_ppm = 0

        if upt['ot_upt'] and upt['ot_upt'] > 0 and x['ot_vrm'] and x['ot_vrm'] > 0:
            ot_upt = upt['ot_upt']
            ot_vrm = x['ot_vrm']
            ot_ppm = round(ot_upt/ot_vrm, 2)
        else:
            ot_ppm = 0

        data += [{"year": x['year'], "mb": mb_ppm, "cb": cb_ppm, "rb": rb_ppm, "tb": tb_ppm, "pb": pb_ppm, "hr": hr_ppm, "cr": cr_ppm, "lr": lr_ppm, "yr": yr_ppm, "cc": cc_ppm, "mg": mg_ppm, "ip": ip_ppm, "ar": ar_ppm, "other_rail": other_rail_ppm, "dr": dr_ppm, "dt": dt_ppm, "vp": vp_ppm, "jt": jt_ppm, "fb": fb_ppm, "tr": tr_ppm, "ot": ot_ppm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_per_vrh_by_mode(request):
    filters, q = process_params(request.GET)
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(mb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="MB"))), \
                                 cb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CB"))), \
                                 rb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="RB"))), \
                                 tb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="TB"))), \
                                 pb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="PB"))), \
                                 hr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="HR"))), \
                                 lr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="LR"))), \
                                 cr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CR"))), \
                                 yr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="YR"))), \
                                 sr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="SR"))), \
                                 cc_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CC"))), \
                                 mg_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="MG"))), \
                                 ip_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="IP"))), \
                                 ar_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="AR"))), \
                                 other_rail_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="OR"))), \
                                 dr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="DR"))), \
                                 dt_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="DT"))), \
                                 vp_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="VP"))), \
                                 jt_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="JT"))), \
                                 fb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="FB"))), \
                                 tr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="TR"))), \
                                 ot_pmt=Round(Sum(F('pmt'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
        .values("year").annotate(mb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="MB"))), \
                                 cb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CB"))), \
                                 rb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="RB"))), \
                                 tb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="TB"))), \
                                 pb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="PB"))), \
                                 hr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="HR"))), \
                                 lr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="LR"))), \
                                 cr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CR"))), \
                                 yr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="YR"))), \
                                 sr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="SR"))), \
                                 cc_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="CC"))), \
                                 mg_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="MG"))), \
                                 ip_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="IP"))), \
                                 ar_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="AR"))), \
                                 other_rail_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="OR"))), \
                                 dr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="DR"))), \
                                 dt_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="DT"))), \
                                 vp_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="VP"))), \
                                 jt_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="JT"))), \
                                 fb_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="FB"))), \
                                 tr_vrh=Round(Sum(F('vrh'), filter=Q(mode_id="TR"))), \
                                 ot_vrh=Round(Sum(F('vrh'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in vrh_ts:

        pmt = pmt_ts.get(year=x['year'])

        if pmt['mb_pmt'] and pmt['mb_pmt'] > 0 and x['mb_vrh'] and x['mb_vrh'] > 0:
            mb_pmt = pmt['mb_pmt']
            mb_vrh = x['mb_vrh']
            mb_pmph = round(mb_pmt/mb_vrh, 2)
        else:
            mb_pmph = 0

        if pmt['cb_pmt'] and pmt['cb_pmt'] > 0 and x['cb_vrh'] and x['cb_vrh'] > 0:
            cb_pmt = pmt['cb_pmt']
            cb_vrh = x['cb_vrh']
            cb_pmph = round(cb_pmt/cb_vrh, 2)
        else:
            cb_pmph = 0

        if pmt['rb_pmt'] and pmt['rb_pmt'] > 0 and x['rb_vrh'] and x['rb_vrh'] > 0:
            rb_pmt = pmt['rb_pmt']
            rb_vrh = x['rb_vrh']
            rb_pmph = round(rb_pmt/rb_vrh, 2)
        else:
            rb_pmph = 0

        if pmt['tb_pmt'] and pmt['tb_pmt'] > 0 and x['tb_vrh'] and x['tb_vrh'] > 0:
            tb_pmt = pmt['tb_pmt']
            tb_vrh = x['tb_vrh']
            tb_pmph = round(tb_pmt/tb_vrh, 2)
        else:
            tb_pmph = 0

        if pmt['pb_pmt'] and pmt['pb_pmt'] > 0 and x['pb_vrh'] and x['pb_vrh'] > 0:
            pb_pmt = pmt['pb_pmt']
            pb_vrh = x['pb_vrh']
            pb_pmph = round(pb_pmt/pb_vrh, 2)
        else:
            pb_pmph = 0

        if pmt['hr_pmt'] and pmt['hr_pmt'] > 0 and x['hr_vrh'] and x['hr_vrh'] > 0:
            hr_pmt = pmt['hr_pmt']
            hr_vrh = x['hr_vrh']
            hr_pmph = round(hr_pmt/hr_vrh, 2)
        else:
            hr_pmph = 0

        if pmt['lr_pmt'] and pmt['lr_pmt'] > 0 and x['lr_vrh'] and x['lr_vrh'] > 0:
            lr_pmt = pmt['lr_pmt']
            lr_vrh = x['lr_vrh']
            lr_pmph = round(lr_pmt/lr_vrh, 2)
        else:
            lr_pmph = 0

        if pmt['cr_pmt'] and pmt['cr_pmt'] > 0 and x['cr_vrh'] and x['cr_vrh'] > 0:
            cr_pmt = pmt['cr_pmt']
            cr_vrh = x['cr_vrh']
            cr_pmph = round(cr_pmt/cr_vrh, 2)
        else:
            cr_pmph = 0

        if pmt['yr_pmt'] and pmt['yr_pmt'] > 0 and x['yr_vrh'] and x['yr_vrh'] > 0:
            yr_pmt = pmt['yr_pmt']
            yr_vrh = x['yr_vrh']
            yr_pmph = round(yr_pmt/yr_vrh, 2)
        else:
            yr_pmph = 0

        if pmt['cc_pmt'] and pmt['cc_pmt'] > 0 and x['cc_vrh'] and x['cc_vrh'] > 0:
            cc_pmt = pmt['cc_pmt']
            cc_vrh = x['cc_vrh']
            cc_pmph = round(cc_pmt/cc_vrh, 2)
        else:
            cc_pmph = 0

        if pmt['mg_pmt'] and pmt['mg_pmt'] > 0 and x['mg_vrh'] and x['mg_vrh'] > 0:
            mg_pmt = pmt['mg_pmt']
            mg_vrh = x['mg_vrh']
            mg_pmph = round(mg_pmt/mg_vrh, 2)
        else:
            mg_pmph = 0

        if pmt['ip_pmt'] and pmt['ip_pmt'] > 0 and x['ip_vrh'] and x['ip_vrh'] > 0:
            ip_pmt = pmt['ip_pmt']
            ip_vrh = x['ip_vrh']
            ip_pmph = round(ip_pmt/ip_vrh, 2)
        else:
            ip_pmph = 0

        if pmt['ar_pmt'] and pmt['ar_pmt'] > 0 and x['ar_vrh'] and x['ar_vrh'] > 0:
            ar_pmt = pmt['ar_pmt']
            ar_vrh = x['ar_vrh']
            ar_pmph = round(ar_pmt/ar_vrh, 2)
        else:
            ar_pmph = 0

        if pmt['other_rail_pmt'] and pmt['other_rail_pmt'] > 0 and x['other_rail_vrh'] and x['other_rail_vrh'] > 0:
            other_rail_pmt = pmt['other_rail_pmt']
            other_rail_vrh = x['other_rail_vrh']
            other_rail_pmph = round(other_rail_pmt/other_rail_vrh, 2)
        else:
            other_rail_pmph = 0

        if pmt['dr_pmt'] and pmt['dr_pmt'] > 0 and x['dr_vrh'] and x['dr_vrh'] > 0:
            dr_pmt = pmt['dr_pmt']
            dr_vrh = x['dr_vrh']
            dr_pmph = round(dr_pmt/dr_vrh, 2)
        else:
            dr_pmph = 0

        if pmt['dt_pmt'] and pmt['dt_pmt'] > 0 and x['dt_vrh'] and x['dt_vrh'] > 0:
            dt_pmt = pmt['dt_pmt']
            dt_vrh = x['dt_vrh']
            dt_pmph = round(dt_pmt/dt_vrh, 2)
        else:
            dt_pmph = 0

        if pmt['vp_pmt'] and pmt['vp_pmt'] > 0 and x['vp_vrh'] and x['vp_vrh'] > 0:
            vp_pmt = pmt['vp_pmt']
            vp_vrh = x['vp_vrh']
            vp_pmph = round(vp_pmt/vp_vrh, 2)
        else:
            vp_pmph = 0

        if pmt['jt_pmt'] and pmt['jt_pmt'] > 0 and x['jt_vrh'] and x['jt_vrh'] > 0:
            jt_pmt = pmt['jt_pmt']
            jt_vrh = x['jt_vrh']
            jt_pmph = round(jt_pmt/jt_vrh, 2)
        else:
            jt_pmph = 0

        if pmt['fb_pmt'] and pmt['fb_pmt'] > 0 and x['fb_vrh'] and x['fb_vrh'] > 0:
            fb_pmt = pmt['fb_pmt']
            fb_vrh = x['fb_vrh']
            fb_pmph = round(fb_pmt/fb_vrh, 2)
        else:
            fb_pmph = 0

        if pmt['tr_pmt'] and pmt['tr_pmt'] > 0 and x['tr_vrh'] and x['tr_vrh'] > 0:
            tr_pmt = pmt['tr_pmt']
            tr_vrh = x['tr_vrh']
            tr_pmph = round(tr_pmt/tr_vrh, 2)
        else:
            tr_pmph = 0

        if pmt['ot_pmt'] and pmt['ot_pmt'] > 0 and x['ot_vrh'] and x['ot_vrh'] > 0:
            ot_pmt = pmt['ot_pmt']
            ot_vrh = x['ot_vrh']
            ot_pmph = round(ot_pmt/ot_vrh, 2)
        else:
            ot_pmph = 0

        data += [{"year": x['year'], "mb": mb_pmph, "cb": cb_pmph, "rb": rb_pmph, "tb": tb_pmph, "pb": pb_pmph, "hr": hr_pmph, "cr": cr_pmph, "lr": lr_pmph, "yr": yr_pmph, "cc": cc_pmph, "mg": mg_pmph, "ip": ip_pmph, "ar": ar_pmph, "other_rail": other_rail_pmph, "dr": dr_pmph, "dt": dt_pmph, "vp": vp_pmph, "jt": jt_pmph, "fb": fb_pmph, "tr": tr_pmph, "ot": ot_pmph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_per_vrm_by_mode(request):
    filters, q = process_params(request.GET)
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(mb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="MB"))), \
                                 cb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CB"))), \
                                 rb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="RB"))), \
                                 tb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="TB"))), \
                                 pb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="PB"))), \
                                 hr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="HR"))), \
                                 lr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="LR"))), \
                                 cr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CR"))), \
                                 yr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="YR"))), \
                                 sr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="SR"))), \
                                 cc_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="CC"))), \
                                 mg_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="MG"))), \
                                 ip_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="IP"))), \
                                 ar_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="AR"))), \
                                 other_rail_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="OR"))), \
                                 dr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="DR"))), \
                                 dt_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="DT"))), \
                                 vp_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="VP"))), \
                                 jt_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="JT"))), \
                                 fb_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="FB"))), \
                                 tr_pmt=Round(Sum(F('pmt'), filter=Q(mode_id="TR"))), \
                                 ot_pmt=Round(Sum(F('pmt'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
        .values("year").annotate(mb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="MB"))), \
                                 cb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CB"))), \
                                 rb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="RB"))), \
                                 tb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="TB"))), \
                                 pb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="PB"))), \
                                 hr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="HR"))), \
                                 lr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="LR"))), \
                                 cr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CR"))), \
                                 yr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="YR"))), \
                                 sr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="SR"))), \
                                 cc_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="CC"))), \
                                 mg_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="MG"))), \
                                 ip_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="IP"))), \
                                 ar_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="AR"))), \
                                 other_rail_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="OR"))), \
                                 dr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="DR"))), \
                                 dt_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="DT"))), \
                                 vp_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="VP"))), \
                                 jt_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="JT"))), \
                                 fb_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="FB"))), \
                                 tr_vrm=Round(Sum(F('vrm'), filter=Q(mode_id="TR"))), \
                                 ot_vrm=Round(Sum(F('vrm'), filter=Q(mode_id__in=["OT", "nan"])))).\
        order_by('year')
    data = []
    for x in vrm_ts:

        pmt = pmt_ts.get(year=x['year'])

        if pmt['mb_pmt'] and pmt['mb_pmt'] > 0 and x['mb_vrm'] and x['mb_vrm'] > 0:
            mb_pmt = pmt['mb_pmt']
            mb_vrm = x['mb_vrm']
            mb_pmpm = round(mb_pmt/mb_vrm, 2)
        else:
            mb_pmpm = 0

        if pmt['cb_pmt'] and pmt['cb_pmt'] > 0 and x['cb_vrm'] and x['cb_vrm'] > 0:
            cb_pmt = pmt['cb_pmt']
            cb_vrm = x['cb_vrm']
            cb_pmpm = round(cb_pmt/cb_vrm, 2)
        else:
            cb_pmpm = 0

        if pmt['rb_pmt'] and pmt['rb_pmt'] > 0 and x['rb_vrm'] and x['rb_vrm'] > 0:
            rb_pmt = pmt['rb_pmt']
            rb_vrm = x['rb_vrm']
            rb_pmpm = round(rb_pmt/rb_vrm, 2)
        else:
            rb_pmpm = 0

        if pmt['tb_pmt'] and pmt['tb_pmt'] > 0 and x['tb_vrm'] and x['tb_vrm'] > 0:
            tb_pmt = pmt['tb_pmt']
            tb_vrm = x['tb_vrm']
            tb_pmpm = round(tb_pmt/tb_vrm, 2)
        else:
            tb_pmpm = 0

        if pmt['pb_pmt'] and pmt['pb_pmt'] > 0 and x['pb_vrm'] and x['pb_vrm'] > 0:
            pb_pmt = pmt['pb_pmt']
            pb_vrm = x['pb_vrm']
            pb_pmpm = round(pb_pmt/pb_vrm, 2)
        else:
            pb_pmpm = 0

        if pmt['hr_pmt'] and pmt['hr_pmt'] > 0 and x['hr_vrm'] and x['hr_vrm'] > 0:
            hr_pmt = pmt['hr_pmt']
            hr_vrm = x['hr_vrm']
            hr_pmpm = round(hr_pmt/hr_vrm, 2)
        else:
            hr_pmpm = 0

        if pmt['lr_pmt'] and pmt['lr_pmt'] > 0 and x['lr_vrm'] and x['lr_vrm'] > 0:
            lr_pmt = pmt['lr_pmt']
            lr_vrm = x['lr_vrm']
            lr_pmpm = round(lr_pmt/lr_vrm, 2)
        else:
            lr_pmpm = 0

        if pmt['cr_pmt'] and pmt['cr_pmt'] > 0 and x['cr_vrm'] and x['cr_vrm'] > 0:
            cr_pmt = pmt['cr_pmt']
            cr_vrm = x['cr_vrm']
            cr_pmpm = round(cr_pmt/cr_vrm, 2)
        else:
            cr_pmpm = 0

        if pmt['yr_pmt'] and pmt['yr_pmt'] > 0 and x['yr_vrm'] and x['yr_vrm'] > 0:
            yr_pmt = pmt['yr_pmt']
            yr_vrm = x['yr_vrm']
            yr_pmpm = round(yr_pmt/yr_vrm, 2)
        else:
            yr_pmpm = 0

        if pmt['cc_pmt'] and pmt['cc_pmt'] > 0 and x['cc_vrm'] and x['cc_vrm'] > 0:
            cc_pmt = pmt['cc_pmt']
            cc_vrm = x['cc_vrm']
            cc_pmpm = round(cc_pmt/cc_vrm, 2)
        else:
            cc_pmpm = 0

        if pmt['mg_pmt'] and pmt['mg_pmt'] > 0 and x['mg_vrm'] and x['mg_vrm'] > 0:
            mg_pmt = pmt['mg_pmt']
            mg_vrm = x['mg_vrm']
            mg_pmpm = round(mg_pmt/mg_vrm, 2)
        else:
            mg_pmpm = 0

        if pmt['ip_pmt'] and pmt['ip_pmt'] > 0 and x['ip_vrm'] and x['ip_vrm'] > 0:
            ip_pmt = pmt['ip_pmt']
            ip_vrm = x['ip_vrm']
            ip_pmpm = round(ip_pmt/ip_vrm, 2)
        else:
            ip_pmpm = 0

        if pmt['ar_pmt'] and pmt['ar_pmt'] > 0 and x['ar_vrm'] and x['ar_vrm'] > 0:
            ar_pmt = pmt['ar_pmt']
            ar_vrm = x['ar_vrm']
            ar_pmpm = round(ar_pmt/ar_vrm, 2)
        else:
            ar_pmpm = 0

        if pmt['other_rail_pmt'] and pmt['other_rail_pmt'] > 0 and x['other_rail_vrm'] and x['other_rail_vrm'] > 0:
            other_rail_pmt = pmt['other_rail_pmt']
            other_rail_vrm = x['other_rail_vrm']
            other_rail_pmpm = round(other_rail_pmt/other_rail_vrm, 2)
        else:
            other_rail_pmpm = 0

        if pmt['dr_pmt'] and pmt['dr_pmt'] > 0 and x['dr_vrm'] and x['dr_vrm'] > 0:
            dr_pmt = pmt['dr_pmt']
            dr_vrm = x['dr_vrm']
            dr_pmpm = round(dr_pmt/dr_vrm, 2)
        else:
            dr_pmpm = 0

        if pmt['dt_pmt'] and pmt['dt_pmt'] > 0 and x['dt_vrm'] and x['dt_vrm'] > 0:
            dt_pmt = pmt['dt_pmt']
            dt_vrm = x['dt_vrm']
            dt_pmpm = round(dt_pmt/dt_vrm, 2)
        else:
            dt_pmpm = 0

        if pmt['vp_pmt'] and pmt['vp_pmt'] > 0 and x['vp_vrm'] and x['vp_vrm'] > 0:
            vp_pmt = pmt['vp_pmt']
            vp_vrm = x['vp_vrm']
            vp_pmpm = round(vp_pmt/vp_vrm, 2)
        else:
            vp_pmpm = 0

        if pmt['jt_pmt'] and pmt['jt_pmt'] > 0 and x['jt_vrm'] and x['jt_vrm'] > 0:
            jt_pmt = pmt['jt_pmt']
            jt_vrm = x['jt_vrm']
            jt_pmpm = round(jt_pmt/jt_vrm, 2)
        else:
            jt_pmpm = 0

        if pmt['fb_pmt'] and pmt['fb_pmt'] > 0 and x['fb_vrm'] and x['fb_vrm'] > 0:
            fb_pmt = pmt['fb_pmt']
            fb_vrm = x['fb_vrm']
            fb_pmpm = round(fb_pmt/fb_vrm, 2)
        else:
            fb_pmpm = 0

        if pmt['tr_pmt'] and pmt['tr_pmt'] > 0 and x['tr_vrm'] and x['tr_vrm'] > 0:
            tr_pmt = pmt['tr_pmt']
            tr_vrm = x['tr_vrm']
            tr_pmpm = round(tr_pmt/tr_vrm, 2)
        else:
            tr_pmpm = 0

        if pmt['ot_pmt'] and pmt['ot_pmt'] > 0 and x['ot_vrm'] and x['ot_vrm'] > 0:
            ot_pmt = pmt['ot_pmt']
            ot_vrm = x['ot_vrm']
            ot_pmpm = round(ot_pmt/ot_vrm, 2)
        else:
            ot_pmpm = 0

        data += [{"year": x['year'], "mb": mb_pmpm, "cb": cb_pmpm, "rb": rb_pmpm, "tb": tb_pmpm, "pb": pb_pmpm, "hr": hr_pmpm, "cr": cr_pmpm, "lr": lr_pmpm, "yr": yr_pmpm, "cc": cc_pmpm, "mg": mg_pmpm, "ip": ip_pmpm, "ar": ar_pmpm, "other_rail": other_rail_pmpm, "dr": dr_pmpm, "dt": dt_pmpm, "vp": vp_pmpm, "jt": jt_pmpm, "fb": fb_pmpm, "tr": tr_pmpm, "ot": ot_pmpm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)




@csrf_exempt
def cost_per_upt_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(
            do_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", service_id="DO")),
            pt_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", service_id="PT")),
            tx_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", service_id="TX")),
            other_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", service_id__in=["TN", "nan"]))
        )\
        .order_by('year')
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(
            do_upt=Sum(F("upt"), filter=Q(service_id="DO")),
            pt_upt=Sum(F("upt"), filter=Q(service_id="PT")),
            tx_upt=Sum(F("upt"), filter=Q(service_id="TX")),
            other_upt=Sum(F("upt"), filter=Q(service_id__in=["TN", "nan"])),
        ).order_by('year')
    data = []

    for x in spending_ts:

        ridership = upt_ts.get(year=x['year'])

        if ridership['do_upt'] and ridership['do_upt'] > 0 and x['do_opexp'] and x['do_opexp'] > 0:
            do_upt = ridership['do_upt']
            do_opexp = x['do_opexp']
            do_cpp = round(do_opexp/do_upt, 2)
        else:
            do_cpp = 0
        if ridership['pt_upt'] and ridership['pt_upt'] > 0 and x['pt_opexp'] and x['pt_opexp'] > 0:
            pt_upt = ridership['pt_upt']
            pt_opexp = x['pt_opexp']
            pt_cpp = round(pt_opexp/pt_upt, 2)
        else:
            pt_cpp = 0
        if ridership['tx_upt'] and ridership['tx_upt'] > 0 and x['tx_opexp'] and x['tx_opexp'] > 0:
            tx_upt = ridership['tx_upt']
            tx_opexp = x['tx_opexp']
            tx_cpp = round(tx_opexp/tx_upt, 2)
        else:
            tx_cpp = 0
        if ridership['other_upt'] and ridership['other_upt'] > 0 and x['other_opexp'] and x['other_opexp'] > 0:
            other_upt = ridership['other_upt']
            other_opexp = x['other_opexp']
            other_cpp = round(other_opexp/other_upt, 2)
        else:
            other_cpp = 0

        data += [{"year": x['year'], "do": do_cpp, "pt": pt_cpp, "tx": tx_cpp, "other": other_cpp}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def cost_per_pmt_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(
            do_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", service_id="DO")),
            pt_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", service_id="PT")),
            tx_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", service_id="TX")),
            other_opexp=Sum(F('expense')*F("year_id__in_todays_dollars"), filter=Q(expense_type_id__budget="Operating", service_id__in=["TN", "nan"]))
        )\
        .order_by('year')
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
        .values("year").annotate(
            do_pmt=Sum(F("pmt"), filter=Q(service_id="DO")),
            pt_pmt=Sum(F("pmt"), filter=Q(service_id="PT")),
            tx_pmt=Sum(F("pmt"), filter=Q(service_id="TX")),
            other_pmt=Sum(F("pmt"), filter=Q(service_id__in=["TN", "nan"])),
        ).order_by('year')
    data = []

    for x in spending_ts:

        ridership = pmt_ts.get(year=x['year'])

        if ridership['do_pmt'] and ridership['do_pmt'] > 0 and x['do_opexp'] and x['do_opexp'] > 0:
            do_pmt = ridership['do_pmt']
            do_opexp = x['do_opexp']
            do_cpp = round(do_opexp/do_pmt, 2)
        else:
            do_cpp = 0
        if ridership['pt_pmt'] and ridership['pt_pmt'] > 0 and x['pt_opexp'] and x['pt_opexp'] > 0:
            pt_pmt = ridership['pt_pmt']
            pt_opexp = x['pt_opexp']
            pt_cpp = round(pt_opexp/pt_pmt, 2)
        else:
            pt_cpp = 0
        if ridership['tx_pmt'] and ridership['tx_pmt'] > 0 and x['tx_opexp'] and x['tx_opexp'] > 0:
            tx_pmt = ridership['tx_pmt']
            tx_opexp = x['tx_opexp']
            tx_cpp = round(tx_opexp/tx_pmt, 2)
        else:
            tx_cpp = 0
        if ridership['other_pmt'] and ridership['other_pmt'] > 0 and x['other_opexp'] and x['other_opexp'] > 0:
            other_pmt = ridership['other_pmt']
            other_opexp = x['other_opexp']
            other_cpp = round(other_opexp/other_pmt, 2)
        else:
            other_cpp = 0

        data += [{"year": x['year'], "do": do_cpp, "pt": pt_cpp, "tx": tx_cpp, "other": other_cpp}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def frr_by_service(request):
    filters, q = process_params(request.GET)
    # ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
    spending_ts = TransitExpense.objects.filter(q)\
        .values("year").annotate(
            do_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", service_id="DO")),
            pt_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", service_id="PT")),
            tx_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", service_id="TX")),
            other_opexp=Sum(F('expense'), filter=Q(expense_type_id__budget="Operating", service_id__in=["TN", "nan"]))
        )\
        .order_by('year')
    fares_ts = Fares.objects.filter(q)\
        .values("year").annotate(
            do_fares=Sum(F('fares'), service_id="DO"),
            pt_fares=Sum(F('fares'), service_id="PT"),
            tx_fares=Sum(F('fares'), service_id="TX"),
            other_fares=Sum(F('fares'), service_id__in=["DO", "nan"]),
        )\
        .order_by('year')
    data = []

    for x in spending_ts:
        revenue = fares_ts.get(year=x['year'])

        if x['do_opexp'] and x['do_opexp'] > 0 and revenue['do_fares'] and revenue['do_fares'] > 0:
            do_opexp = x['do_opexp']
            do_fares=revenue['do_fares']
            do_frr = round(do_fares/do_opexp, 4)
        else:
            do_frr = 0
        if x['pt_opexp'] and x['pt_opexp'] > 0 and revenue['pt_fares'] and revenue['pt_fares'] > 0:
            pt_opexp = x['pt_opexp']
            pt_fares=revenue['pt_fares']
            pt_frr = round(pt_fares/pt_opexp, 4)
        else: 
            pt_frr = 0
        if x['tx_opexp'] and x['tx_opexp'] > 0 and revenue['tx_fares'] and revenue['tx_fares'] > 0:
            tx_opexp = x['tx_opexp']
            tx_fares=revenue['tx_fares']
            tx_frr = round(tx_fares/tx_opexp, 4)
        else: 
            tx_frr = 0
        if x['other_opexp'] and x['other_opexp'] > 0 and revenue['other_fares'] and revenue['other_fares'] > 0:
            other_opexp = x['other_opexp']
            other_fares=revenue['other_fares']
            other_frr = round(other_fares/other_opexp, 4)
        else: 
            other_frr = 0
    
        data += [{"year": x['year'], "do": do_frr, "pt": pt_frr, "tx": tx_frr, "other": other_frr}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

# @csrf_exempt
# def cost_per_vrh_by_service(request):
#     return(JsonResponse({}))

# @csrf_exempt
# def cost_per_vrm_by_service(request):
#     return(JsonResponse({}))

@csrf_exempt
def vrm_per_vrh_by_service(request):
    data = []
    filters, q = process_params(request.GET)
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('vrm'), filter=Q(service_id="DO")),
        pt=Sum(F('vrm'), filter=Q(service_id="PT")),
        tx=Sum(F('vrm'), filter=Q(service_id="TX")),
        other=Sum(F('vrm'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('vrh'), filter=Q(service_id="DO")),
        pt=Sum(F('vrh'), filter=Q(service_id="PT")),
        tx=Sum(F('vrh'), filter=Q(service_id="TX")),
        other=Sum(F('vrh'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    for x in vrh_ts:
        vrm = vrm_ts.get(year=x['year'])
        if x['do'] and x["do"] > 0 and vrm['do'] and vrm['do'] > 0:
            do_vrh = x['do']
            do_vrm = vrm['do']
            do_mph = round(do_vrm / do_vrh, 2)
        else:
            do_mph = 0
        if x['pt'] and x["pt"] > 0 and vrm['pt'] and vrm['pt'] > 0:
            pt_vrh = x['pt']
            pt_vrm = vrm['pt']
            pt_mph = round(pt_vrm / pt_vrh, 2)
        else:
            pt_mph = 0
        if x['tx'] and x["tx"] > 0 and vrm['tx'] and vrm['tx'] > 0:
            tx_vrh = x['tx']
            tx_vrm = vrm['tx']
            tx_mph = round(tx_vrm / tx_vrh, 2)
        else:
            tx_mph = 0
        if x['other'] and x["other"] > 0 and vrm['other'] and vrm['other'] > 0:
            other_vrh = x['other']
            other_vrm = vrm['other']
            other_mph = round(other_vrm / other_vrh, 2)
        else:
            other_mph = 0
        
        data += [{"year": x['year'], "do": do_mph, "pt": pt_mph, "tx": tx_mph, "other": other_mph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_per_vrh_by_service(request):
    data = []
    filters, q = process_params(request.GET)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('upt'), filter=Q(service_id="DO")),
        pt=Sum(F('upt'), filter=Q(service_id="PT")),
        tx=Sum(F('upt'), filter=Q(service_id="TX")),
        other=Sum(F('upt'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('vrh'), filter=Q(service_id="DO")),
        pt=Sum(F('vrh'), filter=Q(service_id="PT")),
        tx=Sum(F('vrh'), filter=Q(service_id="TX")),
        other=Sum(F('vrh'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    for x in vrh_ts:
        upt = upt_ts.get(year=x['year'])

        if x['do'] and x["do"] > 0 and upt['do'] and upt['do'] > 0 :
            do_vrh = x['do']
            do_upt = upt['do']
            do_pph = round(do_upt / do_vrh, 2)
        else:
            do_pph = 0

        if x['pt'] and x["pt"] > 0 and upt['pt'] and upt['pt'] > 0:
            pt_vrh = x['pt']
            pt_upt = upt['pt']
            pt_pph = round(pt_upt / pt_vrh, 2)
        else:
            pt_pph = 0

        if x['tx'] and x["tx"] > 0 and upt['tx'] and upt['tx'] > 0:
            tx_vrh = x['tx']
            tx_upt = upt['tx']
            tx_pph = round(tx_upt / tx_vrh, 2)
        else:
            tx_pph = 0

        if x['other'] and x["other"] > 0 and upt['other'] and upt['other'] > 0:
            other_vrh = x['other']
            other_upt = upt['other']
            other_pph = round(other_upt / other_vrh, 2)
        else:
            other_pph = 0
    
        
        data += [{"year": x['year'], "do": do_pph, "pt": pt_pph, "tx": tx_pph, "other": other_pph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def upt_per_vrm_by_service(request):
    data = []
    filters, q = process_params(request.GET)
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('upt'), filter=Q(service_id="DO")),
        pt=Sum(F('upt'), filter=Q(service_id="PT")),
        tx=Sum(F('upt'), filter=Q(service_id="TX")),
        other=Sum(F('upt'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('vrm'), filter=Q(service_id="DO")),
        pt=Sum(F('vrm'), filter=Q(service_id="PT")),
        tx=Sum(F('vrm'), filter=Q(service_id="TX")),
        other=Sum(F('vrm'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    for x in vrm_ts:
        upt = upt_ts.get(year=x['year'])
        if x['do'] and x["do"] > 0 and upt['do'] and upt['do'] > 0:
            do_vrm = x['do']
            do_upt = upt['do']
            do_ppm = round(do_upt / do_vrm, 2)
        else:
            do_ppm = 0
        if x['pt'] and x["pt"] > 0 and upt['pt'] and  upt['pt'] > 0:
            pt_vrm = x['pt']
            pt_upt = upt['pt']
            pt_ppm = round(pt_upt / pt_vrm, 2)
        else:
            pt_ppm = 0
        if x['tx'] and x["tx"] > 0 and upt['tx'] and upt['tx'] > 0:
            tx_vrm = x['tx']
            tx_upt = upt['tx']
            tx_ppm = round(tx_upt / tx_vrm, 2)
        else:
            tx_ppm = 0
        if x['other'] and x["other"] > 0 and upt['other'] and upt['other'] > 0:
            other_vrm = x['other']
            other_upt = upt['other']
            other_ppm = round(other_upt / other_vrm, 2)
        else:
            other_ppm = 0
        
        data += [{"year": x['year'], "do": do_ppm, "pt": pt_ppm, "tx": tx_ppm, "other": other_ppm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_per_vrh_by_service(request):
    data = []
    filters, q = process_params(request.GET)
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('pmt'), filter=Q(service_id="DO")),
        pt=Sum(F('pmt'), filter=Q(service_id="PT")),
        tx=Sum(F('pmt'), filter=Q(service_id="TX")),
        other=Sum(F('pmt'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    vrh_ts = VehicleRevenueHours.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('vrh'), filter=Q(service_id="DO")),
        pt=Sum(F('vrh'), filter=Q(service_id="PT")),
        tx=Sum(F('vrh'), filter=Q(service_id="TX")),
        other=Sum(F('vrh'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')

    for x in vrh_ts:

        pmt = pmt_ts.get(year=x['year'])

        if x['do'] and x["do"] > 0 and pmt['do'] and pmt['do'] > 0:
            do_vrh = x['do']
            do_pmt = pmt['do']
            do_pmph = round(do_pmt / do_vrh, 2)
        else:
            do_pmph = 0
        if x['pt'] and x["pt"] > 0 and pmt['pt'] and pmt['pt'] > 0:
            pt_vrh = x['pt']
            pt_pmt = pmt['pt']
            pt_pmph = round(pt_pmt / pt_vrh, 2)
        else:
            pt_pmph = 0
        if x['tx'] and x["tx"] > 0 and pmt['tx'] and pmt['tx'] > 0:
            tx_vrh = x['tx']
            tx_pmt = pmt['tx']
            tx_pmph = round(tx_pmt / tx_vrh, 2)
        else:
            tx_pmph = 0
        if x['other'] and x["other"] > 0 and pmt['other'] and pmt['other'] > 0:
            other_vrh = x['other']
            other_pmt = pmt['other']
            other_pmph = round(other_pmt / other_vrh, 2)
        else:
            other_pmph = 0
        
        data += [{"year": x['year'], "do": do_pmph, "pt": pt_pmph, "tx": tx_pmph, "other": other_pmph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def pmt_per_vrm_by_service(request):
    data = []
    filters, q = process_params(request.GET)
    pmt_ts = PassengerMilesTraveled.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('pmt'), filter=Q(service_id="DO")),
        pt=Sum(F('pmt'), filter=Q(service_id="PT")),
        tx=Sum(F('pmt'), filter=Q(service_id="TX")),
        other=Sum(F('pmt'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    vrm_ts = VehicleRevenueMiles.objects.filter(q)\
    .values("year").annotate(
        do=Sum(F('vrm'), filter=Q(service_id="DO")),
        pt=Sum(F('vrm'), filter=Q(service_id="PT")),
        tx=Sum(F('vrm'), filter=Q(service_id="TX")),
        other=Sum(F('vrm'), filter=Q(service_id__in=['TN', "nan"]))
    )\
    .order_by('year')
    for x in vrm_ts:
        pmt = pmt_ts.get(year=x['year'])
        if x['do'] and x["do"] > 0 and pmt['do'] and pmt['do'] > 0:
            do_vrm = x['do']
            do_pmt = pmt['do']
            do_pmpm = round(do_pmt / do_vrm, 2)
        else:
            do_pmpm = 0
        if x['pt'] and x["pt"] > 0 and pmt['pt'] and pmt['pt'] > 0:
            pt_vrm = x['pt']
            pt_pmt = pmt['pt']
            pt_pmpm = round(pt_pmt / pt_vrm, 2)
        else:
            pt_pmpm = 0
        if x['tx'] and x["tx"] > 0 and pmt['tx'] and pmt['tx'] > 0:
            tx_vrm = x['tx']
            tx_pmt = pmt['tx']
            tx_pmpm = round(tx_pmt / tx_vrm, 2)
        else:
            tx_pmpm = 0
        if x['other'] and x["other"] > 0 and pmt['other'] and pmt['other'] > 0:
            other_vrm = x['other']
            other_pmt = pmt['other']
            other_pmpm = round(other_pmt / other_vrm, 2)
        else:
            other_pmpm = 0
        
        data += [{"year": x['year'], "do": do_pmpm, "pt": pt_pmpm, "tx": tx_pmpm, "other": other_pmpm}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def get_uzas(request):
    # print(request.GET['q'])
    if "q" in request.GET and request.GET['q']:
        uzas = TransitAgency.objects.filter(uza_name__icontains=request.GET['q']).values('uza_name', 'uza').distinct().order_by('uza_name')
        return JsonResponse(list(uzas), safe=False)
    else:
        uzas = TransitAgency.objects.values('uza_name', 'uza').distinct().order_by('uza_name')
        return JsonResponse(list(uzas), safe=False)

@csrf_exempt
def get_states(request):
    # print(request.GET['q'])
    if "q" in request.GET and request.GET['q']:
        states = TransitAgency.objects.filter(state__icontains=request.GET['q']).values('state').distinct().order_by('state')
        return JsonResponse(list(states), safe=False)
    else:
        states = TransitAgency.objects.values('state').distinct().order_by('state')
        return JsonResponse(list(states), safe=False)

@csrf_exempt
def get_agencies(request):
    # print(request.GET['q'])
    if "q" in request.GET and request.GET['q']:
        agencies = TransitAgency.objects.filter(agency_name__icontains=request.GET['q']).values('agency_name', 'id').distinct().order_by('agency_name')
        return JsonResponse(list(agencies), safe=False)
    else:
        agencies = TransitAgency.objects.values('agency_name', 'id').distinct().order_by('agency_name')
        return JsonResponse(list(agencies), safe=False)

@csrf_exempt
def austin_safety_crisis(request):
    # q = (Q(pedestrian_death_count__gte=1) | Q(pedestrian_serious_injury_count__gte=1) | Q(bicycle_death_count__gte=1) | Q(bicycle_serious_injury_count__gte=1) | Q(other_death_count__gte=1) | Q(other_serious_injury_count__gte=1))
    # atd_failures = Crash.objects.filter(q)
    crash_counts = Crash.objects.raw("""
    select 1 as crash_id,
        YEAR(crash_date) as year,
        MONTH(crash_date) as month,
        sum(bicycle_death_count) as bicycle_death_count,
        sum(bicycle_serious_injury_count) as bicycle_serious_injury_count,
        sum(pedestrian_death_count) as pedestrian_death_count,
        sum(pedestrian_serious_injury_count) as pedestrian_serious_injury_count,
        sum(other_death_count) as other_death_count,
        sum(other_serious_injury_count) as other_serious_injury_count
    from transportation.crash 
    group by 
    YEAR(crash_date),
    MONTH(crash_date)
    order by 
    YEAR(crash_date),
    MONTH(crash_date);
    """)
    return render(request, "austin_safety_crisis.html", context={"crashes": crash_counts})

class HomePage(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, "home.html", context={"debug": DEBUG})
    

class BlogPage(View):
    
    def get(self, request, *args, **kwargs):

        return render(request, "blog.html", context={"debug": DEBUG})
    
class CapMetroPage(View):
    
    def get(self, request, *args, **kwargs):
        local_routes = RoutePerformance.objects.filter(route_id__route_id__gte=1, route_id__route_id__lte=99).values("route_id__route_long_name", "route_id__route_id").distinct
        flyer_routes = RoutePerformance.objects.filter(route_id__route_id__gte=100, route_id__route_id__lte=199).exclude(route_id__route_id__in=[101,102]).values("route_id__route_long_name", "route_id__route_id").distinct
        feeder_routes = RoutePerformance.objects.filter(route_id__route_id__gte=200, route_id__route_id__lte=299).values("route_id__route_long_name", "route_id__route_id").distinct
        paratransit =  RoutePerformance.objects.filter(route_id__route_id__in=[101,102]).values("route_id__route_long_name", "route_id__route_id").distinct
        night_routes = RoutePerformance.objects.filter(route_id__route_id__gte=480, route_id__route_id__lte=489).values("route_id__route_long_name", "route_id__route_id").distinct
        crosstown_routes = RoutePerformance.objects.filter(route_id__route_id__gte=300, route_id__route_id__lte=399).values("route_id__route_long_name", "route_id__route_id").distinct()
        shuttle_routes = RoutePerformance.objects.filter(route_id__route_id__gte=400, route_id__route_id__lte=499).exclude(route_id__route_id__in=[480,481,482,483,484,485,486,487,488,489]).values("route_id__route_long_name", "route_id__route_id").distinct
        ut_routes = RoutePerformance.objects.filter(route_id__route_id__gte=600, route_id__route_id__lte=699).values("route_id__route_long_name", "route_id__route_id").distinct
        rapid_routes = RoutePerformance.objects.filter(route_id__route_id__gte=800, route_id__route_id__lte=899).values("route_id__route_long_name", "route_id__route_id").distinct
        express_routes = RoutePerformance.objects.filter(route_id__route_id__gte=900, route_id__route_id__lte=999).values("route_id__route_long_name", "route_id__route_id").distinct
        rail_routes = RoutePerformance.objects.filter(route_id__route_id__gte=500, route_id__route_id__lte=599).values("route_id__route_long_name", "route_id__route_id").distinct

        context = {
            "local_routes": local_routes,
            "flyer_routes": flyer_routes,
            "feeder_routes": feeder_routes,
            "paratransit": paratransit,
            "crosstown_routes": crosstown_routes,
            "night_routes": night_routes,
            "shuttle_routes": shuttle_routes,
            "ut_routes": ut_routes,
            "rapid_routes": rapid_routes,
            "express_routes": express_routes,
            "rail_routes": rail_routes,
            "debug": DEBUG
        }
        return render(request, "capmetro.html", context=context)

        
class CityMapperPage(View):
    
    def get(self, request, *args, **kwargs):

        return render(request, "citymapper.html", context={"debug": DEBUG})
    
class BikeCrashMap(View):
    
    def get(self, request, *args, **kwargs):

        m = folium.Map(location=[30.297370913553245, -97.7313631855747], zoom_start=12)
        # crashes = Crash.objects.filter(Q(pedestrian_death_count__gt = 0) | Q(bicycle_death_count__gt = 0))
        crashes = Crash.objects.filter(Q(bicycle_serious_injury_count__gt = 0) | Q(bicycle_death_count__gt = 0))
        # Crash.bicycle_serious_injury_count
        print(len(crashes))
        
        
        for crash in crashes:
            # print(crash)
            # print(crash.atd_mode_category_metadata)
            description = f"{'https://data.austintexas.gov/resource/y2wy-tgr5.json?crash_id=' + str(crash.crash_id)}"

            link = f"<a target='_blank' href='{description}'>Link to More Info</a>"
            tooltip = f"""
            <div>{crash.crash_date.strftime("%Y-%m-%d")}</div></br>
            {crash.bicycle_death_count} deaths </br>
            {crash.bicycle_serious_injury_count} serious injuries</br>
            {crash.units_involved}
            """
            crash_summary = f"""
            <h4>{crash.crash_date.strftime("%Y-%m-%d")}</h4></br>

            <div>Bike Deaths: {crash.bicycle_death_count}</div></br>

            <div>Serious Injuries: {crash.bicycle_serious_injury_count}</div></br>
            
            <div>{crash.units_involved}</div></br>

            {link}
            """
            # crash_summary = {
            #     "date": crash.crash_date.strftime("%Y-%m-%d"),
            #     "bike_deaths": crash.bicycle_death_count,
            #     "bicycle_serious_injuries": crash.bicycle_serious_injury_count,
            #     "more_info": link
            # }
            if crash.latitude and crash.longitude and crash.latitude != 0  and crash.longitude != 0:
                if crash.bicycle_death_count > 0:
                    folium.Marker(
                        [crash.latitude, crash.longitude], popup=folium.Popup(max_width=450, html=crash_summary, parse_html=False), icon=folium.Icon(color="red")
                    ).add_to(m)
                else:
                    folium.Marker(
                        [crash.latitude, crash.longitude], popup=folium.Popup(max_width=450, html=crash_summary, parse_html=False), icon=folium.Icon(color="green")
                    ).add_to(m)
        # folium.GeoJson(geojson, name="geojson", tooltip="hi").add_to(m)
        m = m._repr_html_()
        context = {"map": m}
        return render(request, "bike_crash_map.html", context=context)
    
    
class PedestrianCrashMap(View):
    
    def get(self, request, *args, **kwargs):

        m = folium.Map(location=[30.297370913553245, -97.7313631855747], zoom_start=12)
        # crashes = Crash.objects.filter(Q(pedestrian_death_count__gt = 0) | Q(bicycle_death_count__gt = 0))
        crashes = Crash.objects.filter(Q(pedestrian_serious_injury_count__gt = 0) | Q(pedestrian_death_count__gt = 0))
        # Crash.bicycle_serious_injury_count
        print(len(crashes))
        
        
        for crash in crashes:
            # print(crash)
            # print(crash.atd_mode_category_metadata)
            description = f"{'https://data.austintexas.gov/resource/y2wy-tgr5.json?crash_id=' + str(crash.crash_id)}"

            link = f"<a target='_blank' href='{description}'>Link to More Info</a>"
            tooltip = f"""
            <div>{crash.crash_date.strftime("%Y-%m-%d")}</div></br>
            {crash.pedestrian_death_count} deaths </br>
            {crash.pedestrian_serious_injury_count} serious injuries</div></br>
            <div>{crash.units_involved} 
            """
            crash_summary = f"""
            <h4>{crash.crash_date.strftime("%Y-%m-%d")}</h4></br>

            <div>Pedestrian Deaths: {crash.pedestrian_death_count}</div></br>

            <div>Serious Injuries: {crash.pedestrian_serious_injury_count}</div></br>

            <div>{crash.units_involved}</div></br>

            {link}
            """
            # crash_summary = {
            #     "date": crash.crash_date.strftime("%Y-%m-%d"),
            #     "bike_deaths": crash.bicycle_death_count,
            #     "bicycle_serious_injuries": crash.bicycle_serious_injury_count,
            #     "more_info": link
            # }
            if crash.latitude and crash.longitude and crash.latitude != 0  and crash.longitude != 0:
                if crash.pedestrian_death_count > 0:
                    folium.Marker(
                        [crash.latitude, crash.longitude], popup=folium.Popup(max_width=450, html=crash_summary, parse_html=False), icon=folium.Icon(color="red")
                    ).add_to(m)
                else:
                    folium.Marker(
                        [crash.latitude, crash.longitude], popup=folium.Popup(max_width=450, html=crash_summary, parse_html=False), icon=folium.Icon(color="green")
                    ).add_to(m)
        # folium.GeoJson(geojson, name="geojson", tooltip="hi").add_to(m)
        m = m._repr_html_()
        context = {"map": m}
        return render(request, "bike_crash_map.html", context=context)
    
    

@csrf_exempt
def monthly_upt(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(date=F("date"), upt=Round(Sum("upt"))).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def monthly_upt_by_mode(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(
        date=F("date"), 
        mb=Round(Sum(F('upt'), filter=Q(mode_id="MB"))), \
        cb=Round(Sum(F('upt'), filter=Q(mode_id="CB"))), \
        rb=Round(Sum(F('upt'), filter=Q(mode_id="RB"))), \
        tb=Round(Sum(F('upt'), filter=Q(mode_id="TB"))), \
        pb=Round(Sum(F('upt'), filter=Q(mode_id="PB"))), \
        hr=Round(Sum(F('upt'), filter=Q(mode_id="HR"))), \
        lr=Round(Sum(F('upt'), filter=Q(mode_id="LR"))), \
        cr=Round(Sum(F('upt'), filter=Q(mode_id="CR"))), \
        yr=Round(Sum(F('upt'), filter=Q(mode_id="YR"))), \
        sr=Round(Sum(F('upt'), filter=Q(mode_id="SR"))), \
        cc=Round(Sum(F('upt'), filter=Q(mode_id="CC"))), \
        mg=Round(Sum(F('upt'), filter=Q(mode_id__in=["MG", "MO"]))), \
        ip=Round(Sum(F('upt'), filter=Q(mode_id="IP"))), \
        ar=Round(Sum(F('upt'), filter=Q(mode_id="AR"))), \
        at=Round(Sum(F('upt'), filter=Q(mode_id="AT"))), \
        other_rail=Round(Sum(F('upt'), filter=Q(mode_id="OR"))), \
        dr=Round(Sum(F('upt'), filter=Q(mode_id="DR"))), \
        dt=Round(Sum(F('upt'), filter=Q(mode_id="DT"))), \
        vp=Round(Sum(F('upt'), filter=Q(mode_id="VP"))), \
        jt=Round(Sum(F('upt'), filter=Q(mode_id="JT"))), \
        fb=Round(Sum(F('upt'), filter=Q(mode_id="FB"))), \
        tr=Round(Sum(F('upt'), filter=Q(mode_id="TR"))), \
        ot=Round(Sum(F('upt'), filter=Q(mode_id__in=["OT", "nan"])))
    ).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def monthly_upt_by_mode_type(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(
        date=F("date"),
        bus=Round(Sum('upt', filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('upt'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('upt'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('upt'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('upt'), filter=Q(mode_id__type="Other")))
    )\
    .order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def monthly_upt_by_service(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(
        date=F("date"), 
        directly_operated=Round(Sum(F('upt'), filter=Q(service_id="DO"))), \
        purchased_transportation=Round(Sum(F('upt'), filter=Q(service_id="PT"))), \
        taxi=Round(Sum(F('upt'), filter=Q(service_id="TX"))), \
        other=Round(Sum(F('upt'), filter=Q(service_id="OT")))\
    ).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)


@csrf_exempt
def monthly_voms(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehiclesOperatedMaximumService.objects.filter(q).values("year", "month").annotate(date=F("date"), voms=Round(Sum("voms"))).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)


@csrf_exempt
def monthly_vrm(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehicleRevenueMiles.objects.filter(q).values("year", "month").annotate(date=F("date"), vrm=Round(Sum("vrm"))).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)



@csrf_exempt
def monthly_vrm_by_mode(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehicleRevenueMiles.objects.filter(q).values("year", "month").annotate(
        date=F("date"), 
        mb=Round(Sum(F('vrm'), filter=Q(mode_id="MB"))), \
        cb=Round(Sum(F('vrm'), filter=Q(mode_id="CB"))), \
        rb=Round(Sum(F('vrm'), filter=Q(mode_id="RB"))), \
        tb=Round(Sum(F('vrm'), filter=Q(mode_id="TB"))), \
        pb=Round(Sum(F('vrm'), filter=Q(mode_id="PB"))), \
        hr=Round(Sum(F('vrm'), filter=Q(mode_id="HR"))), \
        lr=Round(Sum(F('vrm'), filter=Q(mode_id="LR"))), \
        cr=Round(Sum(F('vrm'), filter=Q(mode_id="CR"))), \
        yr=Round(Sum(F('vrm'), filter=Q(mode_id="YR"))), \
        sr=Round(Sum(F('vrm'), filter=Q(mode_id="SR"))), \
        cc=Round(Sum(F('vrm'), filter=Q(mode_id="CC"))), \
        mg=Round(Sum(F('vrm'), filter=Q(mode_id__in=["MG", "MO"]))), \
        ip=Round(Sum(F('vrm'), filter=Q(mode_id="IP"))), \
        ar=Round(Sum(F('vrm'), filter=Q(mode_id="AR"))), \
        at=Round(Sum(F('vrm'), filter=Q(mode_id="AT"))), \
        other_rail=Round(Sum(F('vrm'), filter=Q(mode_id="OR"))), \
        dr=Round(Sum(F('vrm'), filter=Q(mode_id="DR"))), \
        dt=Round(Sum(F('vrm'), filter=Q(mode_id="DT"))), \
        vp=Round(Sum(F('vrm'), filter=Q(mode_id="VP"))), \
        jt=Round(Sum(F('vrm'), filter=Q(mode_id="JT"))), \
        fb=Round(Sum(F('vrm'), filter=Q(mode_id="FB"))), \
        tr=Round(Sum(F('vrm'), filter=Q(mode_id="TR"))), \
        ot=Round(Sum(F('vrm'), filter=Q(mode_id__in=["OT", "nan"])))
    ).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def monthly_vrm_by_mode_type(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehicleRevenueMiles.objects.filter(q).values("year", "month").annotate(
        date=F("date"),
        bus=Round(Sum(F('vrm'), filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('vrm'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('vrm'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('vrm'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('vrm'), filter=Q(mode_id__type="Other")))
    )\
    .order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def monthly_vrm_by_service(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehicleRevenueMiles.objects.filter(q).values("year", "month").annotate(
        date=F("date"), 
        directly_operated=Round(Sum(F('vrm'), filter=Q(service_id="DO"))), \
        purchased_transportation=Round(Sum(F('vrm'), filter=Q(service_id="PT"))), \
        taxi=Round(Sum(F('vrm'), filter=Q(service_id="TX"))), \
        other=Round(Sum(F('vrm'), filter=Q(service_id="OT")))\
    ).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)


@csrf_exempt
def monthly_vrh(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehicleRevenueHours.objects.filter(q).values("year", "month").annotate(date=F("date"), vrh=Round(Sum("vrh"))).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)



@csrf_exempt
def monthly_vrh_by_mode(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehicleRevenueHours.objects.filter(q).values("year", "month").annotate(
        date=F("date"), 
        mb=Round(Sum(F('vrh'), filter=Q(mode_id="MB"))), \
        cb=Round(Sum(F('vrh'), filter=Q(mode_id="CB"))), \
        rb=Round(Sum(F('vrh'), filter=Q(mode_id="RB"))), \
        tb=Round(Sum(F('vrh'), filter=Q(mode_id="TB"))), \
        pb=Round(Sum(F('vrh'), filter=Q(mode_id="PB"))), \
        hr=Round(Sum(F('vrh'), filter=Q(mode_id="HR"))), \
        lr=Round(Sum(F('vrh'), filter=Q(mode_id="LR"))), \
        cr=Round(Sum(F('vrh'), filter=Q(mode_id="CR"))), \
        yr=Round(Sum(F('vrh'), filter=Q(mode_id="YR"))), \
        sr=Round(Sum(F('vrh'), filter=Q(mode_id="SR"))), \
        cc=Round(Sum(F('vrh'), filter=Q(mode_id="CC"))), \
        mg=Round(Sum(F('vrh'), filter=Q(mode_id__in=["MG", "MO"]))), \
        ip=Round(Sum(F('vrh'), filter=Q(mode_id="IP"))), \
        ar=Round(Sum(F('vrh'), filter=Q(mode_id="AR"))), \
        at=Round(Sum(F('vrh'), filter=Q(mode_id="AT"))), \
        other_rail=Round(Sum(F('vrh'), filter=Q(mode_id="OR"))), \
        dr=Round(Sum(F('vrh'), filter=Q(mode_id="DR"))), \
        dt=Round(Sum(F('vrh'), filter=Q(mode_id="DT"))), \
        vp=Round(Sum(F('vrh'), filter=Q(mode_id="VP"))), \
        jt=Round(Sum(F('vrh'), filter=Q(mode_id="JT"))), \
        fb=Round(Sum(F('vrh'), filter=Q(mode_id="FB"))), \
        tr=Round(Sum(F('vrh'), filter=Q(mode_id="TR"))), \
        ot=Round(Sum(F('vrh'), filter=Q(mode_id__in=["OT", "nan"])))
    ).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def monthly_vrh_by_mode_type(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehicleRevenueHours.objects.filter(q).values("year", "month").annotate(
        date=F("date"),
        bus=Round(Sum(F('vrh'), filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('vrh'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('vrh'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('vrh'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('vrh'), filter=Q(mode_id__type="Other")))
    )\
    .order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def monthly_vrh_by_service(request):
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    q &= Q(date__gte=start_date)
    ts = MonthlyVehicleRevenueHours.objects.filter(q).values("year", "month").annotate(
        date=F("date"), 
        directly_operated=Round(Sum(F('vrh'), filter=Q(service_id="DO"))), \
        purchased_transportation=Round(Sum(F('vrh'), filter=Q(service_id="PT"))), \
        taxi=Round(Sum(F('vrh'), filter=Q(service_id="TX"))), \
        other=Round(Sum(F('vrh'), filter=Q(service_id="OT")))\
    ).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

@csrf_exempt
def monthly_upt_per_vrh(request):
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    q &= Q(date__gte=start_date)
    upt_ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(date=F("date"), upt=Round(Sum("upt"))).order_by('year', "month")
    vrh_ts = MonthlyVehicleRevenueHours.objects.filter(q).values("year", "month").annotate(date=F("date"), vrh=Round(Sum("vrh"))).order_by('year', "month")
    data = []
    x = 0
    for upt_month in upt_ts:
        upt = upt_month['upt']
        vrh = vrh_ts[x]['vrh']
        if upt and vrh and upt > 0 and vrh > 0:
            data += [{
                "year": upt_month['year'],
                "month": months[upt_month['month']],
                "date": upt_month['date'],
                "upt_per_vrh": upt / vrh
            }]
        x += 1

    resp = {
        "filters": filters,
        "length": len(data),
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@csrf_exempt
def monthly_upt_per_vrm(request):
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    filters, q = process_params(request.GET)
    if "start" in  request.GET and request.GET['start']:
        date_array = request.GET['start'].split("-")
        start_date = datetime.datetime(year=int(date_array[0]),month=int(date_array[1]),day=int(date_array[2]))
    else:
        start_date = datetime.datetime(year=1980,month=1,day=1)
    q &= Q(date__gte=start_date)
    upt_ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(date=F("date"), upt=Round(Sum("upt"))).order_by('year', "month")
    vrm_ts = MonthlyVehicleRevenueMiles.objects.filter(q).values("year", "month").annotate(date=F("date"), vrm=Round(Sum("vrm"))).order_by('year', "month")
    data = []
    x = 0
    for upt_month in upt_ts:
        upt = upt_month['upt']
        vrm = vrm_ts[x]['vrm']
        if upt and vrm and upt > 0 and vrm > 0:
            data += [{
                "year": upt_month['year'],
                "month": months[upt_month['month']],
                "date": upt_month['date'],
                "upt_per_vrm": upt / vrm
            }]
        x += 1

    resp = {
        "filters": filters,
        "length": len(data),
        "data": data
    }
    return JsonResponse(resp, safe=False)
    # months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

@csrf_exempt
def monthly_upt_per_vrh_by_mode_type(request):
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    filters, q = process_params(request.GET)
    start_date = datetime.datetime(year=2020,month=1,day=1)
    q &= Q(date__gte=start_date)

    upt_ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(
        date=F("date"), bus=Round(Sum(F('upt'), filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('upt'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('upt'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('upt'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('upt'), filter=Q(mode_id__type="Other")))
    ).order_by('year', "month")

    vrh_ts = MonthlyVehicleRevenueHours.objects.filter(q).values("year", "month").annotate(
        date=F("date"), bus=Round(Sum(F('vrh'), filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('vrh'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('vrh'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('vrh'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('vrh'), filter=Q(mode_id__type="Other")))
    ).order_by('year', "month")

    data = []
    x = 0

    for upt_month in upt_ts:
        if upt_month['bus'] and vrh_ts[x]['bus'] and upt_month['bus'] > 0 and vrh_ts[x]['bus'] > 0:
            bus = upt_month['bus'] / vrh_ts[x]['bus']
        else:
            bus = 0
        if upt_month['rail'] and vrh_ts[x]['rail'] and upt_month['rail'] > 0 and vrh_ts[x]['rail'] > 0:
            rail = upt_month['rail'] / vrh_ts[x]['rail']
        else:
            rail = 0
        if upt_month['microtransit'] and vrh_ts[x]['microtransit'] and upt_month['microtransit'] > 0 and vrh_ts[x]['microtransit'] > 0:
            microtransit = upt_month['microtransit'] / vrh_ts[x]['microtransit']
        else:
            microtransit = 0
        if upt_month['ferry'] and vrh_ts[x]['ferry'] and upt_month['ferry'] > 0 and vrh_ts[x]['ferry'] > 0:
            ferry = upt_month['ferry'] / vrh_ts[x]['ferry']
        else:
            ferry = 0
        if upt_month['other'] and vrh_ts[x]['other'] and upt_month['other'] > 0 and vrh_ts[x]['other'] > 0:
            other = upt_month['other'] / vrh_ts[x]['other']
        else:
            other = 0
    
        data += [{
            "year": upt_month['year'],
            "month": months[upt_month['month']],
            "date": upt_month['date'],
            "bus": bus,
            "rail": rail, 
            "microtransit": microtransit,
            "ferry": ferry,
            "other": other
        }]
        x += 1

    resp = {
        "filters": filters,
        "length": len(data),
        "data": data
    }
    return JsonResponse(resp, safe=False)


@csrf_exempt
def upt_month_over_month_baseline(request):
    filters, q = process_params(request.GET)
    baseline_ridership_start_date = datetime.datetime(year=2019,month=1,day=1)
    baseline_ridership_end_date = datetime.datetime(year=2020,month=1,day=1)
    ridership_data_start_date = datetime.datetime(year=2020,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    baseline_q = q & Q(date__gte=baseline_ridership_start_date, date__lt=baseline_ridership_end_date)

    baseline_ridership = MonthlyUnlinkedPassengerTrips.objects.filter(baseline_q).values("year", "month").annotate(date=F("date"), upt=Round(Sum("upt"))).order_by('year', "month")
    baseline_list = []
    for x in baseline_ridership:
        baseline_list += [x]

    q &= Q(date__gte=ridership_data_start_date)
    ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(date=F("date"), upt=Round(Sum("upt"))).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    mom_data = []
    for x in range(length):
        month_id = x % 12
        print(month_id)
        if data[x]['upt'] > 0 and baseline_list[month_id]["upt"] > 0:
            print(data[x])
            print(f"ridership: {data[x]['upt']}")
            print(f"baseline ridership: {baseline_list[month_id]['upt']}")
            ratio = data[x]['upt'] / baseline_list[month_id]['upt']
            print(ratio)
            new_month = { 
                'year': data[x]['year'],
                'month': data[x]['month'],
                'date': data[x]['date'],
                'change_from_baseline': ratio,
                "baseline": 1
            }
            mom_data += [new_month]

    resp = {
        "filters": filters,
        "length": length,
        "data": mom_data
    }
    return JsonResponse(resp, safe=False)
    
@csrf_exempt
def upt_month_over_month_baseline_by_mode_type(request):
    filters, q = process_params(request.GET)
    baseline_ridership_start_date = datetime.datetime(year=2019,month=1,day=1)
    baseline_ridership_end_date = datetime.datetime(year=2020,month=1,day=1)
    ridership_data_start_date = datetime.datetime(year=2020,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    baseline_q = q & Q(date__gte=baseline_ridership_start_date, date__lt=baseline_ridership_end_date)

    baseline_ridership = MonthlyUnlinkedPassengerTrips.objects.filter(baseline_q)\
    .values("year", "month").annotate(date=F("date"), bus=Round(Sum(F('upt'), filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('upt'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('upt'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('upt'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('upt'), filter=Q(mode_id__type="Other")))).order_by("year", "month")
    baseline_list = []
    for x in baseline_ridership:
        baseline_list += [x]

    q &= Q(date__gte=ridership_data_start_date)
    ts = MonthlyUnlinkedPassengerTrips.objects.filter(q)\
    .values("year", "month").annotate(date=F("date"), bus=Round(Sum(F('upt'), filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('upt'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('upt'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('upt'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('upt'), filter=Q(mode_id__type="Other")))).order_by("year", "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    mom_data = []

    for x in range(length):
        month_id = x % 12
        print(month_id)

        if data[x]['bus'] and baseline_list[month_id]["bus"] and data[x]['bus'] > 0 and baseline_list[month_id]["bus"] > 0:
            bus = data[x]['bus'] / baseline_list[month_id]['bus']
        else:
            bus = 0
        if data[x]['rail'] and baseline_list[month_id]["rail"] and data[x]['rail'] > 0 and baseline_list[month_id]["rail"] > 0:
            rail = data[x]['rail'] / baseline_list[month_id]['rail']
        else:
            rail = 0
        if data[x]['microtransit'] and baseline_list[month_id]["microtransit"] and data[x]['microtransit'] > 0 and baseline_list[month_id]["microtransit"] > 0:
            microtransit = data[x]['microtransit'] / baseline_list[month_id]['microtransit']
        else:
            microtransit = 0
        if data[x]['ferry'] and baseline_list[month_id]["ferry"] and data[x]['ferry'] > 0 and baseline_list[month_id]["ferry"] > 0:
            ferry = data[x]['ferry'] / baseline_list[month_id]['ferry']
        else:
            ferry = 0
        if data[x]['other'] and baseline_list[month_id]["other"] and data[x]['other'] > 0 and baseline_list[month_id]["other"] > 0:
            other = data[x]['other'] / baseline_list[month_id]['other']
        else:
            other = 0

        new_month = { 
            'year': data[x]['year'],
            'month': data[x]['month'],
            'date': data[x]['date'],
            'bus': bus,
            'rail': rail,
            'microtransit': microtransit,
            'ferry': ferry,
            'other': other,
            "baseline": 1
        }
        mom_data += [new_month]

    resp = {
        "filters": filters,
        "length": length,
        "data": mom_data
    }
    return JsonResponse(resp, safe=False)

# @csrf_exempt
# def upt_month_over_month_baseline_by_mode_type(request):
#     filters, q = process_params(request.GET)
#     ts = MonthlyUnlinkedPassengerTrips.objects.filter(q)\
#         .values("year", "").annotate(bus=Round(Sum(F('upt'), filter=Q(mode_id__type="Bus"))), \
#                                  rail=Round(Sum(F('upt'), filter=Q(mode_id__type="Rail"))), \
#                                  microtransit=Round(Sum(F('upt'), filter=Q(mode_id__type="MicroTransit"))), \
#                                  ferry=Round(Sum(F('upt'), filter=Q(mode_id__type="Ferry"))), \
#                                  other=Round(Sum(F('upt'), filter=Q(mode_id__type="Other")))).\
#         order_by('year')
#     data = []
#     for x in ts:
#         data += [x]
#     length = len(data)
#     resp = {
#         "filters": filters,
#         "length": length,
#         "data": data
#     }
#     return JsonResponse(resp, safe=False)

# eh I'm not sure if this is wrong I feel like I'm supposed to divide the baseline ridership values by five, but it's not working rn
@csrf_exempt
def upt_month_over_month_baseline_average(request):
    filters, q = process_params(request.GET)
    baseline_ridership_start_date = datetime.datetime(year=2015,month=1,day=1)
    baseline_ridership_end_date = datetime.datetime(year=2020,month=1,day=1)
    ridership_data_start_date = datetime.datetime(year=2020,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    baseline_q = q & Q(date__gte=baseline_ridership_start_date, date__lt=baseline_ridership_end_date)

    baseline_ridership = MonthlyUnlinkedPassengerTrips.objects.filter(baseline_q).values("month").annotate(date=F("date"), upt=(Round(Sum("upt")))).order_by("month")
    baseline_list = []
    for x in baseline_ridership:
        baseline_list += [x]

    q &= Q(date__gte=ridership_data_start_date)
    ts = MonthlyUnlinkedPassengerTrips.objects.filter(q).values("year", "month").annotate(date=F("date"), upt=Round(Sum("upt"))).order_by('year', "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    mom_data = []
    for x in range(length):
        month_id = x % 12
        print(month_id)
        if data[x]['upt'] > 0 and baseline_list[month_id]["upt"] > 0:
            print(data[x])
            print(f"ridership: {data[x]['upt']}")
            print(f"baseline ridership: {baseline_list[month_id]['upt']}")
            ratio = data[x]['upt'] / baseline_list[month_id]['upt']
            print(ratio)
            new_month = { 
                'year': data[x]['year'],
                'month': data[x]['month'],
                'date': data[x]['date'],
                'change_from_baseline': ratio
            }
            mom_data += [new_month]
    resp = {
        "filters": filters,
        "length": length,
        "data": mom_data
    }
    return JsonResponse(resp, safe=False)


@csrf_exempt
def upt_month_over_month_baseline_average_by_mode_type(request):
    filters, q = process_params(request.GET)
    baseline_ridership_start_date = datetime.datetime(year=2016,month=1,day=1)
    baseline_ridership_end_date = datetime.datetime(year=2020,month=1,day=1)
    ridership_data_start_date = datetime.datetime(year=2020,month=1,day=1)
    months = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    baseline_q = q & Q(date__gte=baseline_ridership_start_date, date__lt=baseline_ridership_end_date)

    baseline_ridership = MonthlyUnlinkedPassengerTrips.objects.filter(baseline_q)\
    .values("month").annotate(date=F("date"), bus=Round(Sum(F('upt'), filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('upt'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('upt'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('upt'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('upt'), filter=Q(mode_id__type="Other")))).order_by("month")
    baseline_list = []
    for x in baseline_ridership:
        baseline_list += [x]

    q &= Q(date__gte=ridership_data_start_date)
    ts = MonthlyUnlinkedPassengerTrips.objects.filter(q)\
    .values("year", "month").annotate(date=F("date"), bus=Round(Sum(F('upt'), filter=Q(mode_id__type="Bus"))), \
        rail=Round(Sum(F('upt'), filter=Q(mode_id__type="Rail"))), \
        microtransit=Round(Sum(F('upt'), filter=Q(mode_id__type="MicroTransit"))), \
        ferry=Round(Sum(F('upt'), filter=Q(mode_id__type="Ferry"))), \
        other=Round(Sum(F('upt'), filter=Q(mode_id__type="Other")))).order_by("year", "month")
    data = []
    for x in ts:
        x['month'] = months[x['month']]
        data += [x]
    length = len(data)
    mom_data = []

    for x in range(length):
        month_id = x % 12
        print(month_id)

        if data[x]['bus'] and baseline_list[month_id]["bus"] and data[x]['bus'] > 0 and baseline_list[month_id]["bus"] > 0:
            bus = data[x]['bus'] / baseline_list[month_id]['bus']
        else:
            bus = 0
        if data[x]['rail'] and baseline_list[month_id]["rail"] and data[x]['rail'] > 0 and baseline_list[month_id]["rail"] > 0:
            rail = data[x]['rail'] / baseline_list[month_id]['rail']
        else:
            rail = 0
        if data[x]['microtransit'] and baseline_list[month_id]["microtransit"] and data[x]['microtransit'] > 0 and baseline_list[month_id]["microtransit"] > 0:
            microtransit = data[x]['microtransit'] / baseline_list[month_id]['microtransit']
        else:
            microtransit = 0
        if data[x]['ferry'] and baseline_list[month_id]["ferry"] and data[x]['ferry'] > 0 and baseline_list[month_id]["ferry"] > 0:
            ferry = data[x]['ferry'] / baseline_list[month_id]['ferry']
        else:
            ferry = 0
        if data[x]['other'] and baseline_list[month_id]["other"] and data[x]['other'] > 0 and baseline_list[month_id]["other"] > 0:
            other = data[x]['other'] / baseline_list[month_id]['other']
        else:
            other = 0

        new_month = { 
            'year': data[x]['year'],
            'month': data[x]['month'],
            'date': data[x]['date'],
            'bus': bus,
            'rail': rail,
            'microtransit': microtransit,
            'ferry': ferry,
            'other': other,
            "baseline": 1
        }
        mom_data += [new_month]

    resp = {
        "filters": filters,
        "length": length,
        "data": mom_data
    }
    return JsonResponse(resp, safe=False)


from django.db import connection

@csrf_exempt
def commuter_rail_upt(request):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT 
            transit_agency.agency_name,
            transit_agency.id AS transit_agency_id,
            riders.total_riders,
            spending.operating_expenses,
            (spending.operating_expenses / riders.total_riders) AS cost_per_trip
        FROM 
            transit_agency

        LEFT JOIN (
            
            SELECT 
                transit_agency.agency_name,
                transit_agency.id AS transit_agency_id,
                sum(upt.upt) AS total_riders
            FROM 
                upt
            LEFT JOIN
                transit_agency
            ON
                transit_agency.id = upt.transit_agency_id
            WHERE
                upt.mode_id IN ("CR", "YR")
            AND
                upt.year >= 2010
            GROUP BY
                transit_agency.id, transit_agency.agency_name
            ORDER BY total_riders DESC

        ) AS riders ON riders.transit_agency_id = transit_agency.id

        LEFT JOIN (

            SELECT 
                transit_agency.agency_name,
                transit_agency.id AS transit_agency_id,
                sum(transit_expense.expense * cpi.in_todays_dollars) AS operating_expenses
            FROM 
                transit_expense
            LEFT JOIN cpi ON cpi.year = transit_expense.year_id
            LEFT JOIN
                transit_agency
            ON
                transit_agency.id = transit_expense.transit_agency_id
            WHERE
                transit_expense.mode_id  IN ("CR", "YR")
            AND
                transit_expense.expense_type_id IN ("VO", "VM", "NVM", "GA")
            AND
                transit_expense.year_id >= 2010
            GROUP BY
                transit_agency.id, transit_agency.agency_name
            ORDER BY operating_expenses DESC

        ) 
        AS spending ON spending.transit_agency_id = transit_agency.id
            
        WHERE 
            riders.total_riders IS NOT NULL
        AND 
            riders.total_riders > 0
        AND 
            spending.operating_expenses IS NOT NULL
        AND 
            spending.operating_expenses > 0
        ORDER BY 
            cost_per_trip ASC;
    ''')
    # print(cursor.fetchall())
    data = []
    for x in cursor.fetchall():
        data += [
            {
                "agency": x[0], 
                "riders": x[2],
                "operating_expense": x[3],
                "cost_per_passenger": x[4]
            }
        ]
    resp = {"data": data}
    return JsonResponse(resp)


@csrf_exempt
def commuter_rail_pmt(request):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT
            transit_agency.agency_name,
            transit_agency.id AS transit_agency_id,
            passenger_miles.passenger_miles,
            spending.operating_expenses,
            (spending.operating_expenses / passenger_miles.passenger_miles) AS cost_per_passenger_mile
        FROM 
            transit_agency

        LEFT JOIN (
            
            SELECT 
                transit_agency.agency_name,
                transit_agency.id AS transit_agency_id,
                sum(pmt.pmt) AS passenger_miles
            FROM 
                pmt
            LEFT JOIN
                transit_agency
            ON
                transit_agency.id = pmt.transit_agency_id
            WHERE
                pmt.mode_id IN ("CR", "YR")
            AND
                pmt.year >= 2010
            GROUP BY
                transit_agency.id, transit_agency.agency_name
            ORDER BY passenger_miles DESC

        ) AS passenger_miles ON passenger_miles.transit_agency_id = transit_agency.id

        LEFT JOIN (

            SELECT 
                transit_agency.agency_name,
                transit_agency.id AS transit_agency_id,
                sum(transit_expense.expense * cpi.in_todays_dollars) AS operating_expenses
            FROM 
                transit_expense
            LEFT JOIN cpi ON cpi.year = transit_expense.year_id
            LEFT JOIN
                transit_agency
            ON
                transit_agency.id = transit_expense.transit_agency_id
            WHERE
                transit_expense.mode_id  IN ("CR", "YR")
            AND
                transit_expense.expense_type_id IN ("VO", "VM", "NVM", "GA")
            AND
                transit_expense.year_id >= 2010
            GROUP BY
                transit_agency.id, transit_agency.agency_name
            ORDER BY operating_expenses DESC

        ) 
        AS spending ON spending.transit_agency_id = transit_agency.id
            
        WHERE 
            passenger_miles.passenger_miles IS NOT NULL
        AND 
            passenger_miles.passenger_miles > 0
        AND 
            spending.operating_expenses IS NOT NULL
        AND 
            spending.operating_expenses > 0
        ORDER BY 
            cost_per_passenger_mile ASC;
    ''')
    # print(cursor.fetchall())
    data = []
    for x in cursor.fetchall():
        data += [
            {
                "agency": x[0], 
                "riders": x[2],
                "operating_expense": x[3],
                "cost_per_passenger_mile": x[4]
            }
        ]
    resp = {"data": data}
    return JsonResponse(resp)





@csrf_exempt
def total_red_line_spending(request):
    cursor = connection.cursor()
    cursor.execute('''
        SELECT 
            transit_agency.agency_name,
            transit_agency.id AS transit_agency_id,
            round(sum(transit_expense.expense * cpi.in_todays_dollars)) AS total_red_line_spending
        FROM 
            transit_expense
        LEFT JOIN cpi ON cpi.year = transit_expense.year_id
        LEFT JOIN
            transit_agency
        ON
            transit_agency.id = transit_expense.transit_agency_id
        WHERE

            transit_agency.ntd_id = 60048
        AND
            transit_expense.mode_id  IN ("CR", "YR")
        AND
            transit_expense.year_id >= 2010
        GROUP BY
            transit_agency.id, transit_agency.agency_name;
    ''')
    # print(cursor.fetchall())
    data = []
    for x in cursor.fetchall():
        data += [
            {
                "agency": x[0], 
                "total_red_line_spending": x[2]
            }
        ]
    resp = {"data": data}
    return JsonResponse(resp)

def get_transit_date():
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/Chicago')
    utc = datetime.datetime.today()
    central = utc.astimezone(to_zone)
    todays_transit_date = central.strftime("%Y%m%d")
    if central.strftime("%T")[:2] == "00":
        todays_transit_date = str(int(todays_transit_date) - 1)
    return todays_transit_date

@csrf_exempt
def get_closest_bus_stops(request):
    if "lat" in request.GET and request.GET['lat'] and "lon" in request.GET and request.GET['lon']:
        lat = request.GET['lat']
        lon = request.GET['lon']
    else:
        return JsonResponse({"hi": "hello"})
    todays_transit_date = get_transit_date()
    route_ids = []
    r = requests.get("https://data.texas.gov/download/cuc7-ywmd/text%2Fplain")
    bus_positions = json.loads(r.text)
    now = (datetime.datetime.now() - datetime.timedelta(hours=6, minutes=5)).strftime("%H:%M:%S") 
    # now_timestring = now
    in_two_hours = datetime.datetime.now() - datetime.timedelta(hours=4)
    in_two_hours_timestring = in_two_hours.strftime("%H:%M:%S")
    print(f"NOW {now}")
    print(f"INTWOHOURS {in_two_hours_timestring}")
    stops = Stops.objects.raw("""
        SELECT 
            SQRT(POWER(ABS(longitude - (%s)), 2) + POWER(ABS(latitude - (%s)), 2)) as distance,
            id, stop_id,
            stop_name, corner_placement,
            latitude, longitude
        FROM stops
        order by SQRT(POWER(ABS(longitude - (%s)), 2) + POWER(ABS(latitude - (%s)), 2)) ASC
        LIMIT 10;
    """, [lon, lat, lon, lat])
    stop_ids = []
    # for stop in stops:
    #     stop_ids += [stop.id]
    m = folium.Map(location=[lat, lon], zoom_start=12)
 
    for stop in stops:
        stop_ids += [stop.id]
        # move this into the next for loop, then write the upcoming schedule into the html object before adding the html to the stop marker


    for stop_id in stop_ids:
        cursor = connection.cursor()
        cursor.execute('''
            select time(stop_times.departure_time) as departs,
            trip_headsign,
            stops.stop_id,
            stops.stop_name,
            trips.shape_id,
            trips.trip_id,
            stops.latitude,
            stops.longitude,
            routes.route_id
            from stop_times
            left join trips on trips.id = stop_times.trip_id
            left join routes on trips.route_id = routes.id
            LEFT JOIN stops on stop_times.stop_id = stops.id
            where stop_times.trip_id in
            (select id from trips where service_id in 
            (select service_id from calendar_dates where date = %s))
            and departure_time > "1970-01-01 %s"
            and departure_time < "1970-01-01 %s"
            and stop_times.stop_id = %s
            order by stop_times.departure_time;

        ''', [todays_transit_date, now, in_two_hours_timestring, stop_id])
        shape_ids = []
        html = "<h1>Transit Schedule:</h1>\n"
        stop_lat = None
        stop_lon = None
        # route_ids = []
        folium.Marker(
            [lat, lon], popup=folium.Popup(max_width=450, html="<h1>YOU</h1>", parse_html=False), icon=folium.Icon(color="black")
        ).add_to(m)
        for x in cursor.fetchall():
            # print(x)
            # print(x[8])
            
            # break
            route_id = int(x[8])
            bus_real_time_location = None
            html += f"<h3>{x[0]} - {x[1]}</h3></br>"
            stop_lat = x[6]
            stop_lon = x[7]
            # print(x)
            if int(x[8]) not in route_ids:
                route_ids += [int(x[8])]
            if int(x[4]) not in shape_ids:
                shape_ids += [{"shape": int(x[4]), "route": x[8]}]
        if stop_lat and stop_lon:
            folium.Marker(
                [stop_lat, stop_lon], popup=folium.Popup(max_width=450, html=html, parse_html=False), icon=folium.Icon(color="red")
            ).add_to(m)

        for shape in shape_ids:
            shapes_points = Shapes.objects.filter(shape_id=shape['shape'])
            line = []
            for shape_point in shapes_points:
                # print(f"{shape_point.shape_pt_lat}, {shape_point.shape_pt_lon}")
                line += [(float(shape_point.shape_pt_lat), float(shape_point.shape_pt_lon))]
            # line_string = LineString(line)
            folium.PolyLine(line, tooltip= f"<h1>{shape['route']}</h1>").add_to(m)
    print(route_ids)
    for bus_position in bus_positions['entity']:
        # print(bus_position['vehicle'])
        if "trip" in bus_position['vehicle'] and int(bus_position['vehicle']['trip']['routeId']) in route_ids:
            trips = Trips.objects.filter(trip_id__contains=bus_position['vehicle']['trip']['tripId'][0:7])
            trip_name = "Unknown"
            if len(trips) > 0:
                trip_name = trips[0].trip_headsign
            headsign = f"<h2>{trip_name}</h2>"
            
            folium.Marker(
                [float(bus_position['vehicle']['position']['latitude']), float(bus_position['vehicle']['position']['longitude'])], popup=folium.Popup(max_width=450, html=headsign, parse_html=False), icon=folium.Icon(color="green",icon='<i class="fa-solid fa-car"></i>')
            ).add_to(m)

    m = m._repr_html_()
    context = {"map": m}
    return render(request, "bike_crash_map.html", context=context)


@csrf_exempt
def bus_positions(request):
    if "route_id" in request.GET and request.GET['route_id']:
        route_id = request.GET['route_id']
        all_routes = False
    else:
        all_routes = True
    r = requests.get("https://data.texas.gov/download/cuc7-ywmd/text%2Fplain")
    bus_positions = json.loads(r.text)
    # print(bus_positions['entity'])
    m = folium.Map(location=[30.26807592381281, -97.74281180530993], zoom_start=12)
    for bus_position in bus_positions['entity']:
        # folium.Marker(
        #     [crash.latitude, crash.longitude], popup=folium.Popup(max_width=450, html=crash_summary, parse_html=False), icon=folium.Icon(color="red")
        # ).add_to(m)
        # print(bus_position)
        # print(bus_position['vehicle']['position']['latitude'])
        lat = bus_position['vehicle']['position']['latitude']
        # print(bus_position['vehicle']['position']['longitude'])
        lon = bus_position['vehicle']['position']['longitude']
        if "vehicle" in bus_position and "position" in bus_position['vehicle'] and "latitude" in bus_position['vehicle']['position']:
            # print("I'M GONN AKMSKS")
            # print(bus_position)
            if "trip" in bus_position['vehicle']:
                trip_id = bus_position['vehicle']['trip']['tripId']
                route = bus_position['vehicle']['trip']['routeId']
                print(trip_id)
                print(trip_id[:7])
                print(route)
                try:
                    trip = Trips.objects.filter(trip_id__contains=trip_id[:7])
                    headsign = f"<h1>{trip[0].trip_headsign}</h1>"
                    print("success")
                except:
                    headsign = "<h1>Unknown</h1>"
                    print("failure")

            else:
                headsign = "<h1>Unknown</h1>"
            if all_routes or (int(route) == int(route_id)):
                folium.Marker(
                    [float(bus_position['vehicle']['position']['latitude']), float(bus_position['vehicle']['position']['longitude'])], popup=folium.Popup(max_width=450, html=headsign, parse_html=False), icon=folium.Icon(color="red")
                ).add_to(m)
        # break

    m = m._repr_html_()
    context = {"map": m}
    return render(request, "bike_crash_map.html", context=context)
    
    # return JsonResponse({"hi": "hi"})


@csrf_exempt
def system_map(request):
    yesterday = (datetime.datetime.today()- datetime.timedelta(1)).replace(hour=0, minute=0, second=0, microsecond=0) 
    today = (datetime.datetime.today()).replace(hour=0, minute=0, second=0, microsecond=0) 
    print(today)
    service = CalendarDates.objects.filter(date__gt=yesterday, date__lte=today)
    services = []
    for s in service:
        print(s.service_id)
        print(s.date)
        services += [s.service_id]
    shapes = Trips.objects.filter(service_id__in=services).values('shape_id', "route_id__route_color", "route_id__route_short_name", "route_id__route_long_name").distinct()
    # for shape in shapes:
    #     print(shape)

    m = folium.Map(location=[30.26807592381281, -97.74281180530993], zoom_start=12)

    for shape in shapes:
        if int(shape['shape_id']) in (522, 428, 446, 142, 935, 670, 671, 457):
            continue
        print(shape)
        shapes_points = Shapes.objects.filter(shape_id=shape['shape_id'])
        line = []
        for shape_point in shapes_points:
            # print(f"{shape_point.shape_pt_lat}, {shape_point.shape_pt_lon}")
            line += [(float(shape_point.shape_pt_lat), float(shape_point.shape_pt_lon))]
        # line_string = LineString(line)
        tooltip = f"""
            <h1>{shape['route_id__route_long_name']} {shape['shape_id']}</h1>
        """
        folium.PolyLine(line, color=f"#{shape['route_id__route_color']}", tooltip=tooltip).add_to(m)
    m = m._repr_html_()
    context = {"map": m}
    return render(request, "bike_crash_map.html", context=context)


@csrf_exempt
def display_shape(request):

    shapes_points = Shapes.objects.filter(shape_id=request.GET['shape_id'])
    m = folium.Map(location=[30.26807592381281, -97.74281180530993], zoom_start=12)
    line=[]
    for shape_point in shapes_points:
        line += [(float(shape_point.shape_pt_lat), float(shape_point.shape_pt_lon))]
        tooltip = f"""
            <h1>{request.GET['shape_id']}</h1>
        """
        folium.PolyLine(line, color="red", tooltip=tooltip).add_to(m)
    m = m._repr_html_()
    context = {"map": m}
    return render(request, "bike_crash_map.html", context=context)

@csrf_exempt
def route(request):
    if "from_lat" in request.GET and request.GET['from_lat'] and "from_lon" in request.GET and request.GET['from_lon'] and "to_lat" in request.GET and request.GET['to_lat'] and "to_lon" in request.GET and request.GET['to_lon']:
        from_lat = float(request.GET['from_lat'])
        from_lon = float(request.GET['from_lon'])
        to_lat = float(request.GET['to_lat'])
        to_lon = float(request.GET['to_lon'])
        walk_dist = pow(pow(abs(to_lon - from_lon), 2) + pow(abs(to_lat-from_lat),2),(1/2))
        min_dist = walk_dist
        min_trip_id = "Walk"
        min_stop_id = None
        print("yes")
    else:
        return JsonResponse({"hi": "hi"})
    stops = Stops.objects.raw("""
        SELECT 
            SQRT(POWER(ABS(longitude - (%s)), 2) + POWER(ABS(latitude - (%s)), 2)) as distance,
            id, stop_id,
            stop_name, corner_placement,
            latitude, longitude
        FROM stops
        order by SQRT(POWER(ABS(longitude - (%s)), 2) + POWER(ABS(latitude - (%s)), 2)) ASC
        LIMIT 5;
    """, [from_lon, from_lat, from_lon, from_lat])

    stop_ids = []
    
    m = folium.Map(location=[from_lat, from_lon], zoom_start=12)
    for stop in stops:
        stop_ids += [stop.id]
        
        # move this into the next for loop, then write the upcoming schedule into the html object before adding the html to the stop marker

        folium.Marker(
            [stop.latitude, stop.longitude], popup=folium.Popup(max_width=450, html="<h1>Bus Stop</h1>", parse_html=False), icon=folium.Icon(color="red")
        ).add_to(m)
    for stop_id in stop_ids:
        cursor = connection.cursor()
        cursor.execute('''
            select time(stop_times.departure_time) as departs,
            trip_headsign,
            stops.stop_id,
            stops.stop_name,
            trips.shape_id,
            trips.id
            from stop_times
            left join trips on trips.id = stop_times.trip_id
            left join routes on trips.route_id = routes.id
            LEFT JOIN stops on stop_times.stop_id = stops.id
            where stop_times.trip_id in
            (select id from trips where service_id in 
            (select service_id from calendar_dates where date = 20230629))
            and departure_time > "1970-01-01 09:40:00"
            and departure_time < "1970-01-01 10:50:00"
            and stop_times.stop_id = %s
            order by stop_times.departure_time;

        ''', [stop_id])
        shape_ids = []
        trips = []
        trip_times = []
        for x in cursor.fetchall():
            if x[5] not in trips:
                trips += [x[5]]
            print(x)
            if int(x[4]) not in shape_ids:
                shape_ids += [int(x[4])]
        for trip_id in trips:
            min_dist = walk_dist
            min_stop_id = None
            arrival_time = None
            queryset = StopTimes.objects.filter(trip_id=trip_id).values('arrival_time', "stop_id", "stop_id__latitude", "stop_id__longitude", "trip_id__trip_headsign")
            for q in queryset:
                # print(q)
                potential_distance = pow(pow(abs(to_lon - q['stop_id__longitude']), 2) + pow(abs(to_lat-q['stop_id__latitude']),2),(1/2))
                if potential_distance < min_dist:
                    min_dist = potential_distance
                    min_trip_id = trip_id
                    min_stop_id = q['stop_id']
                    arrival_time = q['arrival_time']
                    headsign = q['trip_id__trip_headsign']
            trip_times += [{"trip_id": trip_id, "min_dist": min_dist, "from_stop": stop_id, "to_stop": min_stop_id, "arrival": arrival_time, "headsign": headsign}]
        for shape in shape_ids:
            shapes_points = Shapes.objects.filter(shape_id=shape)
            line = []
            for shape_point in shapes_points:
                # print(f"{shape_point.shape_pt_lat}, {shape_point.shape_pt_lon}")
                line += [(float(shape_point.shape_pt_lat), float(shape_point.shape_pt_lon))]
            # line_string = LineString(line)
            folium.PolyLine(line, tooltip="bus").add_to(m)

    m = m._repr_html_()
    context = {"map": m}
    # print(f"take trip #{min_trip_id} to stop {min_stop_id} and walk for {min_dist} degrees")
    print(trip_times)
    return render(request, "bike_crash_map.html", context=context)


@csrf_exempt
def address(request):
    return render(request, "address.html", context={})

@csrf_exempt
def monthly_ridership(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("date", "month", "year").annotate(riders=Round(Sum(F("number_days") * F("average_daily_riders")))).order_by("date")
    for row in performance:
        data += [{"year": row['year'], "month": row['month'], "date": row['date'], "riders": row['riders']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


@csrf_exempt
def monthly_revenue_hours(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("date", "month", "year").annotate(revenue_hours=Round(Sum(F("number_days") * F("revenue_hours")))).order_by("date")
    for row in performance:
        data += [{"year": row['year'], "month": row['month'], "date": row['date'], "revenue_hours": row['revenue_hours']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


@csrf_exempt
def monthly_revenue_miles(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("date", "month", "year").annotate(revenue_miles=Round(Sum(F("number_days") * F("revenue_miles")))).order_by("date")
    for row in performance:
        data += [{"year": row['year'], "month": row['month'], "date": row['date'], "revenue_miles": row['revenue_miles']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


@csrf_exempt
def monthly_total_hours(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("date", "month", "year").annotate(total_hours=Round(Sum(F("number_days") * F("total_hours")))).order_by("date")
    for row in performance:
        data += [{"year": row['year'], "month": row['month'], "date": row['date'], "total_hours": row['total_hours']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


@csrf_exempt
def monthly_total_miles(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("date", "month", "year").annotate(total_miles=Round(Sum(F("number_days") * F("total_miles")))).order_by("date")
    for row in performance:
        data += [{"year": row['year'], "month": row['month'], "date": row['date'], "total_miles": row['total_miles']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))









@csrf_exempt
def monthly_ridership_by_route(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("route_id__route_id", "date", "month", "year").annotate(riders=Round(Sum(F("number_days") * F("average_daily_riders")))).order_by("date")
    for row in performance:
        data += [{"route": row['route_id__route_id'], "year": row['year'], "month": row['month'], "date": row['date'], "riders": row['riders']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


@csrf_exempt
def monthly_revenue_hours_by_route(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("route_id__route_id", "date", "month", "year").annotate(revenue_hours=Round(Sum(F("number_days") * F("revenue_hours")))).order_by("date")
    for row in performance:
        data += [{"route": row['route_id__route_id'], "year": row['year'], "month": row['month'], "date": row['date'], "revenue_hours": row['revenue_hours']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


@csrf_exempt
def monthly_revenue_miles_by_route(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("route_id__route_id", "date", "month", "year").annotate(revenue_miles=Round(Sum(F("number_days") * F("revenue_miles")))).order_by("date")
    for row in performance:
        data += [{"route": row['route_id__route_id'], "year": row['year'], "month": row['month'], "date": row['date'], "revenue_miles": row['revenue_miles']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


@csrf_exempt
def monthly_total_hours_by_route(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("route_id__route_id", "date", "month", "year").annotate(total_hours=Round(Sum(F("number_days") * F("total_hours")))).order_by("date")
    for row in performance:
        data += [{"route": row['route_id__route_id'], "year": row['year'], "month": row['month'], "date": row['date'], "total_hours": row['total_hours']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


@csrf_exempt
def monthly_total_miles_by_route(request):
    # q = Q(route_id__route_id=7)
    data = []
    filters = {}
    q = Q()

    if "route_id" in request.GET and request.GET['route_id']:
        filters['route_id'] = request.GET['route_id']
        route_list = request.GET['route_id'].split(",")
        q &= Q(route_id__route_id__in=route_list)


    performance = RoutePerformance.objects.filter(q)\
        .values("route_id__route_id", "date", "month", "year").annotate(total_miles=Round(Sum(F("number_days") * F("total_miles")))).order_by("date")
    for row in performance:
        data += [{"route": row['route_id__route_id'], "year": row['year'], "month": row['month'], "date": row['date'], "total_miles": row['total_miles']}]
        length = len(data)
    resp = {
        "length": length,
        "data": data
    }
    return(JsonResponse(resp))


class StravaHeatmap(View):
    
    def get(self, request, *args, **kwargs):
        return render(request, "strava_heatmap.html")
