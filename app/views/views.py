from django.shortcuts import render
from views.models import Crash, TransitAgency, TransitExpense, UnlinkedPassengerTrips, Fares, PassengerMilesTraveled, VehicleRevenueHours, VehicleRevenueMiles, VehiclesOperatedMaximumService, DirectionalRouteMiles

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
            riders=1
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
        print(x)
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
    upt_ts = UnlinkedPassengerTrips.objects.filter(q)\
        .values("year").annotate(
            bus_upt=Round(Sum("upt"), filter=Q(mode_id__type="Bus")),
            rail_upt=Round(Sum("upt"), filter=Q(mode_id__type="Rail")),
            microtransit_upt=Round(Sum("upt"), filter=Q(mode_id__type="MicroTransit")),
            ferry_upt=Round(Sum("upt"), filter=Q(mode_id__type="Ferry")),
            other_upt=Round(Sum("upt"), filter=Q(mode_id__type="Other")),
        ).order_by('year')
    data = []
    for x in spending_ts:
        bus_opexp = x['bus_opexp']
        rail_opexp = x['rail_opexp']
        microtransit_opexp = x['microtransit_opexp']
        ferry_opexp = x['ferry_opexp']
        other_opexp = x['other_opexp']

        ridership = upt_ts.get(year=x['year'])

        if ridership['bus_upt'] and ridership['bus_upt'] > 0:
            bus_upt = ridership['bus_upt']
        else:
            bus_upt = 1
        if ridership['rail_upt'] and ridership['rail_upt'] > 0:
            rail_upt = ridership['rail_upt']
        else:
            rail_upt = 1
        if ridership['microtransit_upt'] and ridership['microtransit_upt'] > 0:
            microtransit_upt = ridership['microtransit_upt']
        else:
            microtransit_upt = 1
        if ridership['ferry_upt'] and ridership['ferry_upt'] > 0:
            ferry_upt = ridership['ferry_upt']
        else:
            ferry_upt = 1
        if ridership['other_upt'] and ridership['other_upt'] > 0:
            other_upt = ridership['other_upt']
        else:
            other_upt = 1

        bus_cpp = round(bus_opexp/bus_upt, 2)
        rail_cpp = round(rail_opexp/rail_upt, 2)
        microtransit_cpp = round(microtransit_opexp/microtransit_upt, 2)
        ferry_cpp = round(ferry_opexp/ferry_upt, 2)
        other_cpp = round(other_opexp/other_upt, 2)

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
            bus_pmt=Round(Sum("pmt"), filter=Q(mode_id__type="Bus")),
            rail_pmt=Round(Sum("pmt"), filter=Q(mode_id__type="Rail")),
            microtransit_pmt=Round(Sum("pmt"), filter=Q(mode_id__type="MicroTransit")),
            ferry_pmt=Round(Sum("pmt"), filter=Q(mode_id__type="Ferry")),
            other_pmt=Round(Sum("pmt"), filter=Q(mode_id__type="Other")),
        ).order_by('year')
    data = []
    for x in spending_ts:
        bus_opexp = x['bus_opexp']
        rail_opexp = x['rail_opexp']
        microtransit_opexp = x['microtransit_opexp']
        ferry_opexp = x['ferry_opexp']
        other_opexp = x['other_opexp']

        ridership = pmt_ts.get(year=x['year'])

        if ridership['bus_pmt'] and ridership['bus_pmt'] > 0:
            bus_pmt = ridership['bus_pmt']
        else:
            bus_pmt = 1
        if ridership['rail_pmt'] and ridership['rail_pmt'] > 0:
            rail_pmt = ridership['rail_pmt']
        else:
            rail_pmt = 1
        if ridership['microtransit_pmt'] and ridership['microtransit_pmt'] > 0:
            microtransit_pmt = ridership['microtransit_pmt']
        else:
            microtransit_pmt = 1
        if ridership['ferry_pmt'] and ridership['ferry_pmt'] > 0:
            ferry_pmt = ridership['ferry_pmt']
        else:
            ferry_pmt = 1
        if ridership['other_pmt'] and ridership['other_pmt'] > 0:
            other_pmt = ridership['other_pmt']
        else:
            other_pmt = 1

        bus_cpp = round(bus_opexp/bus_pmt, 2)
        rail_cpp = round(rail_opexp/rail_pmt, 2)
        microtransit_cpp = round(microtransit_opexp/microtransit_pmt, 2)
        ferry_cpp = round(ferry_opexp/ferry_pmt, 2)
        other_cpp = round(other_opexp/other_pmt, 2)

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
            bus_fares=Sum(F('fares'), mode_id__type="Bus"),
            rail_fares=Sum(F('fares'), mode_id__type="Rail"),
            microtransit_fares=Sum(F('fares'), mode_id__type="MicroTransit"),
            ferry_fares=Sum(F('fares'), mode_id__type="Ferry"),
            other_fares=Sum(F('fares'), mode_id__type="Other"),
        )\
        .order_by('year')
    data = []

    for x in spending_ts:
        if x['bus_opexp'] and x['bus_opexp'] > 0:
            bus_opexp = x['bus_opexp']
        else:
            bus_opexp = 1
        if x['rail_opexp'] and x['rail_opexp'] > 0:
            rail_opexp = x['rail_opexp']
        else: 
            rail_opexp = 1
        if x['microtransit_opexp'] and x['microtransit_opexp'] > 0:
            microtransit_opexp = x['microtransit_opexp']
        else: 
            microtransit_opexp = 1
        if x['ferry_opexp'] and x['ferry_opexp'] > 0:
            ferry_opexp = x['ferry_opexp']
        else: 
            ferry_opexp = 1
        if x['other_opexp'] and x['other_opexp'] > 0:
            other_opexp = x['other_opexp']
        else: 
            other_opexp = 1
        
        revenue = fares_ts.get(year=x['year'])
        bus_fares=revenue['bus_fares']
        rail_fares=revenue['rail_fares']
        microtransit_fares=revenue['microtransit_fares']
        ferry_fares=revenue['ferry_fares']
        other_fares=revenue['other_fares']
        bus_frr = round(bus_fares/bus_opexp, 4)
        rail_frr = round(rail_fares/rail_opexp, 4)
        microtransit_frr = round(microtransit_fares/microtransit_opexp, 4)
        ferry_frr = round(ferry_fares/ferry_opexp, 4)
        other_frr = round(other_fares/other_opexp, 4)
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
        if x['bus'] and x["bus"] > 0:
            bus_vrh = x['bus']
        else:
            bus_vrh = 1
        if x['rail'] and x["rail"] > 0:
            rail_vrh = x['rail']
        else:
            rail_vrh = 1
        if x['microtransit'] and x["microtransit"] > 0:
            microtransit_vrh = x['microtransit']
        else:
            microtransit_vrh = 1
        if x['ferry'] and x["ferry"] > 0:
            ferry_vrh = x['ferry']
        else:
            ferry_vrh = 1
        if x['other'] and x["other"] > 0:
            other_vrh = x['other']
        else:
            other_vrh = 1
        vrm = vrm_ts.get(year=x['year'])
        bus_vrm = vrm['bus']
        rail_vrm = vrm['rail']
        microtransit_vrm = vrm['microtransit']
        ferry_vrm = vrm['ferry']
        other_vrm = vrm['other']
        bus_mph = round(bus_vrm / bus_vrh, 2)
        rail_mph = round(rail_vrm / rail_vrh, 2)
        microtransit_mph = round(microtransit_vrm / microtransit_vrh, 2)
        ferry_mph = round(ferry_vrm / ferry_vrh, 2)
        other_mph = round(other_vrm / other_vrh, 2)
        data += [{"bus": bus_mph, "rail": rail_mph, "microtransit": microtransit_mph, "ferry": ferry_mph, "other": other_mph}]
    length = len(data)
    resp = {
        "filters": filters,
        "length": length,
        "data": data
    }
    return JsonResponse(resp, safe=False)

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

# @csrf_exempt
# def cost_per_vrh_by_mode(request):
#     return(JsonResponse({}))

# @csrf_exempt
# def cost_per_vrm_by_mode(request):
#     return(JsonResponse({}))

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

# @csrf_exempt
# def cost_per_vrh_by_service(request):
#     return(JsonResponse({}))

# @csrf_exempt
# def cost_per_vrm_by_service(request):
#     return(JsonResponse({}))

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