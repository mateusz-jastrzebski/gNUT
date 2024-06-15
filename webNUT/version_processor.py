# myapp/context_processors.py
import subprocess
import json
from datetime import datetime
from django.conf import settings
import requests

def version_processor(request):
    app_version = settings.APP_VERSION
    year_of_release = get_year_of_release(app_version)
    return {
        'APP_VERSION': app_version,
        'YEAR_OF_RELEASE': year_of_release
    }

def get_year_of_release(tag):
    if tag == 'DEV': return datetime.now().year
    url = f"https://hub.docker.com/v2/repositories/mjast/gnut/tags/{tag}"
    headers = {
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if 'tag_last_pushed' in data:
            return data['tag_last_pushed'].split('-')[0]
        else:
            return None
    else:
        print(f"Error fetching tag information for {tag}: {response.status_code} - {response.text}")
        return None
