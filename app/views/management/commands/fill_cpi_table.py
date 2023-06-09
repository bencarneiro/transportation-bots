from django.core.management.base import BaseCommand

from views.models import ConsumerPriceIndex
class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        ConsumerPriceIndex(year=1989, in_todays_dollars=2.3741935483871).save()
        ConsumerPriceIndex(year=1990, in_todays_dollars=2.25248661055853).save()
        ConsumerPriceIndex(year=1991, in_todays_dollars=2.16152716593245).save()
        ConsumerPriceIndex(year=1992, in_todays_dollars=2.0983606557377).save()
        ConsumerPriceIndex(year=1993, in_todays_dollars=2.03737024221453).save()
        ConsumerPriceIndex(year=1994, in_todays_dollars=1.98650472334683).save()
        ConsumerPriceIndex(year=1995, in_todays_dollars=1.93175853018373).save()
        ConsumerPriceIndex(year=1996, in_todays_dollars=1.87635436583811).save()
        ConsumerPriceIndex(year=1997, in_todays_dollars=1.83426791277259).save()
        ConsumerPriceIndex(year=1998, in_todays_dollars=1.80613496932515).save()
        ConsumerPriceIndex(year=1999, in_todays_dollars=1.76710684273709).save()
        ConsumerPriceIndex(year=2000, in_todays_dollars=1.70963995354239).save()
        ConsumerPriceIndex(year=2001, in_todays_dollars=1.66233766233766).save()
        ConsumerPriceIndex(year=2002, in_todays_dollars=1.63646470261256).save()
        ConsumerPriceIndex(year=2003, in_todays_dollars=1.6).save()
        ConsumerPriceIndex(year=2004, in_todays_dollars=1.55849655902594).save()
        ConsumerPriceIndex(year=2005, in_todays_dollars=1.50742447516641).save()
        ConsumerPriceIndex(year=2006, in_todays_dollars=1.46031746031746).save()
        ConsumerPriceIndex(year=2007, in_todays_dollars=1.42016401350699).save()
        ConsumerPriceIndex(year=2008, in_todays_dollars=1.36739433348816).save()
        ConsumerPriceIndex(year=2009, in_todays_dollars=1.37249417249417).save()
        ConsumerPriceIndex(year=2010, in_todays_dollars=1.34983952315452).save()
        ConsumerPriceIndex(year=2011, in_todays_dollars=1.30902623388173).save()
        ConsumerPriceIndex(year=2012, in_todays_dollars=1.28222996515679).save()
        ConsumerPriceIndex(year=2013, in_todays_dollars=1.26351931330472).save()
        ConsumerPriceIndex(year=2014, in_todays_dollars=1.24376848331221).save()
        ConsumerPriceIndex(year=2015, in_todays_dollars=1.242194092827).save()
        ConsumerPriceIndex(year=2016, in_todays_dollars=1.22666666666667).save()
        ConsumerPriceIndex(year=2017, in_todays_dollars=1.20114239086087).save()
        ConsumerPriceIndex(year=2018, in_todays_dollars=1.17244125846276).save()
        ConsumerPriceIndex(year=2019, in_todays_dollars=1.15134923738756).save()
        ConsumerPriceIndex(year=2020, in_todays_dollars=1.13755795981453).save()
        ConsumerPriceIndex(year=2021, in_todays_dollars=1.08634686346863).save()
        ConsumerPriceIndex(year=2022, in_todays_dollars=1).save()