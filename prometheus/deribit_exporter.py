from prometheus_client.core import Summary, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server, Gauge
from prometheus_api_client import PrometheusConnect
import random
import json
import requests 
import datetime, time

class PrometheusClient:
    def __init__(self):
        # self.metrics = "http://18.217.47.37:9090/"
        self.metrics = "http://prometheus:9090/"
        self.g = Gauge("deribit_open_interest_compared_to_vault", 'Deribit Open Interest at Vault Strike Prices and Expiry', ['vault', 'instrument'])

    def rETH_THETA(self):
        r = requests.get('https://deribit.com/api/v2/public/get_instruments?currency=ETH&expired=false&kind=option')
        req = r.json()

        ## get current strike prices and expiry
        prom = PrometheusConnect(url=self.metrics, disable_ssl=True)
        eth_strike_price = prom.custom_query(query="query_vaultShortPositions_strikePrice{job='rETH-THETA'} / 100000000")
        eth_strike_price = round(float(eth_strike_price[0]["value"][1]))
        eth_exp = prom.custom_query(query="query_vaultShortPositions_expiry{job='rETH-THETA'} * 1000")
        eth_exp = float(eth_exp[0]["value"][1])

        ## filter by strike and expiry
        a = list(filter(lambda x: x["expiration_timestamp"] == eth_exp and x["option_type"] == "call" and x["strike"] == eth_strike_price, req["result"]))
        
        o = a[0]
        name = o["instrument_name"]
        r = requests.get("https://deribit.com/api/v2/public/get_book_summary_by_instrument?instrument_name=" + name)
        req = r.json()      
        oi = req["result"][0]["open_interest"]
        self.g.labels(vault='rETH-THETA', instrument=name).set(oi)

    def rBTC_THETA(self):
        r = requests.get('https://deribit.com/api/v2/public/get_instruments?currency=BTC&expired=false&kind=option')
        req = r.json()

        ## get current strike prices and expiry
        prom = PrometheusConnect(url=self.metrics, disable_ssl=True)
        btc_strike_price = prom.custom_query(query="query_vaultShortPositions_strikePrice{job='rBTC-THETA'} / 100000000")
        btc_strike_price = round(float(btc_strike_price[0]["value"][1]))
        btc_exp = prom.custom_query(query="query_vaultShortPositions_expiry{job='rBTC-THETA'} * 1000")
        btc_exp = float(btc_exp[0]["value"][1])

        ## filter by strike and expiry
        a = list(filter(lambda x: x["expiration_timestamp"] == btc_exp and x["option_type"] == "call" and x["strike"] == btc_strike_price, req["result"]))
        
        o = a[0]
        name = o["instrument_name"]
        r = requests.get("https://deribit.com/api/v2/public/get_book_summary_by_instrument?instrument_name=" + name)
        req = r.json()      
        oi = req["result"][0]["open_interest"]
        self.g.labels(vault='rBTC-THETA', instrument=name).set(oi)

    def rUSDC_ETH_P_THETA(self):
        r = requests.get('https://deribit.com/api/v2/public/get_instruments?currency=ETH&expired=false&kind=option')
        req = r.json()

        ## get current strike prices and expiry
        prom = PrometheusConnect(url=self.metrics, disable_ssl=True)
        eth_strike_price = prom.custom_query(query="query_vaultShortPositions_strikePrice{job='rUSDC-ETH-P-THETA'} / 100000000")
        eth_strike_price = round(float(eth_strike_price[0]["value"][1]))
        eth_exp = prom.custom_query(query="query_vaultShortPositions_expiry{job='rUSDC-ETH-P-THETA'} * 1000")
        eth_exp = float(eth_exp[0]["value"][1])

        ## filter by strike and expiry
        a = list(filter(lambda x: x["expiration_timestamp"] == eth_exp and x["option_type"] == "call" and x["strike"] == eth_strike_price, req["result"]))
        o = a[0]
        name = o["instrument_name"]
        r = requests.get("https://deribit.com/api/v2/public/get_book_summary_by_instrument?instrument_name=" + name)
        req = r.json()      
        oi = req["result"][0]["open_interest"]
        self.g.labels(vault='rUSDC-ETH-P-THETA', instrument=name).set(oi)
           
if __name__ == '__main__':
    start_http_server(9000)
    p = PrometheusClient()
    while True:
        p.rETH_THETA()
        p.rBTC_THETA()
        p.rUSDC_ETH_P_THETA()