import pandas as pd
from django.core.management.base import BaseCommand
from technical_indicator.models import CompanyWiseChartData


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # import pdb;pdb.set_trace()
        query_set = CompanyWiseChartData.objects.all()
        for record in query_set:
            print(record.symbol)
            try:
                df = pd.DataFrame({"Close": record.last_price.get("lastprice", None)})
                df.reset_index(level=0, inplace=True)
                exp1 = df.Close.ewm(span=12, adjust=False).mean()
                exp2 = df.Close.ewm(span=26, adjust=False).mean()
                macd = exp1 - exp2
                exp3 = macd.ewm(span=9, adjust=False).mean()
                record.macd["macd"] = list(macd)
                record.signal["signal"] = list(exp3)
                record.save()
            except:
                continue
