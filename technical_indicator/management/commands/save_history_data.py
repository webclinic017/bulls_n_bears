import nsepy
import pandas as pd
from datetime import date
from technical_indicator.constants import COMPANIES
from django.core.management.base import BaseCommand
from technical_indicator.models import CompanyWiseChartData


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        obj = CompanyWiseChartData.objects.all()
        if obj:
            obj.delete()
        for comp in COMPANIES:
            print(comp)
            try:
                data = nsepy.get_history(
                    symbol=comp, start=date(2020, 1, 1), end=date(2021, 7, 30)
                )
                CompanyWiseChartData.objects.create(
                    symbol=comp, last_price={"lastprice": list(data["Close"])}
                )
            except:
                continue
