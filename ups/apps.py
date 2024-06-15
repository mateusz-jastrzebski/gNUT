from django.apps import AppConfig
from .nut2utils import WebNUT
import webNUT.config as config
import time
import threading


class UpsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ups'
    ups_list = {}
    webnut = None

    def ready(self):
        self.webnut = WebNUT(config.server, config.port, config.username, config.password)
        self.ups_list = self.webnut.get_ups_list()
        update_thread = threading.Thread(target=self.update_ups_list)
        update_thread.daemon = True
        update_thread.start()

    def update_ups_list(self):
        while True:
            try:
                self.ups_list = self.webnut.get_ups_list()
                time.sleep(3)
            except Exception as e:
                print(f"Error updating UPS list: {e}")
                self.handle_reconnection()

    def handle_reconnection(self):
        attempt = 1
        while True:
            try:
                print(f"Reconnecting... Attempt {attempt}")
                self.webnut = WebNUT(config.server, config.port, config.username, config.password)
                self.ups_list = self.webnut.get_ups_list()
                print("Reconnected successfully.")
                return
            except Exception as e:
                print(f"Reconnection failed: {e}")
                time.sleep(min(attempt, 10))  # Exponential backoff
                attempt += 1
