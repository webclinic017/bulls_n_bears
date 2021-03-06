from datetime import datetime

import numpy as np
import requests

from technical_indicator.utils import get_strike_prices

QUANDL_API_KEY = "Y_b6qLJZMw_gK4zuCnk3"
COMPANIES = [
    "BANKINDIA",
    "SANOFI",
    "TATACONSUM",
    "MPHASIS",
    "BANDHANBNK",
    "LTI",
    "TORNTPOWER",
    "POLYCAB",
    "PNB",
    "IPCALAB",
    "HINDZINC",
    "VBL",
    "APOLLOTYRE",
    "SYNGENE",
    "HCLTECH",
    "ADANIPORTS",
    "CADILAHC",
    "M&MFIN",
    "IBULHSGFIN",
    "MGL",
    "BAJFINANCE",
    "INFY",
    "BOSCHLTD",
    "PFIZER",
    "COALINDIA",
    "AJANTPHARM",
    "PGHH",
    "UBL",
    "IDFCFIRSTB",
    "DALBHARAT",
    "GAIL",
    "AUBANK",
    "L&TFH",
    "ICICIGI",
    "TATAMOTORS",
    "TVSMOTOR",
    "SUNTV",
    "TITAN",
    "WIPRO",
    "BAJAJHLDNG",
    "INDHOTEL",
    "IGL",
    "ADANIENT",
    "BATAINDIA",
    "INDIGO",
    "TCS",
    "POWERGRID",
    "BANKBARODA",
    "ADANIGREEN",
    "GSPL",
    "BHARTIARTL",
    "CUB",
    "UNIONBANK",
    "PEL",
    "EXIDEIND",
    "HDFCAMC",
    "DRREDDY",
    "ATGL",
    "DEEPAKNTR",
    "WHIRLPOOL",
    "BHEL",
    "HINDALCO",
    "ESCORTS",
    "SUNPHARMA",
    "GODREJIND",
    "AMARAJABAT",
    "TRENT",
    "TATAELXSI",
    "PAGEIND",
    "AARTIIND",
    "HEROMOTOCO",
    "ASHOKLEY",
    "RECLTD",
    "NESTLEIND",
    "GLAND",
    "RELIANCE",
    "AUROPHARMA",
    "GRASIM",
    "COFORGE",
    "MFSL",
    "GODREJPROP",
    "BALKRISIND",
    "NAUKRI",
    "ADANITRANS",
    "MARICO",
    "TATACHEM",
    "DHANI",
    "PIDILITIND",
    "GLENMARK",
    "INDIA",
    "PETRONET",
    "BPCL",
    "COLPAL",
    "LAURUSLABS",
    "SBIN",
    "ASIANPAINT",
    "RAMCOCEM",
    "BIOCON",
    "SRTRANSFIN",
    "LT",
    "AMBUJACEM",
    "CASTROLIND",
    "MINDTREE",
    "CANBK",
    "SIEMENS",
    "BERGEPAINT",
    "SAIL",
    "FORTIS",
    "BHARATFORG",
    "AXISBANK",
    "ABCAPITAL",
    "LTTS",
    "IDEA",
    "PIIND",
    "ICICIPRULI",
    "MANAPPURAM",
    "ICICIBANK",
    "EICHERMOT",
    "OBEROIRLTY",
    "JINDALSTEL",
    "DABUR",
    "TATASTEEL",
    "PFC",
    "M&M",
    "ABBOTINDIA",
    "VOLTAS",
    "ZEEL",
    "JSWENERGY",
    "SBILIFE",
    "HAL",
    "TORNTPHARM",
    "JSWSTEEL",
    "HDFC",
    "JUBLFOOD",
    "APOLLOHOSP",
    "OIL",
    "NATCOPHARM",
    "BRITANNIA",
    "INDUSTOWER",
    "HDFCBANK",
    "COROMANDEL",
    "IOC",
    "LUPIN",
    "APLLTD",
    "DMART",
    "CONCOR",
    "BBTC",
    "BAJAJFINSV",
    "MRF",
    "CESC",
    "NAVINFLUOR",
    "DIXON",
    "CROMPTON",
    "HINDUNILVR",
    "IRCTC",
    "HAVELLS",
    "VEDL",
    "UPL",
    "SHREECEM",
    "ENDURANCE",
    "LICHSGFIN",
    "INDUSINDBK",
    "ITC",
    "EMAMILTD",
    "HDFCLIFE",
    "MUTHOOTFIN",
    "CIPLA",
    "ACC",
    "PRESTIGE",
    "NMDC",
    "CUMMINSIND",
    "SBICARD",
    "ULTRACEMCO",
    "INDIAMART",
    "NTPC",
    "KOTAKBANK",
    "HINDPETRO",
    "ONGC",
    "GUJGASLTD",
    "AUTO",
    "SRF",
    "YESBANK",
    "VGUARD",
    "ABFRL",
    "ALKEM",
    "TATAPOWER",
    "GODREJAGRO",
    "GMRINFRA",
    "RBLBANK",
    "MARUTI",
    "LALPATHLAB",
    "TECHM",
    "FEDERALBNK",
    "GODREJCP",
    "DLF",
    "CHOLAFIN",
    "BEL",
]

COLUMNS = [
    "Symbol",
    "Series",
    "Date",
    "Prev Close",
    "Open Price",
    "High Price",
    "Low Price",
    "Last Price",
    "Close Price",
    "Average Price",
    "Total Traded Quantity",
    "Turnover",
    "No. of Trades",
    "Deliverable Qty",
    "% Dly Qt to Traded Qty",
]

CSVs = {
    "cash_csv": [
        "/home/shashank/Desktop/cm16JUL2021bhav.csv",
        "/home/shashank/Desktop/cm19JUL2021bhav.csv",
        "/home/shashank/Desktop/cm20JUL2021bhav.csv",
    ],
    "future_csv": [
        "/home/shashank/Desktop/fo16JUL2021bhav.csv",
        "/home/shashank/Desktop/fo19JUL2021bhav.csv",
        "/home/shashank/Desktop/fo20JUL2021bhav.csv",
    ],
}