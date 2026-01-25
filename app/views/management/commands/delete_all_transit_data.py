from django.core.management.base import BaseCommand
from views.models import *

from views.models import ConsumerPriceIndex
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        Shapes.objects.all().update(transit_agency_id=None)
        CalendarDates.objects.all().update(transit_agency_id=None)
        Routes.objects.all().update(transit_agency_id=None)
        Trips.objects.all().update(transit_agency_id=None)
        Stops.objects.all().update(transit_agency_id=None)
        StopTimes.objects.all().update(transit_agency_id=None)
        print("y")
        MonthlyUnlinkedPassengerTrips.objects.all().delete()
        MonthlyVehicleRevenueHours.objects.all().delete()
        MonthlyVehicleRevenueMiles.objects.all().delete()
        MonthlyVehiclesOperatedMaximumService.objects.all().delete()
        print("monthlies done")
        UnlinkedPassengerTrips.objects.all().delete()
        VehicleRevenueHours.objects.all().delete()
        VehicleRevenueMiles.objects.all().delete()
        print("VRM DONE")
        VehiclesOperatedMaximumService.objects.all().delete()
        PassengerMilesTraveled.objects.all().delete()
        DirectionalRouteMiles.objects.all().delete()
        print("about to do expenses")
        for year in range(1980, 2025):
            print(year)
            TransitExpense.objects.filter(year=year).delete()
        Fares.objects.all().delete()
        print("Fares done")

        TransitAgency.objects.all().delete()
        Mode.objects.all().delete()
        Service.objects.all().delete()