import random
import json
import requests
import datetime
import time
from python_graphql_client import GraphqlClient
import asyncio
import mysql.connector
from prometheus_client.core import Summary, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server, Gauge
from prometheus_api_client import PrometheusConnect


class Skew:
    def openInterest():
        dataBase = mysql.connector.connect(
            host="localhost",
            user="ribbon",
            passwd="password"
        )

        metrics = "http://localhost:9090/"

        deribit_ribbon_sql = "INSERT INTO ribbon.deribit_ribbon_skew (timestamp, strike, venue, oi) VALUES (%s, %s, %s, %s)"
        deribit_sql = "INSERT INTO ribbon.deribit_skew (timestamp, strike, venue, oi) VALUES (%s, %s, %s, %s)"

        # rBTC-THETA
        r = requests.get(
            'https://deribit.com/api/v2/public/get_instruments?currency=BTC&expired=false&kind=option')
        req = r.json()

        ## get current strike prices and expiry
        prom = PrometheusConnect(url=metrics, disable_ssl=True)
        btc_strike_price = prom.custom_query(
            query="query_vaultShortPositions_strikePrice{job='rBTC-THETA'} / 100000000")
        btc_strike_price = round(float(btc_strike_price[0]["value"][1]))
        btc_exp = prom.custom_query(
            query="query_vaultShortPositions_expiry{job='rBTC-THETA'} * 1000")
        btc_exp = float(btc_exp[0]["value"][1])

        ## filter by strike and expiry
        a = list(
            filter(lambda x: x["expiration_timestamp"] == btc_exp, req["result"]))

        # with ribbon
        for option in a:
            if option["instrument_name"].split("-")[3] == "C":
             r = requests.get(
                 "https://deribit.com/api/v2/public/get_book_summary_by_instrument?instrument_name=" + option["instrument_name"])
             print("https://deribit.com/api/v2/public/get_book_summary_by_instrument?instrument_name=" + option["instrument_name"])
             req = r.json()
             oi = req["result"][0]["open_interest"]

             ribbon_oi = prom.custom_query(
                    query="query_vaults_totalBalance{job='rBTC-THETA'} / 100000000")
             total_oi = oi

             if option["strike"] == btc_strike_price:
              total_oi = oi + float(ribbon_oi[0]["value"][1])

             timestamp = datetime.datetime.fromtimestamp(
                 int(option["expiration_timestamp"])/1000).strftime('%Y-%m-%d')
             strike = option["strike"]
             venue = "deribit"

             val = (timestamp, strike, venue, total_oi)
             dataBase.cursor().execute(deribit_ribbon_sql, val)
             dataBase.commit() 

            print("Inserted with ribbon %s %s", "deribit_ribbon_skew", strike)

        # without ribbon
        for option in a:
            if option["instrument_name"].split("-")[3] == "C":
             r = requests.get(
                 "https://deribit.com/api/v2/public/get_book_summary_by_instrument?instrument_name=" + option["instrument_name"])
             print("https://deribit.com/api/v2/public/get_book_summary_by_instrument?instrument_name=" +
                   option["instrument_name"])
             req = r.json()
             oi = req["result"][0]["open_interest"]
             total_oi = oi

             timestamp = datetime.datetime.fromtimestamp(
                 int(option["expiration_timestamp"])/1000).strftime('%Y-%m-%d')
             strike = option["strike"]
             venue = "deribit"

             val = (timestamp, strike, venue, total_oi)
             dataBase.cursor().execute(deribit_sql, val)
             dataBase.commit()

            print("Inserted without %s %s", "deribit_skew", strike)
        
        dataBase.close()

if __name__ == '__main__':
    Skew.openInterest()
