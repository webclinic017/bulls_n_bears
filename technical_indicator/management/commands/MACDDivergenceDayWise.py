import itertools

import numpy as np
from scipy.signal import argrelextrema
from django.core.management.base import BaseCommand
from technical_indicator.models import CompanyWiseChartData


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        qs = CompanyWiseChartData.objects.all()
        print(qs)
        if input("press enter"):
            pass
        for record in qs:
            if record.symbol == "ADANIPORTS" or 1 == 1:
                last_price_list = record.last_price.get("lastprice", None)
                macd_list = record.macd.get("macd", None)
                # macp_price_dictionary = { key:value for key,value in enumerate(zip(macd_list,last_price_list))}
                macd_np_arr = np.asarray(macd_list, dtype=np.float32)

                # for local maxima
                # macd_index_arr = argrelextrema(macd_np_arr, np.greater)

                # for local minima
                macd_index_arr = argrelextrema(macd_np_arr, np.less)

                macd_min_dict = {key: macd_np_arr[key] for key in macd_index_arr[0]}
                val = {
                    value: (tup[1] - tup[0])
                    for value, tup in zip(
                        list(itertools.combinations(list(macd_min_dict.keys()), 2)),
                        list(itertools.combinations(list(macd_min_dict.values()), 2)),
                    )
                    if (tup[1] - tup[0]) > 0
                    and last_price_list[value[0]] > last_price_list[value[1]]
                    and value[0] > (len(macd_list) - 30)
                    and value[1] > (len(macd_list) - 10)
                }
                print(record.symbol, "  ##################") if val else None
                for start, end in list(val.keys()):
                    print(
                        start,
                        " ",
                        last_price_list[start],
                        "  ",
                        macd_list[start],
                        "    ",
                        end,
                        " ",
                        last_price_list[end],
                        "  ",
                        macd_list[end],
                    )
                # if input('press enter'):
                #     pass
