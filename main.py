import requests
import json
from moodle_connection import get_cookie_key

with open('utils/./request.json', 'r') as f:
    data = json.load(f)

credentials = get_cookie_key()

calendar = requests.post(data['url'], params={'sesskey': credentials[1], 'info': 'core_calendar_get_calendar_monthly_view'}, headers=data['headers'], cookies=credentials[0], json=data['body']).json()

for data_set in calendar[0].get('data').get('weeks'):
    for dias in data_set.get('days'):
        if dias.get('hasevents'):
            for eventos in dias.get('events'):
                print(f'Nome do evento: { eventos.get("name") }')