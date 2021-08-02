import nsepy
import pandas as pd
from datetime import date
from technical_indicator.constants import COMPANIES
from django.core.management.base import BaseCommand
from technical_indicator.utils import get_strike_prices
from technical_indicator.models import CompanyWiseOptionPremiumChartData


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # for comp in COMPANIES:
        #     print(comp)
        try:
            for strike_price in get_strike_prices('RELIANCE'):
                obj = CompanyWiseOptionPremiumChartData.objects.filter(symbol='RELIANCE',strike_price=float(strike_price))
                nsepy.live.
                response = nsepy.live.get_quote(
                    'RELIANCE', "EQ", "OPTSTK", "26AUG2021", "CE", float(strike_price)
                )
                data_list = response.get("data", None)
                data_dict = data_list[-1]
                if obj:
                    temp_last_price = obj[0].last_price["lastprice"]
                    temp_last_price.append(float(data_dict.get("lastPrice", None)))
                    obj[0].last_price["lastprice"] = temp_last_price
                    obj[0].save()
                else:
                    CompanyWiseOptionPremiumChartData.objects.create(
                        symbol='RELIANCE',
                        strike_price=float(strike_price),
                        last_price={
                            "lastprice": [float(data_dict.get("lastPrice", None))]
                        },
                    )
        except:
            # continue
            pass
