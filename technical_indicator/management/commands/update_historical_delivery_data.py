import os
import pandas as pd
from csv import writer
from django.core.management.base import BaseCommand
from technical_indicator.constants import COMPANIES, COLUMNS


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        bhavcopy_df = pd.read_csv("/home/shashank/Desktop/sec_bhavdata_full.csv")
        for comp in COMPANIES:
            if comp in list(bhavcopy_df["SYMBOL"]):
                temp_df = bhavcopy_df[bhavcopy_df['SYMBOL'] == comp]
                record = temp_df.reset_index().to_dict('records')[0]
                del record['index']
                print(comp)
                for file in os.listdir('/home/shashank/Desktop/market_data_testing'):
                    if comp in file:
                        with open(f'/home/shashank/Desktop/market_data_testing/{file}', 'a') as f_object:
                            writer_object = writer(f_object)
                            writer_object.writerow(list(record.values()))
                            f_object.close()
                            break
