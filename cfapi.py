import os

import requests

api_schema = 'https'
api_fqdn = 'api.cloudflare.com'
api_auth_email = os.getenv('CLOUDFLARE_EMAIL', default='')
api_auth_token = os.getenv('CLOUDFLARE_API_KEY', default='')
api_headers = {'X-Auth-Email': api_auth_email, 'X-Auth-Key': api_auth_token}

def list_zones():
    api_path = '/client/v4/zones/'
    api_query = {'per_page': 200}
    api_uri = f'{api_schema}://{api_fqdn}{api_path}'
    response = requests.get(api_uri, headers=api_headers, params=api_query)
    return response

def list_available_plans(zone_id: str):
    api_path = f'/client/v4/zones/{zone_id}/available_plans'
    api_query = {'per_page': 200}
    api_uri = f'{api_schema}://{api_fqdn}{api_path}'
    response = requests.get(api_uri, headers=api_headers, params=api_query)
    return response

def edit_zone_plan(zone_id: str, plan_id: str):
    api_path = f'/client/v4/zones/{zone_id}'
    api_uri = f'{api_schema}://{api_fqdn}{api_path}'
    api_body = {
        "plan": {
            "id": plan_id
        }
    }
    response = requests.patch(api_uri, headers=api_headers, json=api_body)
    return response
