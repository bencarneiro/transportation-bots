from django.core.management.base import BaseCommand
from views.models import TransitExpense, TransitAgency, Mode, Service, ExpenseType


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        # Save all the Service types
        Service(id="DO", name="Directly Operated").save()
        Service(id="PT", name="Purchased Transportation").save()
        Service(id="TX", name="Purchased Transportation").save()
        Service(id="TN", name="Other").save()
        Service(id="nan", name="Other").save()

        # Save all the expense types
        ExpenseType(id="VO", name="Vehicle Operations", budget="Operating").save()
        ExpenseType(id="VM", name="Vehicle Maintenance", budget="Operating").save()
        ExpenseType( id="NVM", name="Non-Vehicle Maintenance", budget="Operating").save()
        ExpenseType(id="GA", name="General Administration", budget="Operating").save()
        ExpenseType(id="RS", name="Rolling Stock", budget="Capital").save()
        ExpenseType(id="FC", name="Facilities", budget="Capital").save()
        ExpenseType(id="OC", name="Other Capital", budget="Operating").save()

        # save all the modes
        Mode(id="CB", name="Commuter Bus", type="Bus").save()
        Mode(id="DR", name="Demand Response", type="MicroTransit").save()
        Mode(id="DT", name="Demand Response (Taxi)", type="MicroTransit").save()
        Mode(id="FB", name="Ferryboat", type="Ferry").save()
        Mode(id="LR", name="Light Rail", type="Rail").save()
        Mode(id="MB", name="Local Bus", type="Bus").save()
        Mode(id="RB", name="Rapid Bus", type="Bus").save()
        Mode(id="SR", name="Streetcar", type="Rail").save()
        Mode(id="TB", name="Trolleybus", type="Bus").save()
        Mode(id="VP", name="Vanpool", type="MicroTransit").save()
        Mode(id="OT", name="Other", type="Other").save()
        Mode(id="nan", name="Other", type="Other").save()
        Mode(id="CR", name="Commuter Rail", type="Rail").save()
        Mode(id="YR", name="Hybrid Rail", type="Rail").save()
        Mode(id="OR", name="Other Rail", type="Rail").save()
        Mode(id="MG", name="Monorail", type="Rail").save()
        Mode(id="AR", name="Alaska Railroad", type="Rail").save()
        Mode(id="TR", name="Aerial Tramway", type="Other").save()
        Mode(id="HR", name="Heavy Rail", type="Rail").save()
        Mode(id="IP", name="Inclined Plane", type="Rail").save()
        Mode(id="PB", name="Publico", type="Bus").save()
        Mode(id="CC", name="Cable Car", type="Rail").save()
        Mode(id="JT", name="Jitney", type="MicroTransit").save()


