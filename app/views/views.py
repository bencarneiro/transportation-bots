from django.shortcuts import render
from views.models import Crash, TransitAgency, TransitExpense, UnlinkedPassengerTrips, PassengerMilesTraveled, VehicleRevenueHours, VehicleRevenueMiles, VehiclesOperatedMaximumService, DirectionalRouteMiles

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Sum, Count, Q, F
from django.db.models.functions import Round

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
        q &= Q(mode=mode_list)

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

    if "uza" in params and params['uza']:
        filters['uza'] = params['uza']
        uza_id_list = params['uza'].split(",")
        q &= Q(transit_agency_id__uza=uza_id_list)

    # if "city" in params and params['city']:
    #     filters['city'] = params['city']
    #     q &= Q(transit_agency_id__city=params['city'])

    if "state" in params and params['state']:
        filters['state'] = params['state']
        state_list = params['state'].split(",")
        q &= Q(transit_agency_id__state=state_list)
    
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
    ts = TransitExpense.objects.filter(q).values("year", "mode_id__type").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
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
def spending_by_mode(request):
    filters, q = process_params(request.GET)
    ts = TransitExpense.objects.filter(q).values("year", "mode_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
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
    ts = TransitExpense.objects.filter(q).values("year", "service_id__name").annotate(expense=Round(Sum(F('expense')*F("year_id__in_todays_dollars")))).order_by('year')
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
    ts = UnlinkedPassengerTrips.objects.filter(q).values("year", "mode_id__type").annotate(upt=Round(Sum("upt"))).order_by('year')
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
    ts = PassengerMilesTraveled.objects.filter(q).values("year", "mode_id__type").annotate(pmt=Round(Sum("pmt"))).order_by('year')
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
    ts = VehicleRevenueMiles.objects.filter(q).values("year", "mode_id__type").annotate(vrm=Round(Sum("vrm"))).order_by('year')
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
    ts = VehicleRevenueHours.objects.filter(q).values("year", "mode_id__type").annotate(vrh=Round(Sum("vrh"))).order_by('year')
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
    ts = DirectionalRouteMiles.objects.filter(q).values("year", "mode_id__type").annotate(drm=Round(Sum("drm"))).order_by('year')
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
    ts = VehiclesOperatedMaximumService.objects.filter(q).values("year", "mode_id__type").annotate(voms=Round(Sum("voms"))).order_by('year')
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
    ts = UnlinkedPassengerTrips.objects.filter(q).values("year", "service_id__name").annotate(upt=Round(Sum("upt"))).order_by('year')
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
    ts = PassengerMilesTraveled.objects.filter(q).values("year", "service_id__name").annotate(pmt=Round(Sum("pmt"))).order_by('year')
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
    ts = VehicleRevenueMiles.objects.filter(q).values("year", "service_id__name").annotate(vrm=Round(Sum("vrm"))).order_by('year')
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
    ts = VehicleRevenueHours.objects.filter(q).values("year", "service_id__name").annotate(vrh=Round(Sum("vrh"))).order_by('year')
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
    ts = DirectionalRouteMiles.objects.filter(q).values("year", "service_id__name").annotate(drm=Round(Sum("drm"))).order_by('year')
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
    ts = VehiclesOperatedMaximumService.objects.filter(q).values("year", "service_id__name").annotate(voms=Round(Sum("voms"))).order_by('year')
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
    ts = UnlinkedPassengerTrips.objects.filter(q).values("year", "mode_id__name").annotate(upt=Round(Sum("upt"))).order_by('year')
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
    ts = PassengerMilesTraveled.objects.filter(q).values("year", "mode_id__name").annotate(pmt=Round(Sum("pmt"))).order_by('year')
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
    ts = VehicleRevenueMiles.objects.filter(q).values("year", "mode_id__name").annotate(vrm=Round(Sum("vrm"))).order_by('year')
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
    ts = VehicleRevenueHours.objects.filter(q).values("year", "mode_id__name").annotate(vrh=Round(Sum("vrh"))).order_by('year')
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
    ts = DirectionalRouteMiles.objects.filter(q).values("year", "mode_id__name").annotate(drm=Round(Sum("drm"))).order_by('year')
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
    ts = VehiclesOperatedMaximumService.objects.filter(q).values("year", "mode_id__name").annotate(voms=Round(Sum("voms"))).order_by('year')
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
    return(JsonResponse({}))

@csrf_exempt
def cost_per_pmt(request):
    return(JsonResponse({}))

@csrf_exempt
def frr(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrh(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrm(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrh(request):
    return(JsonResponse({}))

@csrf_exempt
def vrm_per_vrh(request):
    return(JsonResponse({}))

@csrf_exempt
def upt_per_vrh(request):
    return(JsonResponse({}))

@csrf_exempt
def upt_per_vrm(request):
    return(JsonResponse({}))

@csrf_exempt
def pmt_per_vrh(request):
    return(JsonResponse({}))

@csrf_exempt
def pmt_per_vrm(request):
    return(JsonResponse({}))





@csrf_exempt
def cost_per_upt_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_pmt_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def frr_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrh_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrm_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrh_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def vrm_per_vrh_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def upt_per_vrh_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def upt_per_vrm_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def pmt_per_vrh_by_mode_type(request):
    return(JsonResponse({}))

@csrf_exempt
def pmt_per_vrm_by_mode_type(request):
    return(JsonResponse({}))





@csrf_exempt
def cost_per_upt_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_pmt_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def frr_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrh_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrm_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrh_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def vrm_per_vrh_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def upt_per_vrh_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def upt_per_vrm_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def pmt_per_vrh_by_mode(request):
    return(JsonResponse({}))

@csrf_exempt
def pmt_per_vrm_by_mode(request):
    return(JsonResponse({}))





@csrf_exempt
def cost_per_upt_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_pmt_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def frr_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrh_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrm_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def cost_per_vrh_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def vrm_per_vrh_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def upt_per_vrh_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def upt_per_vrm_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def pmt_per_vrh_by_service(request):
    return(JsonResponse({}))

@csrf_exempt
def pmt_per_vrm_by_service(request):
    return(JsonResponse({}))