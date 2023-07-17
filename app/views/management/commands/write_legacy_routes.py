
from django.core.management.base import BaseCommand
from views.models import Routes


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        
        Routes(
            route_id = 101,
            transit_agency_id = 1696,
            route_short_name = "IM",
            route_long_name = "Innovative Mobility",
            route_type = 3
        ).save

        Routes(
            route_id = 102,
            transit_agency_id = 1696,
            route_short_name = "MetroAccess",
            route_long_name = "MetroAccess - Paratransit",
            route_type = 3
        ).save()

        Routes(
            route_id = 17,
            transit_agency_id = 1696,
            route_short_name = "17",
            route_long_name = "17 - Cesar Chavez",
            route_type = 3
        ).save()

        Routes(
            route_id = 19,
            transit_agency_id = 1696,
            route_short_name = "19",
            route_long_name = "19 - Bull Creek",
            route_type = 3
        ).save()

        Routes(
            route_id = 6,
            transit_agency_id = 1696,
            route_short_name = "6",
            route_long_name = "6 - East 12th",
            route_type = 3
        ).save()

        Routes(
            route_id = 455,
            transit_agency_id = 1696,
            route_short_name = "455",
            route_long_name = "455 - Leander / Lakeline",
            route_type = 3
        ).save()

        Routes(
            route_id = 680,
            transit_agency_id = 1696,
            route_short_name = "680",
            route_long_name = "680 - North Riverside/Lakeshore",
            route_type = 3
        ).save()

        Routes(
            route_id = 681,
            transit_agency_id = 1696,
            route_short_name = "681",
            route_long_name = "681 - Intramural Fields/Far West",
            route_type = 3
        ).save()

        Routes(
            route_id = 682,
            transit_agency_id = 1696,
            route_short_name = "682",
            route_long_name = "682 - Forty Acres/East",
            route_type = 3
        ).save()


        Routes(
            route_id = 410,
            transit_agency_id = 1696,
            route_short_name = "410",
            route_long_name = "410 - West Campus",
            route_type = 3
        ).save()
        Routes(
            route_id = 411,
            transit_agency_id = 1696,
            route_short_name = "411",
            route_long_name = "411 - Riverside",
            route_type = 3
        ).save()
        Routes(
            route_id = 412,
            transit_agency_id = 1696,
            route_short_name = "412",
            route_long_name = "412 - Main Campus",
            route_type = 3
        ).save()

        Routes(
            route_id = 987,
            transit_agency_id = 1696,
            route_short_name = "987",
            route_long_name = "987 - Leander / Lakeline",
            route_type = 3
        ).save()

        Routes(
            route_id = 987,
            transit_agency_id = 1696,
            route_short_name = "987",
            route_long_name = "987 - Leander / Lakeline",
            route_type = 3
        ).save()
        Routes(
            route_id = 981,
            transit_agency_id = 1696,
            route_short_name = "981",
            route_long_name = "981 - Oak Knoll Express",
            route_type = 3
        ).save()

        Routes(
            route_id = 451,
            transit_agency_id = 1696,
            route_short_name = "451",
            route_long_name = "451 - Saltillo / Downtown Shuttle",
            route_type = 3
        ).save()
        Routes(
            route_id = 470,
            transit_agency_id = 1696,
            route_short_name = "470",
            route_long_name = "470 - Manor Circulator",
            route_type = 3
        ).save()

        Routes(
            route_id = 21,
            transit_agency_id = 1696,
            route_short_name = "21",
            route_long_name = "21 - Exposition / Clockwise",
            route_type = 3
        ).save()

        Routes(
            route_id = 22,
            transit_agency_id = 1696,
            route_short_name = "22",
            route_long_name = "22 - Chicon / Counterclockwise",
            route_type = 3
        ).save()

        Routes(
            route_id = 450,
            transit_agency_id = 1696,
            route_short_name = "450",
            route_long_name = "450 - Leander / Lakeline Shuttle",
            route_type = 3
        ).save()

        Routes(
            route_id = 455,
            transit_agency_id = 1696,
            route_short_name = "455",
            route_long_name = "455 - Leander / Lakeline Shuttle",
            route_type = 3
        ).save()

        Routes(
            route_id = 445,
            transit_agency_id = 1696,
            route_short_name = "445",
            route_long_name = "445 - Howard / New Life Shuttle",
            route_type = 3
        ).save()



        Routes(
            route_id = 275,
            transit_agency_id = 1696,
            route_short_name = "275",
            route_long_name = "275 - North Lamar Feeder",
            route_type = 3
        ).save()
        Routes(
            route_id = 100,
            transit_agency_id = 1696,
            route_short_name = "100",
            route_long_name = "100 - Airport",
            route_type = 3
        ).save()
        Routes(
            route_id = 110,
            transit_agency_id = 1696,
            route_short_name = "110",
            route_long_name = "110 - South Central Flyer",
            route_type = 3
        ).save()
        Routes(
            route_id = 122,
            transit_agency_id = 1696,
            route_short_name = "122",
            route_long_name = "122 - Four Points Ltd",
            route_type = 3
        ).save()
        Routes(
            route_id = 127,
            transit_agency_id = 1696,
            route_short_name = "127",
            route_long_name = "127 - Dove Springs Flyer",
            route_type = 3
        ).save()
        Routes(
            route_id = 240,
            transit_agency_id = 1696,
            route_short_name = "240",
            route_long_name = "240 - Rutland",
            route_type = 3
        ).save()
        Routes(
            route_id = 320,
            transit_agency_id = 1696,
            route_short_name = "320",
            route_long_name = "320 - St. Johns",
            route_type = 3
        ).save()
        Routes(
            route_id = 331,
            transit_agency_id = 1696,
            route_short_name = "331",
            route_long_name = "331 - Oltorf",
            route_type = 3
        ).save()

        Routes(
            route_id = 338,
            transit_agency_id = 1696,
            route_short_name = "338",
            route_long_name = "338 - Lamar / 45th",
            route_type = 3
        ).save()

        Routes(
            route_id = 464,
            transit_agency_id = 1696,
            route_short_name = "464",
            route_long_name = "464 - MLK / Capitol",
            route_type = 3
        ).save()

        Routes(
            route_id = 653,
            transit_agency_id = 1696,
            route_short_name = "653",
            route_long_name = "653 - Red River / UT",
            route_type = 3
        ).save()

        Routes(
            route_id = 970,
            transit_agency_id = 1696,
            route_short_name = "970",
            route_long_name = "970 - AMD / Lantana Campus",
            route_type = 3
        ).save()

        Routes(
            route_id = 37,
            transit_agency_id = 1696,
            route_short_name = "37",
            route_long_name = "37 - Colony Park/Windsor Park",
            route_type = 3
        ).save()


        Routes(
            route_id = 238,
            transit_agency_id = 1696,
            route_short_name = "238",
            route_long_name = "238 - Westgate",
            route_type = 3
        ).save()

        Routes(
            route_id = 983,
            transit_agency_id = 1696,
            route_short_name = "983",
            route_long_name = "983 - Leander Express",
            route_type = 3
        ).save()