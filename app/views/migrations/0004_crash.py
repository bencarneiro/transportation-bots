# Generated by Django 3.2 on 2023-04-17 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0003_alter_trafficreport_traffic_report_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crash',
            fields=[
                ('crash_id', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('crash_fatal_fl', models.BooleanField(default=False)),
                ('crash_date', models.DateTimeField()),
                ('case_id', models.CharField(max_length=256, null=True)),
                ('rpt_latitude', models.FloatField(null=True)),
                ('rpt_longitude', models.FloatField(null=True)),
                ('rpt_block_num', models.CharField(max_length=256, null=True)),
                ('rpt_street_pfx', models.CharField(max_length=256, null=True)),
                ('rpt_street_name', models.CharField(max_length=256, null=True)),
                ('rpt_street_sfx', models.CharField(max_length=256, null=True)),
                ('crash_speed_limit', models.IntegerField(null=True)),
                ('road_constr_zone_fl', models.BooleanField(default=False, null=True)),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('street_name', models.CharField(max_length=256, null=True)),
                ('street_nbr', models.CharField(max_length=256, null=True)),
                ('street_name_2', models.CharField(max_length=256, null=True)),
                ('street_nbr_2', models.CharField(max_length=256, null=True)),
                ('crash_sev_id', models.PositiveIntegerField(null=True)),
                ('sus_serious_injry_cnt', models.PositiveIntegerField(default=0)),
                ('nonincap_injry_cnt', models.PositiveIntegerField(default=0)),
                ('poss_injry_cnt', models.PositiveIntegerField(default=0)),
                ('non_injry_cnt', models.PositiveIntegerField(default=0)),
                ('unkn_injry_cnt', models.PositiveIntegerField(default=0)),
                ('tot_injry_cnt', models.PositiveIntegerField(default=0)),
                ('death_cnt', models.PositiveIntegerField(default=0)),
                ('contrib_factr_p1_id', models.PositiveIntegerField(null=True)),
                ('contrib_factr_p2_id', models.PositiveIntegerField(null=True)),
                ('units_involved', models.CharField(max_length=512, null=True)),
                ('atd_mode_category_metadata', models.TextField(null=True)),
                ('pedestrian_fl', models.BooleanField(default=False)),
                ('motor_vehicle_fl', models.BooleanField(default=False)),
                ('motorcycle_fl', models.BooleanField(default=False)),
                ('bicycle_fl', models.BooleanField(default=False)),
                ('other_fl', models.BooleanField(default=False)),
                ('point', models.CharField(max_length=256, null=True)),
                ('apd_confirmed_fatality', models.BooleanField(default=False)),
                ('apd_confirmed_death_count', models.PositiveIntegerField(default=0)),
                ('motor_vehicle_death_count', models.PositiveIntegerField(default=0)),
                ('motor_vehicle_serious_injury_count', models.PositiveIntegerField(default=0)),
                ('bicycle_death_count', models.PositiveIntegerField(default=0)),
                ('bicycle_serious_injury_count', models.PositiveIntegerField(default=0)),
                ('pedestrian_death_count', models.PositiveIntegerField(default=0)),
                ('pedestrian_serious_injury_count', models.PositiveIntegerField(default=0)),
                ('motorcycle_death_count', models.PositiveIntegerField(default=0)),
                ('motorcycle_serious_injury_count', models.PositiveIntegerField(default=0)),
                ('other_death_count', models.PositiveIntegerField(default=0)),
                ('other_serious_injury_count', models.PositiveIntegerField(default=0)),
                ('onsys_fl', models.BooleanField(default=False)),
                ('private_dr_fl', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'crash',
                'managed': True,
            },
        ),
    ]