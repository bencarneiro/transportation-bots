from django.core.management.base import BaseCommand
from views.models import Animal

from dateutil.parser import parse
import requests
from app.settings import MASTODON_API_BASE_URL, MASTODON_FIRST_SECRET, MASTODON_PUPPY_EMAIL, MASTODON_LOGIN_PASSWORD, MASTODON_SECOND_SECRET
from mastodon import Mastodon
api = Mastodon(MASTODON_FIRST_SECRET, MASTODON_SECOND_SECRET, api_base_url=MASTODON_API_BASE_URL)
api.log_in(MASTODON_PUPPY_EMAIL, MASTODON_LOGIN_PASSWORD, scopes=["read", "write"])

class Command(BaseCommand):

    # def add_arguments(self, parser):
    #     parser.add_argument('start_block', type=int, help='scrape transactions starting with this Block #')
    #     parser.add_argument('end_block', type=int, help='Stop Scraping Transactions when this block # is reached')

    def handle(self, *args, **kwargs):
        # Animal.objects.get(animal_id="A878834").delete()
        response = requests.get('https://data.austintexas.gov/resource/wter-evkm.json?$order=DateTime%20DESC')
        animals = response.json()
        for animal in animals:
            try:
                animal_exists = Animal.objects.get(animal_id=animal['animal_id'])
                print("this shit is logged")
                break
            except:
                print(animal)
                name = "(nameless)"
                if "name" in animal:
                    name = animal['name']
                found_location = None
                if "found_location" in animal:
                    found_location = animal['found_location']
                intake_type = None
                if "intake_type" in animal:
                    intake_type = animal['intake_type']
                intake_condition = None
                if "intake_condition" in animal:
                    intake_condition = animal['intake_condition']
                animal_type = None
                if "animal_type" in animal:
                    animal_type = animal['animal_type']
                sex_upon_intake = None
                if "sex_upon_intake" in animal:
                    sex_upon_intake = animal['sex_upon_intake']
                age_upon_intake = None
                if "age_upon_intake" in animal:
                    age_upon_intake = animal['age_upon_intake']
                breed = None
                if "breed" in animal:
                    breed = animal['breed']
                color = None
                if "color" in animal:
                    color = animal['color']

                # break
                new_animal = Animal(
                    animal_id=animal['animal_id'],
                    datetime=animal['datetime'],
                    found_location=found_location,
                    intake_type=intake_type,
                    intake_condition=intake_condition,
                    animal_type=animal_type,
                    sex_upon_intake=sex_upon_intake,
                    age_upon_intake=age_upon_intake,
                    breed=breed,
                    color=color
                ).save()

                print("SAVED")
                datetime = parse(animal['datetime']).strftime('%I:%M:%S %p %Y-%m-%d')
                toot = f"{animal_type} alert! {name} is a {age_upon_intake} {sex_upon_intake} {color} {breed}. \nThey were found near {found_location} at {datetime}.\n\nIntake Type: {intake_type} \nIntake Condition: {intake_condition} \n\nThey are now at the Austin Animal Center - If unclaimed, the animal will be available for adoption in 3 days"
                api.toot(toot)
                print(f"tooted for {animal['animal_id']}")
                # print(toot)
              
                