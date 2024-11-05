

import requests
from django.core.management.base import BaseCommand
from views.models import Crash
from app.settings import MASTODON_API_BASE_URL, MASTODON_FIRST_SECRET, VISION_ZERO_EMAIL, MASTODON_LOGIN_PASSWORD, MASTODON_SECOND_SECRET, GOOGLE_MAPS_API_KEY
from mastodon import Mastodon
from dateutil.parser import parse
import datetime
from views.views import save_crash
import json
from dateutil import tz
import pytz
import calendar

api = Mastodon(MASTODON_FIRST_SECRET, MASTODON_SECOND_SECRET, api_base_url=MASTODON_API_BASE_URL)
api.log_in(VISION_ZERO_EMAIL, MASTODON_LOGIN_PASSWORD, scopes=["read", "write"])

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
                crash_exists = Crash.objects.get(crash_id=int(incident['crash_id']))
                print("Crash already in DB")
                break
            except:
                save_crash(incident)
                address = ""
                if "street_nbr" in incident:
                    address = incident['street_nbr']
                    address += " "
                if "street_name" in incident:
                    address += incident['street_name']
                if not address:
                    address = "NO ADDRESS"
                
                if "latitude" in incident and "longitude" in incident:
                    link = "https://www.google.com/maps/search/?api=1&query=" + incident['latitude'] + "%2C" + incident['longitude']
                    google_maps_base_url = "https://maps.googleapis.com/maps/api/staticmap?center="
                    map_request_url = google_maps_base_url + incident['latitude'] + "," + incident['longitude'] + "&key=" + GOOGLE_MAPS_API_KEY + "&zoom=20&size=1000x1000&maptype=satellite"
                    response = requests.get(map_request_url)
                    uploadable_media = api.media_post(response.content, mime_type="image", file_name=f"{incident['crash_id']}.jpg")
                    media_id = uploadable_media['id']
                else:
                    link = "NO LOCATION PROVIDED"
                    media_id = None

                crash_timestamp = incident['crash_timestamp'][0:10]

                crash_utc_time = parse(incident['crash_timestamp']).replace(tzinfo=tz.tzutc())
                my_datetime_cst = crash_utc_time.astimezone(pytz.timezone('US/Central')).strftime('%I:%M:%S %p')
                day_of_the_week = calendar.day_name[crash_utc_time.astimezone(pytz.timezone('US/Central')).weekday()]
                time_string = my_datetime_cst + " CST"
                description = f"Vision Zero Crash Report\n\nCollision at {address} at {time_string} on {day_of_the_week} {crash_timestamp} involving:"
                if "atd_mode_category_metadata" in incident:
                    for party in json.loads(incident['atd_mode_category_metadata']):
                        details = "("
                        # description = ""
                        description += "\n -"
                        description += party['mode_desc']
                        if int(party['death_cnt']) > 0:
                            details += f"{party['death_cnt']} Deaths, "
                        if int(party['sus_serious_injry_cnt']) > 0:
                            details += f"{party['sus_serious_injry_cnt']} Serious Injuries, "
                        if int(party['nonincap_injry_cnt']) > 0:
                            details += f"{party['nonincap_injry_cnt']} Non-Incapacitating Injuries, "
                        if int(party['non_injry_cnt']) > 0:
                            details += f"{party['non_injry_cnt']} Not Injured, "
                        if int(party['unkn_injry_cnt']) > 0:
                            details += f"{party['unkn_injry_cnt']} Unknown Injuries, "
                        if int(party['poss_injry_cnt']) > 0:
                            details += f"{party['poss_injry_cnt']} Possible Injuries"
                        if len(details) > 2 and details[-2:] == ", ":
                            details = details[:-2]
                        details += ")"
                        description += " "
                        description += details
                    description += f"\n\nLink to Location: {link}"
                    description += f"\nAdditional Info: {'https://data.austintexas.gov/resource/y2wy-tgr5.json?crash_id=' + incident['crash_id']}"
                    description += f"\n#visionzero #mobility #austin #accident #crash"
             
                    print(description)
                    if media_id:
                        api.status_post(description, media_ids=[media_id])
                    else:
                        api.toot(description)
        
                    # print()

                