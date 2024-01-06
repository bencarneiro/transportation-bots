

import requests
from django.core.management.base import BaseCommand
from views.models import Crash
from views.views import save_crash

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
    #     parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        Crash.objects.all().delete()
        offset = 0
        keep_going = True
        while keep_going:
            vision_zero_data_api_url =f"https://data.austintexas.gov/resource/y2wy-tgr5.json?$order=crash_date%20DESC&$offset={offset}"

            response = requests.get(vision_zero_data_api_url)

            for incident in response.json():
                save_crash(incident)

            if len(response.json()) < 1000:
                keep_going = False
            else: 
                offset += 1000
                print(offset)