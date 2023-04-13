from django.core.management.base import BaseCommand
from views.models import TrafficReport
import requests
import datetime
from dateutil.parser import parse

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
    #     parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):

        last_crash = TrafficReport.objects.latest("published_date")
        last_crash_time = last_crash.published_date

        response = requests.get('https://data.austintexas.gov/resource/dx9v-zd7x.json?$order=published_date%20DESC')
        reports = response.json()
        for report in reports:
            print(report)
            if parse(report['published_date']) > last_crash_time:
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
                print("NEW CRASH")
            else:
                print("break")
                break
