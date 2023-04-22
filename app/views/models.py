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

    

class TransitExpense(models.Model):

    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.CharField(max_length=8, null=True)
    service = models.CharField(max_length=8, null=True)
    year = models.IntegerField(null=False)
    expense_type = models.CharField(max_length=64, null=False)
    expense = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "transit_expense"

class Fares(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.CharField(max_length=8, null=True)
    service = models.CharField(max_length=8, null=True)
    year = models.IntegerField(null=False)
    fares = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "fares"

class DirectionalRouteMiles(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.CharField(max_length=8, null=True)
    service = models.CharField(max_length=8, null=True)
    year = models.IntegerField(null=False)
    drm = models.IntegerField(null=False)

    class Meta:
        managed=True
        db_table = "drm"

class VehiclesOperatedMaximumService(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.CharField(max_length=8, null=True)
    service = models.CharField(max_length=8, null=True)
    year = models.IntegerField(null=False)
    voms = models.IntegerField(null=False)

    class Meta:
        managed=True
        db_table = "voms"

class VehicleRevenueMiles(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.CharField(max_length=8, null=True)
    service = models.CharField(max_length=8, null=True)
    year = models.IntegerField(null=False)
    vrm = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "vrm"

class VehicleRevenueHours(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.CharField(max_length=8, null=True)
    service = models.CharField(max_length=8, null=True)
    year = models.IntegerField(null=False)
    vrh = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "vrh"

class UnlinkedPassengerTrips(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.CharField(max_length=8, null=True)
    service = models.CharField(max_length=8, null=True)
    year = models.IntegerField(null=False)
    upt = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "upt"

class PassengerMilesTraveled(models.Model):
    transit_agency = models.ForeignKey(TransitAgency, on_delete=models.DO_NOTHING)
    mode = models.CharField(max_length=8, null=True)
    service = models.CharField(max_length=8, null=True)
    year = models.IntegerField(null=False)
    pmt = models.BigIntegerField(null=False)

    class Meta:
        managed=True
        db_table = "pmt"

class Mode(models.Model):
    id = models.CharField(primary_key=True, max_length=8)
    name = models.CharField(max_length=64, null=False)

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
