import json
import logging
import CloudFlare
import pprint
from datetime import datetime
from utils.utilities import delete_dns_records, get_zones, retrieve_dns_records
from utils.menus import single_choice_menu

pp = pprint.PrettyPrinter()

json_file = open("settings.json")
data = json.load(json_file)

EMAIL = data.get("CLOUDFLARE_EMAIL")
API = data.get("CLOUDFLARE_GLOBAL_API")

AVAILABLE_FUNCTIONS = [
    'Retrieve DNS Records',
    'Delete DNS Records'
]


def main():
    formatter = '%(asctime)s:%(levelname)s:%(message)s'
    filename = f'logs/{datetime.now().strftime("%Y%m%d-%H%M%S")}.log'
    # filename = 'logs/test.log'
    logging.basicConfig(filename=filename,
                        level=logging.DEBUG,
                        format=formatter,
                        filemode='w')

    cf = CloudFlare.CloudFlare(EMAIL, API)

    choosen_zone = get_zones(cf)[single_choice_menu(
        message="Please choose a zone: ",
        options=[zone.get('name') for zone in get_zones(cf)]
    )]

    choosen_function = AVAILABLE_FUNCTIONS[single_choice_menu(
        message="Please choose a function: ",
        options=AVAILABLE_FUNCTIONS
    )]

    if choosen_function == AVAILABLE_FUNCTIONS[0]:
        # Retrieve DNS Records
        logging.info(f"| main | Choosen Function: {choosen_function}")
        retrieved_records = retrieve_dns_records(cf, choosen_zone['id'])
        pp.pprint(retrieved_records)
        logging.info(f"| main | Retrieved Records: {retrieved_records}")
    elif choosen_function == AVAILABLE_FUNCTIONS[1]:
        # Add DNS Records
        logging.info(f"| main | Choosen Function: {choosen_function}")
    elif choosen_function == AVAILABLE_FUNCTIONS[2]:
        # Delete DNS Records
        delete_dns_records(cf, choosen_zone['id'])
        logging.info(f"| main | Choosen Function: {choosen_function}")


if __name__ == '__main__':
    main()
