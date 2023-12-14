from django.core.management.base import BaseCommand
from views.models import TrafficReport
import requests
import datetime
from dateutil.parser import parse
from app.settings import MASTODON_API_BASE_URL, MASTODON_FIRST_SECRET, MASTODON_LOGIN_EMAIL, MASTODON_LOGIN_PASSWORD, MASTODON_SECOND_SECRET, GOOGLE_MAPS_API_KEY
from mastodon import Mastodon

api = Mastodon(MASTODON_FIRST_SECRET, MASTODON_SECOND_SECRET, api_base_url=MASTODON_API_BASE_URL)
api.log_in(MASTODON_LOGIN_EMAIL, MASTODON_LOGIN_PASSWORD, scopes=["read", "write"])

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
                google_maps_base_url = "https://maps.googleapis.com/maps/api/staticmap?center="
                map_request_url = google_maps_base_url + report['latitude'] + "," + report['longitude'] + "&key=" + GOOGLE_MAPS_API_KEY + "&zoom=20&size=1000x1000&maptype=satellite"
                response = requests.get(map_request_url)
                uploadable_media = api.media_post(response.content, mime_type="image", file_name=f"{report['traffic_report_id']}.jpg")
                media_id = uploadable_media['id']
                link = "https://www.google.com/maps/search/?api=1&query=" + report['latitude'] + "%2C" + report['longitude']
                # 30.281821%2C-97.708529
                status_text = f"{report['issue_reported']} at {report['address']} --- {link} --- #austin #austintx #traffic"
                api.status_post(status_text, media_ids=[media_id])
                print("NEW CRASH")
            else:
                print("break")
                break
