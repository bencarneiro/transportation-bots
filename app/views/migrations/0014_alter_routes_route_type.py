# Generated by Django 4.1.5 on 2023-06-26 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("views", "0013_routes_shapes_stops_trips_stoptimes_calendardates"),
    ]

    operations = [
        migrations.AlterField(
            model_name="routes",
            name="route_type",
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
