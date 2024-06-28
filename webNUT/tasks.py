from celery import shared_task
import requests
from django.conf import settings

@shared_task
def check_docker_image_version():
    # Fetch Docker image tags from Docker Hub
    url = 'https://hub.docker.com/v2/repositories/mjast/gnut/tags'
    response = requests.get(url)
    
    if response.status_code == 200:
        tags = response.json().get('results', [])
        if tags:
            latest_tag = tags[0]['name']  # Assuming tags are sorted by latest first
            print(f"Latest Docker image version: {latest_tag}")
            
            # Compare with APP_VERSION
            if latest_tag != settings.APP_VERSION:
                print(f"New version {latest_tag} available! Consider updating!...")
                # Add your logic to perform actions upon detecting a new version
                # For example, pull the new Docker image, restart containers, etc.
        else:
            print("No tags found for the Docker image")
    else:
        print(f"Failed to fetch Docker image tags. Status code: {response.status_code}")
