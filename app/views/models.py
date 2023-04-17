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