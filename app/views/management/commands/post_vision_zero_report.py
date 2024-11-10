

import requests
from django.core.management.base import BaseCommand
from views.models import Crash
from app.settings import VISION_ZERO_TOKEN, GOOGLE_MAPS_API_KEY
from mastodon import Mastodon
from dateutil.parser import parse
import datetime
from views.views import save_crash
import json
from dateutil import tz
import pytz
import calendar

api = Mastodon(api_base_url="https://mastodon.social", access_token=VISION_ZERO_TOKEN)

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
    #     parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        vision_zero_data_api_url =f"https://data.austintexas.gov/resource/y2wy-tgr5.json?$order=crash_timestamp%20DESC"

        response = requests.get(vision_zero_data_api_url)
        
        

        for incident in response.json():
            print(incident)
            try:
                crash_exists = Crash.objects.get(crash_id=int(incident['cris_crash_id']))
                print("Crash already in DB")
                break
            except:
                save_crash(incident)
                address = incident['address_primary'] + " / " + incident['address_secondary']
                
                if "latitude" in incident and "longitude" in incident:
                    link = "https://www.google.com/maps/search/?api=1&query=" + incident['latitude'] + "%2C" + incident['longitude']
                    google_maps_base_url = "https://maps.googleapis.com/maps/api/staticmap?center="
                    map_request_url = google_maps_base_url + incident['latitude'] + "," + incident['longitude'] + "&key=" + GOOGLE_MAPS_API_KEY + "&zoom=20&size=1000x1000&maptype=satellite"
                    response = requests.get(map_request_url)
                    uploadable_media = api.media_post(response.content, mime_type="image", file_name=f"{incident['cris_crash_id']}.jpg")
                    media_id = uploadable_media['id']
                else:
                    link = "NO LOCATION PROVIDED"
                    media_id = None

                crash_timestamp = incident['crash_timestamp'][0:10]

                crash_utc_time = parse(incident['crash_timestamp']).replace(tzinfo=tz.tzutc())
                my_datetime_cst = crash_utc_time.astimezone(pytz.timezone('US/Central')).strftime('%I:%M:%S %p')
                day_of_the_week = calendar.day_name[crash_utc_time.astimezone(pytz.timezone('US/Central')).weekday()]
                time_string = my_datetime_cst + " CST"
                
                description = f"Vision Zero Crash Report\n\nCollision at {address} at {time_string} on {day_of_the_week} {crash_timestamp} \ninvolving: {incident['units_involved']} \n{incident['death_cnt']} deaths and {incident['tot_injry_cnt']} injuries"
                description += f"\n\nLink to Location: {link}"
                description += f"\nAdditional Info: {'https://data.austintexas.gov/resource/y2wy-tgr5.json?cris_crash_id=' + incident['cris_crash_id']}"
                description += f"\n#visionzero #mobility #austin #accident #crash"
            
                print(description)
                if media_id:
                    api.status_post(description, media_ids=[media_id])
                else:
                    api.toot(description)
    
                # print()

            