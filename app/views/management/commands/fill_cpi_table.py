from django.core.management.base import BaseCommand

from views.models import ConsumerPriceIndex
class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        cpi = ConsumerPriceIndex.objects.get(year=1991)
        cpi.in_todays_dollars=2.36637298091043
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=1992)
        cpi.in_todays_dollars=2.29722024233785
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=1993)
        cpi.in_todays_dollars=2.23044982698962
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=1994)
        cpi.in_todays_dollars=2.17476383265857
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=1995)
        cpi.in_todays_dollars=2.11482939632546
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=1996)
        cpi.in_todays_dollars=2.05417463352454
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=1997)
        cpi.in_todays_dollars=2.00809968847352
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=1998)
        cpi.in_todays_dollars=1.97730061349693
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=1999)
        cpi.in_todays_dollars=1.93457382953181
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2000)
        cpi.in_todays_dollars=1.87166085946574
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2001)
        cpi.in_todays_dollars=1.81987577639752
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2002)
        cpi.in_todays_dollars=1.79155086158977
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2003)
        cpi.in_todays_dollars=1.75163043478261
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2004)
        cpi.in_todays_dollars=1.70619375330863
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2005)
        cpi.in_todays_dollars=1.65028161802355
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2006)
        cpi.in_todays_dollars=1.59871031746032
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2007)
        cpi.in_todays_dollars=1.55475156777617
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2008)
        cpi.in_todays_dollars=1.49698095680446
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2009)
        cpi.in_todays_dollars=1.5025641025641
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2010)
        cpi.in_todays_dollars=1.47776249426868
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2011)
        cpi.in_todays_dollars=1.43308136949755
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2012)
        cpi.in_todays_dollars=1.4037456445993
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2013)
        cpi.in_todays_dollars=1.38326180257511
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2014)
        cpi.in_todays_dollars=1.36163920574567
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2015)
        cpi.in_todays_dollars=1.35991561181435
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2016)
        cpi.in_todays_dollars=1.34291666666667
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2017)
        cpi.in_todays_dollars=1.31497348021216
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2018)
        cpi.in_todays_dollars=1.28355236957388
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2019)
        cpi.in_todays_dollars=1.26046147829488
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2020)
        cpi.in_todays_dollars=1.24536321483771
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2021)
        cpi.in_todays_dollars=1.18929889298893
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2022)
        cpi.in_todays_dollars=1.101127434233
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2023)
        cpi.in_todays_dollars=1.05776173285199
        cpi.save()
        cpi = ConsumerPriceIndex.objects.get(year=2024)
        cpi.in_todays_dollars=1.02741472744661
        cpi.save()
        ConsumerPriceIndex(year=2025, in_todays_dollars=1).save()