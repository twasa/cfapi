import json

import jmespath

import cfapi


def get_target_zone_list(json_file_path='./zone_list.json'):
    with open(json_file_path, 'r') as f:
        zone_dict_data = json.load(f)
        return zone_dict_data

def get_plan_id(json_file_path='./plan_id_map.json', plan='enterprise'):
    with open(json_file_path, 'r') as f:
        zone_id = json.load(f)
        return zone_id[plan]


def get_zones(parse_string: str):
    zone_list_response = cfapi.list_zones()
    if not zone_list_response.status_code == 200:
        print(f"error: {zone_list_response.text}")
        exit(1)
    dict_data = json.loads(zone_list_response.content)
    return jmespath.search(parse_string, dict_data)

def get_all_zones():
    parse_string = 'result[*].{name: name, id: id, plan: plan.legacy_id}'
    result = get_zones(parse_string)
    return result

def get_zones_by_plan_type(plan_type='enterprise'):
    zone_data = {"zones": get_all_zones()}
    parse_string = f"zones[?plan == '{plan_type}']"
    result = jmespath.search(parse_string, zone_data)
    return result

def pprint_all_zones(zones):
    print(json.dumps(zones, indent=4, sort_keys=True))

def bulk_edit_zone_plan(zone_list, plan_id):
    for zone in zone_list:  # type: ignore
        result = cfapi.edit_zone_plan(zone.get('id'), plan_id)
        if result.status_code == 200:
            dict_data = json.loads(result.content)
            print(json.dumps(dict_data, indent=4, sort_keys=True))
        else:
            print(f"change zone {zone} plan error: {result.text}")

pprint_all_zones(get_target_zone_list())
