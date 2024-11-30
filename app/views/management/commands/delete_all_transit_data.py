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

        MonthlyUnlinkedPassengerTrips.objects.all().delete()
        MonthlyVehicleRevenueHours.objects.all().delete()
        MonthlyVehicleRevenueMiles.objects.all().delete()
        MonthlyVehiclesOperatedMaximumService.objects.all().delete()
        UnlinkedPassengerTrips.objects.all().delete()
        VehicleRevenueHours.objects.all().delete()
        VehicleRevenueMiles.objects.all().delete()
        VehiclesOperatedMaximumService.objects.all().delete()
        PassengerMilesTraveled.objects.all().delete()
        DirectionalRouteMiles.objects.all().delete()
        TransitExpense.objects.all().delete()
        Fares.objects.all().delete()

        TransitAgency.objects.all().delete()
        Mode.objects.all().delete()
        Service.objects.all().delete()