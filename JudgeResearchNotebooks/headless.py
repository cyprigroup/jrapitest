from historical_data import Coinalytix, HDParams
from judgeresearch import JudgeResearch, JRParams
import json
import plotly.graph_objects as go
import pandas as pd
from datetime import date, datetime, timedelta
import pandas_ta as ta
import time
from watchlist import colors

# set api keys
CA_API_KEY = "<paste your coinalytix.io key here>"
JR_API_KEY = "hHV1QUTclB653YLvFJBJh5Pz0BayF251at64c9x9"

# set delay for send and third feature submission
# 0.50 = 50% of time remaining until window close
FIRSTDELAY = 0.50
SECONDDELAY = 0.90

# set asset
asset = HDParams()
asset.exchange = "BINANCE"
asset.ticker = "BTC-USD-SPOT"
asset.set_start_date("2022-01-01 08:00:00")
asset.interval = "1d"
asset.num_periods = 365

df = None

# replace with your feature generation function
def feature_gen(df):
    ''' Set feature column to 1 or 0 as MACD crosses MACDs '''
    macddf = df.ta.macd(fast=8, slow=21, signal=9, min_periods=None, append=True)
    macddf["macdiff"] = macddf["MACD_8_21_9"] - macddf["MACDs_8_21_9"]
    macddf["feature"] = ['0' if x > 0 else '1' for x in macddf['macdiff']]
    return macddf

# set feature parameters
ft_params = JRParams()
ft_params.attribute = "2022-01-01T00:00:00Z" # default value
ft_params.dv = "BTC-USD"
ft_params.mbs= "240"
ft_params.feature_name = "testfeature001"
ft_params.value = "0"    # default value
ft_params.ipp = "last"    # default value

# wrapper functions
def fcs(asset, params):
    """ fetch, calculate, and submit once """
    HD = Coinalytix()
    HD.with_api_key(CA_API_KEY)
    hddf = HD.fetch_hd(asset)
    fdf = feature_gen(hddf)
    JR = JudgeResearch()
    JR.with_api_key(JR_API_KEY)
    features = JR.craft_features(params, fdf)
    payload = JR.format_payload(features)
    submit = JR.submit_feature(payload)
    return submit
    
def live_fcs(asset, params, firstdelay, seconddelay):
        """
        calculate and submit feature data 3 times, throttled by percentage
        of time remaining until end of widow
        
        first submission = immediate
        second submission = % of remaining time in window ex. .30 = 3 minutes of 10 remaining
        last submission = % of remaining time in window ex, .90 = 9 of 10 remaining
        """
        
        # determine current time
        now = datetime.now()
        print("Current time: " + now.strftime("%Y-%m-%dT%H:%M:%SZ"))
        
        # determine the upcoming deadline (end of window)
        # FIXME: don't assume windows are anchored to 00:00
        genesis_time = datetime.utcnow().today().replace(microsecond=0, second=0, minute=0, hour=0)
        
        # set deadline anchor time
        deadline = genesis_time
        print("Genesis: " + genesis_time.strftime("%Y-%m-%dT%H:%M:%SZ"))
        
        # create timedelta object based on MBS parameter
        window = timedelta(minutes=int(params.mbs))
        
        # iterate through block times until current time is passed, set deadline
        while now > deadline:
            deadline = deadline + window
            
        print("Next Block End: " + deadline.strftime("%Y-%m-%dT%H:%M:%SZ"))
        
        # calculate time remaining until window close
        remaining = deadline - now
        
        # caculate delays (seconds)
        delay1 = int(remaining.total_seconds() * firstdelay)
        delay2 = int(remaining.total_seconds() * seconddelay) - delay1
        
        # submit immediately
        s1 = fcs(asset, ft_params)
        print("First submission at " + datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
        print(s1)
        
        # sleep, recalculate, and send agin
        time.sleep(delay1)
        s2 = fcs(asset, ft_params)
        print("Second submission at " + datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))
        print(s2)
        
        # sleep, recalculate, and send final
        time.sleep(delay2)
        s3 = fcs(asset, ft_params)
        print("Final submission at " + datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"))        
        print(s3)

# send with delays
live_fcs(asset, ft_params, FIRSTDELAY, SECONDDELAY)