import logging
from utils.menus import multi_choice_menu
from pprint import PrettyPrinter

pp = PrettyPrinter()

logger = logging.getLogger(__name__)


def get_zones(cf):
    '''Returns a dictionary of name, id for all zones availabe with given API key'''

    returned_zones = [
        {'name': zone['name'], 'id': zone['id']} for zone in cf.zones.get()]
    logging.info(
        f"| utilties | get_zones | Returned Zones: {returned_zones}\n")
    return returned_zones


def retrieve_dns_records(cf, zone_id):
    '''Returns a dictionary of all DNS records available in the zone selected'''

    required_fields = ['id', 'name', 'type', 'content',
                       'proxied', 'modified_on', 'created_on', ]
    returned_records = [{key: value for key, value in records.items(
    ) if key in required_fields} for records in cf.zones.dns_records.get(zone_id)]
    logging.info(
        f"| utilties | retrieve_dns_records | Returned Records: {returned_records}\n")
    return returned_records


def delete_dns_records(cf, zone_id):
    '''Deletes DNS record(s) available in the zone selected'''

    logging.info("| utilties | delete_dns_records | Initiated")

    retrieved_records = retrieve_dns_records(cf, zone_id)

    type_of_records = list(set([records['type']
                           for records in retrieved_records]))

    user_type_of_records = multi_choice_menu(
        message='DNS Type: ',
        options=type_of_records
    )
    user_records_to_delete = multi_choice_menu(
        message='Record To Delete: ',
        options=[(records['type'], records['name'])
                 for records in retrieved_records if records['type'] in user_type_of_records]
    )

    # Get record for the records to be deleted
    records_to_delete = []
    for user_record in user_records_to_delete:
        for record in retrieved_records:
            if user_record[0] is record['type'] and user_record[1] is record['name']:
                records_to_delete.append(record)

    pp.pprint(records_to_delete)
    logging.info(
        f"| main | Records to Delete: {[records['name'] for records in records_to_delete]}")

    for dns_record in records_to_delete:
        dns_record_id = dns_record['id']
        logging.info(
            f"| utilties | delete_dns_records | Deleted: Record - {dns_record['name']} of record type '{dns_record['type']}'")
        cf.zones.dns_records.delete(zone_id, dns_record_id)


def add_dns_record():
    '''Adds DNS record to zone selected'''

    logging.info("| utilties | add_dns_record | Returned Records: \n")
