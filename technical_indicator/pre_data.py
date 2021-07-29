import json
import time
import random

import requests
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from utils import links

headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}

def proxylist():

    driver = webdriver.Chrome(ChromeDriverManager().install())
    time.sleep(5)
    driver.get("https://free-proxy-list.net/")
    time.sleep(5)
    proxy = []
    for row in range(20):
        '/html/body/section[1]/div/div[2]/div/div[2]/div/table/tbody/tr[1]/td[2]'
        ip = driver.find_element_by_xpath(
            '/html/body/section[1]/div/div[2]/div/div[2]/div/table/tbody/tr[{}]/td[1]'.format(row+1))
        port = driver.find_element_by_xpath(
            '/html/body/section[1]/div/div[2]/div/div[2]/div/table/tbody/tr[{}]/td[2]'.format(row+1))
        proxy.append('{}:{}'.format(ip.text, port.text))
    driver.close()

    return proxy


def total_pre_data():
    proxy = proxylist()
    # date = datetime.date.today()
    # edt = datetime.datetime(day=date.day, month=date.month, year=date.year, hour=18, minute=15, second=0)
    # # edt = datetime.datetime(day=date.day,month=date.month,year=date.year,hour=9,minute=8,second=0)
    s = requests.session()
    # c = 0
    # print(datetime.datetime.now(), edt)
    symbols, pc, lp, ato_buy, ato_sell, total_buy, total_sell = [], [], [], [], [], [], []
    # while datetime.datetime.now() < edt:
    try:
        # print(c,"count")
        # c += 1
        url = 'https://www.nseindia.com/api/market-data-pre-open?key=ALL'

        # load cookies:
        s.get('https://www.nseindia.com/get-quotes/derivatives?symbol=INFY', headers=headers,
              proxies={"http": "http://{}".format(random.choice(proxy))})

        # get data:
        data = s.get(url, headers=headers).json()
        data_dict = json.dumps(data, indent=4)
        data_list = data.get('data', None)
        if data_list:
            for element in data_list:
                # print(element.get('metadata', None).get('symbol', None), element.get('metadata', None).get('previousClose', None), element.get('metadata', None).get('lastPrice', None))
                symbols.append(element.get('metadata', None).get('symbol', None))
                pc.append(element.get('metadata', None).get('previousClose', None))
                lp.append(element.get('metadata', None).get('iep', None))
                ato_buy.append(element.get('detail', None).get('preOpenMarket', None).get('ato', None).get('totalBuyQuantity', None))
                ato_sell.append(element.get('detail', None).get('preOpenMarket', None).get('ato', None).get('totalSellQuantity', None))
                total_buy.append(element.get('detail', None).get('preOpenMarket', None).get('totalBuyQuantity', None))
                total_sell.append(element.get('detail', None).get('preOpenMarket', None).get('totalSellQuantity', None))
        # print(len(symbols), len(pc), len(lp))

        # print(data.get('data', None)[0].get('metadata', None).get('symbol', None))
        # print(data.get('data', None)[0].get('metadata', None).get('previousClose', None))
        # print(data.get('data', None)[0].get('metadata', None).get('lastPrice', None))
        # for i in range(len(data.get('records',0).get('data',0))):
        #     print(data.get('records',0).get('data',0)[i].get('CE',0))
        # if input('press e'):
        #     pass

        # file = open("/home/shashank/workspace/post_fial_market_data_{}_{}_2.csv".format('ADANIPORTS',datetime.datetime.now()),'a+')
        # #open(BASE_DIR + '/data/' + BHAV_FILE_NAME, 'wb')
        # file.write(json.dumps(data))
        # file.close()
        # df=pd.DataFrame(data['data'])
        # print(df.columns.values)
        # try:
        #     df.drop(['chart30dPath', 'chartTodayPath', 'priority', 'meta', 'chart365dPath'], axis=1, inplace=True)
        # except:
        #     pass
        # pat="/home/shashank/workspace/post_fial_market_data_{}_{}_2.csv".format('BALKRISIND',date)
        # if os.path.exists(pat):
        #     df.to_csv(pat,mode='a',index=False,header=False)
        # else:
        #     df.to_csv(pat,mode='a',index=False)

        # if c % 50 == 0:
        #     s = requests.session()
        #
        # if c % 1000 == 0:
        #     proxy = proxylist()

    except Exception as e:
        print(e)
        exit()
            # continue
    print(len(symbols), len(pc), len(lp))
    main_df = pd.DataFrame({'Symbols': symbols, 'Previous_Price': pc, 'Last_Price': lp, 'ATO_BUY': ato_buy,
                            'ATO_SELL': ato_sell, 'Total_Buy': total_buy, 'Total_Sell': total_sell})
    print(main_df.shape)
    print(main_df.head())
    main_df.to_csv('pre_data.csv')

#total_pre_data()

def zerodha(start=0,end=len(links)):

    if end<=len(links):
        driver = webdriver.Chrome(ChromeDriverManager().install())
        time.sleep(5)
        driver.get("https://kite.zerodha.com/")
        time.sleep(5)
        user_id = driver.find_element_by_id("userid")
        time.sleep(5)
        user_id.send_keys("FV6804")
        time.sleep(5)
        password = driver.find_element_by_id("password")
        time.sleep(5)
        password.send_keys("used@121987")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[4]/button").click()
        time.sleep(5)
        pin = driver.find_element_by_id("pin")
        time.sleep(5)
        pin.send_keys("521521")
        time.sleep(5)
        driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div/div/div/form/div[3]/button").click()
        time.sleep(5)
        for link in links[start:end]:
            driver.get(link)
            time.sleep(5)
    else:
        print("end is more than total links")
zerodha()