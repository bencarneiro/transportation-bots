from django.core.management.base import BaseCommand
from views.models import TrafficReport
import requests

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
    #     parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        response = requests.get('https://data.austintexas.gov/resource/dx9v-zd7x.json?$order=published_date%20DESC')
        reports = response.json()
        for report in reports:
            print(report)
            new_incident = TrafficReport(
                traffic_report_id = report['traffic_report_id'],
                published_date = report['published_date'],
                issue_reported = report['issue_reported'],
                location = report['location'],
                latitude = report['latitude'],
                longitude = report['longitude'],
                address = report['address'],
                traffic_report_status = report['traffic_report_status'],
                traffic_report_status_date_time = report['traffic_report_status_date_time']
            ).save()



    #         traffic_report_id = models.BigIntegerField(primary_key=True)
    # published_date = models.DateTimeField(null=False, blank=False)
    # issue_reported = models.CharField(max_length=100, blank=False, null=False)
    # location = models.CharField(max_length=100, blank=False, null=False)
    # latitude = models.CharField(max_length=100, blank=False, null=False)
    # longitude = models.CharField(max_length=100, blank=False, null=False)
    # address = models.CharField(max_length=100, blank=False, null=False)
    # traffic_report_status = models.CharField(max_length=100, blank=False, null=False)
    # traffic_report_status_date_time = models.DateTimeField(null=False, blank=False)
    # traffic_report_status_date_time = models.DateTimeField(null=False, blank=False)
    # traffic_report_status_date_time = models.DateTimeField(null=False, blank=False)