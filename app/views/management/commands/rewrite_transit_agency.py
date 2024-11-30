from django.core.management.base import BaseCommand
from views.models import *

from views.models import ConsumerPriceIndex
class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        cmta_id = TransitAgency.objects.get(ntd_id=60048).id
        

        Shapes.objects.all().update(transit_agency_id=cmta_id)
        CalendarDates.objects.all().update(transit_agency_id=cmta_id)
        Routes.objects.all().update(transit_agency_id=cmta_id)
        Trips.objects.all().update(transit_agency_id=cmta_id)
        Stops.objects.all().update(transit_agency_id=cmta_id)
        StopTimes.objects.all().update(transit_agency_id=cmta_id)
