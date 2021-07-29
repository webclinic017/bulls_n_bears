import copy
import datetime
import os
import time

import requests
import pandas as pd
from django.shortcuts import render
from rest_framework import status
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from technical_indicator.constants import CSVs
from technical_indicator.models import CompanyWiseResistancesSupports, CompanyWiseChartData, PreData
from technical_indicator.utils import proxylist, five_minutes_candle_data, get_pre_data, get_curr_month_last_thursday, \
    get_new_insider_trades


class FutureAnalysis(TemplateView):
    template_name = 'future_analysis.html'


class InsiderTradingPage(TemplateView):
    template_name = 'insider_trades.html'


class LoadData(APIView):
    def post(self, request, *args, **kwargs):
        df = pd.read_csv('/home/shashank/Desktop/fo21JUN2021bhav.csv')
        df = df[df['INSTRUMENT'] == 'OPTSTK']
        comp_list = list(dict.fromkeys(list(df['SYMBOL'])))
        print(len(comp_list))
        dfs_ce, dfs_pe = [], []
        df_ce = df[df['OPTION_TYP'] == 'CE']
        df_pe = df[df['OPTION_TYP'] == 'PE']
        for comp in comp_list:
            dfs_ce.append(df_ce[df_ce['SYMBOL'] == comp])
            dfs_pe.append(df_pe[df_pe['SYMBOL'] == comp])
        for df_c, df_p in zip(dfs_ce, dfs_pe):
            symbol = list(df_c['SYMBOL'])[0]
            oi_list_ce = list(df_c['OPEN_INT'])
            oi_list_ce.sort()
            max_ce_oi_1, max_ce_oi_2, max_ce_oi_3 = oi_list_ce[-1], oi_list_ce[-2], oi_list_ce[-3]
            max_ce_oi_1_price = list(df_c[df_c['OPEN_INT'] == max_ce_oi_1]['STRIKE_PR'])[0]
            max_ce_oi_2_price = list(df_c[df_c['OPEN_INT'] == max_ce_oi_2]['STRIKE_PR'])[0]
            max_ce_oi_3_price = list(df_c[df_c['OPEN_INT'] == max_ce_oi_3]['STRIKE_PR'])[0]
            oi_list_pe = list(df_p['OPEN_INT'])
            oi_list_pe.sort()
            max_pe_oi_1, max_pe_oi_2, max_pe_oi_3 = oi_list_pe[-1], oi_list_pe[-2], oi_list_pe[-3]
            max_pe_oi_1_price = list(df_p[df_p['OPEN_INT'] == max_pe_oi_1]['STRIKE_PR'])[0]
            max_pe_oi_2_price = list(df_p[df_p['OPEN_INT'] == max_pe_oi_2]['STRIKE_PR'])[0]
            max_pe_oi_3_price = list(df_p[df_p['OPEN_INT'] == max_pe_oi_3]['STRIKE_PR'])[0]
            obj = CompanyWiseResistancesSupports.objects.filter(symbol=symbol)
            if obj:
                obj[0].delete()
            CompanyWiseResistancesSupports.objects.create(symbol=symbol,
                                                          first_high_res=max_ce_oi_1_price,
                                                          sec_high_res=max_ce_oi_2_price,
                                                          thr_high_res=max_ce_oi_3_price,
                                                          first_high_res_oi=max_ce_oi_1,
                                                          sec_high_res_oi=max_ce_oi_2,
                                                          thr_high_res_oi=max_ce_oi_3,
                                                          first_high_sup=max_pe_oi_1_price,
                                                          sec_high_sup=max_pe_oi_2_price,
                                                          thr_high_sup=max_pe_oi_3_price,
                                                          first_high_sup_oi=max_pe_oi_1,
                                                          sec_high_sup_oi=max_pe_oi_2,
                                                          thr_high_sup_oi=max_pe_oi_3)
        return Response({'status': True})


class LoadChartData(APIView):
    def post(self, request, *args, **kwargs):
        proxy = proxylist()
        date = datetime.date.today()
        # edt = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=15, minute=31, second=0)
        # edt = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=20, minute=50, second=0)
        s = requests.session()

        symbols_list = []
        # time.sleep(30)
        five_minutes_candle_data(s, proxy)

        query_set = CompanyWiseChartData.objects.all()
        if query_set:
            for qs in query_set:
                if len(qs.last_price['lastprice']) >= 3:
                    first = qs.value['value'][-4]
                    sec = qs.value['value'][-3]
                    thr = qs.value['value'][-2]
                    four = qs.value['value'][-1]
                    if (four - thr) > (thr - sec) and (thr - sec) > (sec - first):
                        print('volume found in :', qs.symbol)
                        if qs.last_price['lastprice'][-3] > qs.last_price['lastprice'][-2] and \
                                qs.last_price['lastprice'][-2] > qs.last_price['lastprice'][-1]:
                            print('company found :', qs.symbol)
        return Response({'status': True})


class HighestValueStocksListing(APIView):
    def post(self, request, *args, **kwargs):
        proxy = proxylist()
        date = datetime.date.today()
        edt = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=15, minute=31, second=0)
        s = requests.session()

        while datetime.datetime.now() < edt:
            time.sleep(295)
            # time.sleep(30)
            five_minutes_candle_data(s, proxy)
        return Response({'status': True})


class DisplayResult(TemplateView):
    template_name = 'templates/display_charts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query_set = CompanyWiseChartData.objects.all()
        if query_set:
            for qs in query_set:
                if len(qs.last_price['lastprice']) >= 3:
                    if qs.last_price['lastprice'][-1] < qs.last_price['lastprice'][-2] < qs.last_price['lastprice'][-3]:
                        if (qs.value['value'][-3] - qs.value['value'][-2]) > 0 and (
                                qs.value['value'][-2] - qs.value['value'][-1]) > 0:
                            context['company'] = qs.symbol
                            res_sup_qs = CompanyWiseResistancesSupports.objects.filter(symbol=qs.symbol)
                            if res_sup_qs:
                                context['first_res'] = res_sup_qs[0].first_high_res
                                context['sec_res'] = res_sup_qs[0].first_high_res
                                context['thr_res'] = res_sup_qs[0].first_high_res
                                context['first_sup'] = res_sup_qs[0].first_high_res
                                context['sec_sup'] = res_sup_qs[0].first_high_res
                                context['thr_sup'] = res_sup_qs[0].first_high_res
        return context


class PreDataStore(APIView):
    def post(self, request, *args, **kwargs):
        proxy = proxylist()
        date = datetime.date.today()
        edt = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=9, minute=8, second=0)
        # edt = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=22, minute=50, second=0)
        s = requests.session()

        while datetime.datetime.now() < edt:
            time.sleep(5)
            get_pre_data(s, proxy)
        return Response({'status': True})


class MarketDataTesting(APIView):
    def get(self, request, *args, **kwargs):
        comp_dict, comp_list = {}, []
        # import pdb; pdb.set_trace()
        for file in os.listdir('/home/shashank/Desktop/market_data_testing'):
            try:
                df = pd.read_csv('/home/shashank/Desktop/market_data_testing/' + file)

                temp_df = df[df['Total Traded Quantity'] > df['Total Traded Quantity'].quantile(0.75)]
                temp_df = temp_df[temp_df['Deliverable Qty'] > temp_df['Deliverable Qty'].quantile(0.75)]
                temp_df = temp_df[((temp_df['Close Price'] - temp_df['Open Price']) / temp_df['Open Price']) < 0.01]
                temp_df = temp_df[((temp_df['Close Price'] - temp_df['Open Price']) / temp_df['Open Price']) > -0.01]

                if ' 23-Jul-2021' in list(temp_df['Date']):
                    print('Inside')
                    comp_list.append(list(temp_df['Symbol'])[-1])

            except Exception as e:
                print(e)
                continue

        comp_dict['Stocks'] = comp_list
        # content = JSONRenderer().render(comp_dict)
        return Response(comp_dict, status=status.HTTP_200_OK)


class CheckFuturePriceCashPriceRelationship(APIView):
    def get(self, request, *args, **kwargs):
        expiry_date = request.data.get('expiry_date', get_curr_month_last_thursday())
        pattern = request.data.get('pattern', 'ALL')
        under_val = {}
        if expiry_date and pattern:
            cash_dfs = [pd.read_csv(csv_path) for csv_path in CSVs.get('cash_csv', None)]
            future_dfs = [pd.read_csv(csv_path) for csv_path in CSVs.get('future_csv', None)]
            for index, tup in enumerate(zip(cash_dfs, future_dfs)):
                cash_df, future_df = tup[0], tup[1]
                future_df = future_df[future_df['INSTRUMENT'] == 'FUTSTK']
                future_df = future_df[future_df['EXPIRY_DT'] == expiry_date]
                fo_symbols = list(future_df['SYMBOL'])
                for sym in fo_symbols:
                    # under_val.append(list((cash_df[cash_df['SYMBOL'] == sym])['CLOSE'])[0])
                    cash_val = (cash_df[cash_df['SYMBOL'] == sym])['CLOSE'].values[0]
                    future_val = (future_df[future_df['SYMBOL'] == sym])['CLOSE'].values[0]
                    per_rise = ((future_val - cash_val) / cash_val) * 100
                    if index == 0:
                        under_val[sym] = [per_rise]
                    else:
                        if under_val[sym]:
                            temp = under_val[sym]
                            temp.append(per_rise)
                            under_val[sym] = temp

            if pattern == 'RISING':
                under_val_copy = copy.deepcopy(under_val)
                for key, sym_list in under_val.items():
                    if not all(sym_list[i] <= sym_list[i + 1] for i in range(len(sym_list) - 1)):
                        del under_val_copy[key]
                return Response(under_val_copy, status=status.HTTP_200_OK)
            elif pattern == 'ALL':
                return Response(under_val, status=status.HTTP_200_OK)
        else:
            return Response('Expiry date or pattern is None Type', status=status.HTTP_200_OK)


class PublishNewInsiderTrade(APIView):
    def get(self, request, *args, **kwargs):
        try:
            s = requests.session()
            insider_json = get_new_insider_trades(s)
            return Response(insider_json, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response("Something nt wrong", status=status.HTTP_200_OK)