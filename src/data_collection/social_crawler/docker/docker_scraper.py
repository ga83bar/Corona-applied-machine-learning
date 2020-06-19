import json
import os
import cloudscraper
from requests import get

ip = get('https://api.ipify.org').text

scr_type = os.environ['JOBT']
file_id = os.environ['IDX']

rsp = {'addr': ip, 'type': scr_type, 'file_id': file_id}

docker_path = '/results'

with open(os.path.join(docker_path, file_id), 'w') as f:
    json.dump(rsp, f)
