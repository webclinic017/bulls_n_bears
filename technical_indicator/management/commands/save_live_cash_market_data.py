import requests
from django.core.management.base import BaseCommand
from technical_indicator.utils import five_minutes_live_stocks_listing


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        five_minutes_live_stocks_listing(requests.session())
