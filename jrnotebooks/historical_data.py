import json
from datetime import datetime

import requests


class HDParams:
    '''
    Collect asset information
    '''
    def __init__(
        self,
        exchange="BINANCE",
        ticker="BTC-USD-SPOT",
        start_date="2022-01-01 08:00:00",
        interval="1d",
        num_periods="365",
    ):

        self.exchange = exchange
        self.ticker = ticker
        self.start_date = datetime.fromisoformat(start_date)
        self.interval = interval
        self.num_periods = num_periods

    def set_start_date(self, datestr):
        self.start_date = datetime.fromisoformat(datestr)

class JRParams:
    '''
    Collect feature information
    '''
    def __init__(
        self,
        dv="ETH-USD",
        mbs=240,
        feature_name="default",
        value="",
        ipp="last",
    ):

        self.dv = dv
        self.mbs = mbs
        self.feature_name = feature_name
        self.value = value
        self.ipp = ipp

#    def set_start_date(self, datestr):
#        self.start_date = datetime.fromisoformat(datestr)

class JudgeResearch:
    '''
    Conduit to JudgeResearch API
    '''
    def __init__(self):
        self.url_root = ""
        self.api_key = ""
        
    def with_api_key(self, key):
        self.api_key = key 
        
    def fmt_time(self, timestamp):
        ''' format time per API doc '''
        return datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    def send_feature(self, jrparams, data):
        '''
        Send feature data point given a JRParams object and a tuple or list of tuples containing startdate & value
        '''
        
        _url = (
            self.url_root
            + "api_key="
            + self.api_key
            + "&exchange="
            + asset.exchange
            + "&ticker="
            + asset.ticker
            + "&startDate="
            + str(int(asset.start_date.timestamp() * 1000))
            + "&interval="
            + asset.interval
            + "&numPeriods="
            + str(asset.num_periods)
        )

        r = requests.get(_url)
        if r.status_code == 200:
            _json = r.json()
            data = _json["data"]
            return data
        else:
            print("Error fetching data")
            return r.text
        
    
class Coinalytix:
    """
    Conduit to Coinalytix API
    """

    def __init__(self):
        self.url_root = "https://timeseries.coinalytix.io/getohlcdata?"
        self.api_key = ""

    def with_api_key(self, key):
        self.api_key = key

    def fetch_hd(self, asset):
        _url = (
            self.url_root
            + "api_key="
            + self.api_key
            + "&exchange="
            + asset.exchange
            + "&ticker="
            + asset.ticker
            + "&startDate="
            + str(int(asset.start_date.timestamp() * 1000))
            + "&interval="
            + asset.interval
            + "&numPeriods="
            + str(asset.num_periods)
        )

        r = requests.get(_url)
        if r.status_code == 200:
            _json = r.json()
            data = _json["data"]
            return data
        else:
            print("Error fetching data")
            return r.text

