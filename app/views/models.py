from django.db import models
from django.db.models import PositiveBigIntegerField, BigIntegerField

# Create your models here.


class TrafficReport(models.Model):

    traffic_report_id = models.CharField(max_length=256, primary_key=True)
    published_date = models.DateTimeField(null=False, blank=False)
    issue_reported = models.CharField(max_length=100, blank=False, null=False)
    location = models.CharField(max_length=100, blank=False, null=False)
    latitude = models.CharField(max_length=100, blank=False, null=False)
    longitude = models.CharField(max_length=100, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)
    traffic_report_status = models.CharField(max_length=100, blank=False, null=False)
    traffic_report_status_date_time = models.DateTimeField(null=False, blank=False)

    class Meta:
        managed = True
        db_table = 'traffic_report'


class Crash(models.Model):

    crash_id = models.PositiveBigIntegerField(primary_key=True)
    crash_fatal_fl = models.BooleanField(default=False) # this one needs to be converted from N / Y
    crash_date = models.DateTimeField(blank=False, null=False)
    case_id = models.CharField(max_length=256, null=True)
    rpt_latitude = models.FloatField(null=True)
    rpt_longitude = models.FloatField(null=True)
    rpt_block_num = models.CharField(max_length=256, null=True)
    rpt_street_pfx = models.CharField(max_length=256, null=True)
    rpt_street_name = models.CharField(max_length=256, null=True)
    rpt_street_sfx = models.CharField(max_length=256, null=True)
    crash_speed_limit = models.IntegerField(null=True)
    road_constr_zone_fl = models.BooleanField(default=False, null=True)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    street_name = models.CharField(max_length=256, null=True)
    street_nbr = models.CharField(max_length=256, null=True)
    street_name_2 = models.CharField(max_length=256, null=True)
    street_nbr_2 = models.CharField(max_length=256, null=True)
    crash_sev_id = models.PositiveIntegerField(null=True)
    sus_serious_injry_cnt = models.PositiveIntegerField(default=0)
    nonincap_injry_cnt = models.PositiveIntegerField(default=0)
    poss_injry_cnt = models.PositiveIntegerField(default=0)
    non_injry_cnt = models.PositiveIntegerField(default=0)
    unkn_injry_cnt = models.PositiveIntegerField(default=0)
    tot_injry_cnt = models.PositiveIntegerField(default=0)
    death_cnt = models.PositiveIntegerField(default=0)
    contrib_factr_p1_id = models.PositiveIntegerField(null=True)
    contrib_factr_p2_id = models.PositiveIntegerField(null=True)
    units_involved = models.CharField(max_length=512, null=True)
    atd_mode_category_metadata = models.TextField(null=True)
    pedestrian_fl = models.BooleanField(default=False)
    motor_vehicle_fl = models.BooleanField(default=False)
    motorcycle_fl = models.BooleanField(default=False)
    bicycle_fl = models.BooleanField(default=False)
    other_fl = models.BooleanField(default=False)
    point = models.CharField(max_length=256, null=True)
    apd_confirmed_fatality = models.BooleanField(default=False) # this one needs to be converted from N / Y
    apd_confirmed_death_count = models.PositiveIntegerField(default=0)
    motor_vehicle_death_count = models.PositiveIntegerField(default=0)
    motor_vehicle_serious_injury_count = models.PositiveIntegerField(default=0)
    bicycle_death_count = models.PositiveIntegerField(default=0)
    bicycle_serious_injury_count = models.PositiveIntegerField(default=0)
    pedestrian_death_count = models.PositiveIntegerField(default=0)
    pedestrian_serious_injury_count = models.PositiveIntegerField(default=0)
    motorcycle_death_count = models.PositiveIntegerField(default=0)
    motorcycle_serious_injury_count = models.PositiveIntegerField(default=0)
    other_death_count = models.PositiveIntegerField(default=0)
    other_serious_injury_count = models.PositiveIntegerField(default=0)
    onsys_fl = models.BooleanField(default=False)
    private_dr_fl = models.BooleanField(default=False)
        
    class Meta:
        managed = True
        db_table = 'crash'

class Animal(models.Model):
    
    animal_id = models.CharField(max_length=128, primary_key=True)
    name = models.CharField(max_length=256, null=True)
    datetime = models.DateTimeField()
    found_location = models.CharField(max_length=256, null=True)
    intake_type = models.CharField(max_length=256, null=True)
    intake_condition = models.CharField(max_length=256, null=True)
    animal_type = models.CharField(max_length=256, null=True)
    sex_upon_intake = models.CharField(max_length=256, null=True)
    age_upon_intake = models.CharField(max_length=256, null=True)
    breed = models.CharField(max_length=256, null=True)
    color = models.CharField(max_length=256, null=True)
    
    class Meta:
        managed = True
        db_table = 'animal'


class Mode(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=64, null=False)
    type = models.CharField(max_length=64, null=False)

    class Meta:
        managed=True
        db_table = "mode"

class Service(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=64, null=False)

    class Meta:
        managed=True
        db_table = "service"

class ExpenseType(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=64, null=False)
    budget = models.CharField(max_length=64, null=False)

    class Meta:
        managed=True
        db_table = "expense_type"

class TransitAgency(models.Model):

    id = models.AutoField(primary_key=True)
    last_report_year = models.IntegerField(null=True)
    ntd_id = models.PositiveIntegerField(null=True)
    legacy_ntd_id = models.CharField(max_length=128, null=True)
    agency_name = models.CharField(max_length=256, null=True)
    agency_status = models.CharField(max_length=64, null=True)
    reporter_type = models.CharField(max_length=64, null=True)
    reporting_module = models.CharField(max_length=64, null=True)
    city = models.CharField(max_length=64, null=True)
    state = models.CharField(max_length=8, null=True)
    census_year = models.IntegerField(null=True)
    uza_name = models.CharField(max_length=64, null=True)
    uza = models.IntegerField(null=True)
    uza_area_sqm = models.IntegerField(null=True)
    uza_population = models.BigIntegerField(null=True)
    status_2021 = models.CharField(max_length=64, null=True)

    class Meta:
        managed = True
        db_table = "transit_agency"
        constraints = [
            models.UniqueConstraint(fields=['ntd_id', 'legacy_ntd_id'], name='unique_registration')
        ]

class ConsumerPriceIndex(models.Model):
    year = models.IntegerField(primary_key=True)
    in_todays_dollars = models.FloatField(default=1)

    class Meta:
        managed=True
        db_table = "cpi"

class TransitExpense(models.Model):

    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.ForeignKey(ConsumerPriceIndex, on_delete=models.DO_NOTHING)
    expense_type = models.ForeignKey(ExpenseType, on_delete=models.DO_NOTHING, default="VO")
    expense = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "transit_expense"

class Fares(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING, default="nan")
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.ForeignKey(ConsumerPriceIndex, on_delete=models.DO_NOTHING)
    fares = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "fares"

class DirectionalRouteMiles(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    drm = models.IntegerField(null=False)

    class Meta:
        managed=True
        db_table = "drm"

class VehiclesOperatedMaximumService(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    voms = models.IntegerField(null=False)

    class Meta:
        managed=True
        db_table = "voms"

class VehicleRevenueMiles(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    vrm = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "vrm"

class VehicleRevenueHours(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    vrh = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "vrh"

class UnlinkedPassengerTrips(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    upt = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "upt"

class PassengerMilesTraveled(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    pmt = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "pmt"


# adding redundant fields for year + month and "date"
# this is just cause I don't know which will be easier to query - probably doesn't matter

class MonthlyUnlinkedPassengerTrips(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, blank=False)
    upt = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "monthly_upt"

class MonthlyVehiclesOperatedMaximumService(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, blank=False)
    voms = models.IntegerField(null=False)

    class Meta:
        managed=True
        db_table = "monthly_voms"

class MonthlyVehicleRevenueMiles(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, blank=False)
    vrm = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "monthly_vrm"

class MonthlyVehicleRevenueHours(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.ForeignKey(Mode, on_delete=models.DO_NOTHING, default="MB")
    service = models.ForeignKey(Service, on_delete=models.DO_NOTHING, default="DO")
    year = models.IntegerField(null=False)
    month = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, blank=False)
    vrh = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "monthly_vrh"


class Shapes(models.Model):
    id = models.AutoField(primary_key=True)
    shape_id = models.PositiveIntegerField(null=False)
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    shape_pt_lat = models.FloatField(null=False)
    shape_pt_lon = models.FloatField(null=False)
    shape_pt_sequence = models.PositiveIntegerField(null=True)
    shape_dist_traveled = models.FloatField(null=False)
    
    class Meta:
        managed=True
        db_table="shapes"

class CalendarDates(models.Model):

    id = models.AutoField(primary_key=True)
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    date = models.DateField(null=False)
    service_id = models.CharField(null=False, max_length=64)
    exception_type = models.IntegerField(default=1)

    class Meta:
        managed=True
        db_table = "calendar_dates"


class Routes(models.Model):

    id = models.AutoField(primary_key=True)
    route_id = models.PositiveBigIntegerField(null=False)
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    route_short_name = models.CharField(null=True, blank=True, max_length=64)
    route_long_name = models.CharField(null=True, blank=True, max_length=256)
    route_type = models.PositiveSmallIntegerField(null=True)
    route_url = models.CharField(null=True, blank=True, max_length=128)
    route_color = models.CharField(null=True, blank=True, max_length=16)
    route_text_color = models.CharField(null=True, blank=True, max_length=16)

    class Meta:
        managed=True
        db_table="routes"


class Trips(models.Model):

    id = models.AutoField(primary_key=True)
    trip_id = models.CharField(null=False, max_length=128)
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    route = models.ForeignKey(Routes, on_delete=models.DO_NOTHING)
    service_id = models.CharField(max_length=64)
    trip_headsign  = models.CharField(max_length=64)
    direction_id = models.IntegerField(default=0)
    block_id = models.CharField(max_length=64)
    shape_id = models.PositiveIntegerField(null=False)
    scheduled_trip_id = models.PositiveIntegerField(null=True, blank=True)
    trip_short_name = models.CharField(max_length=64)
    wheelchair_accessible = models.BooleanField(default=True)
    bikes_allowed = models.BooleanField(default=True)
    
    class Meta:
        managed=True
        db_table="trips"

class Stops(models.Model):
    id = models.AutoField(primary_key=True)
    stop_id = models.PositiveIntegerField(null=False)
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    at_street = models.CharField(max_length=128)
    corner_placement = models.CharField(max_length=16)
    heading = models.PositiveSmallIntegerField(null=True, blank=True)
    location_type = models.PositiveSmallIntegerField(null=True, blank=True)
    on_street = models.CharField(max_length=128)
    parent_station = models.PositiveSmallIntegerField(null=True, blank=True)
    stop_code = models.PositiveSmallIntegerField(null=True, blank=True)
    stop_desc = models.CharField(max_length=128)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    stop_name = models.CharField(max_length=128)
    stop_position = models.CharField(max_length=16)
    stop_timezone = models.CharField(max_length=16)
    stop_url = models.CharField(max_length=128)
    wheelchair_boarding = models.BooleanField(default=True)

    class Meta:
        managed=True
        db_table="stops"

class StopTimes(models.Model):
    id = models.AutoField(primary_key=True)
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    trip = models.ForeignKey(Trips, on_delete=models.DO_NOTHING)
    stop = models.ForeignKey(Stops, on_delete=models.DO_NOTHING)
    arrival_time = models.DateTimeField(null=True, blank=True)
    departure_time = models.DateTimeField(null=True, blank=True)
    stop_sequence = models.PositiveSmallIntegerField(null=True)
    pickup_type = models.PositiveSmallIntegerField(null=True)
    drop_off_type = models.PositiveSmallIntegerField(null=True)
    shape_dist_traveled = models.FloatField(null=True)
    timepoint = models.BooleanField(default=0)

    class Meta:
        managed=True
        db_table="stop_times"
