# import classes that handle API connections and parameters
from historical_data import Coinalytix, HDParams
from judgeresearch import JudgeResearch, JRParams

# import classes for data handling & visiualization
import json
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import pandas_ta as ta
from watchlist import colors

CA_API_KEY = "<paste your coinalytix.io key here>"
JR_API_KEY = "hHV1QUTclB653YLvFJBJh5Pz0BayF251at64c9x9"

asset = HDParams()
asset.exchange = "BINANCE"
asset.ticker = "BTC-USD-SPOT"
asset.set_start_date("2022-01-01 08:00:00")
asset.interval = "1d"
asset.num_periods = 365

HD = Coinalytix()
HD.with_api_key(CA_API_KEY)
asset_data = HD.fetch_hd(asset)
hddf = pd.DataFrame.from_dict(asset_data)
hddf.set_index(pd.DatetimeIndex(hddf["StartDate"]*1000000000), inplace=True)

###
###  Paste you feature generation code here
###

# The feature_gen function accepts a pandas dataframe, datetime indexed and should return a pandas dataframe, similarly
# datetime index and including a column named "feature"

macddf = hddf.ta.macd(fast=8, slow=21, signal=9, min_periods=None, append=True)

def feature_gen(df):
    ''' Set feature column to 1 or 0 as MACD crosses MACDs '''
    df["macdiff"] = df["MACD_8_21_9"] - df["MACDs_8_21_9"]
    df["feature"] = ['0' if x > 0 else '1' for x in df['macdiff']]
    return df


###
###
###


JRATTRIBUTE = "2022-01-01T00:00:00Z" # default value
JRDV = "ETH-USD"
JRMBS= "240"
JRFEATURE_NAME = "testfeature001"
JRVALUE = "0"    # default value
JRIPP = "last"    # default value

JR = JudgeResearch()
JR.with_api_key(JR_API_KEY)
fdf = feature_gen(macddf)

def craft_features(df):
    _features = []
    for index, row in df.iterrows():
        _jrparams = JRParams()
        _jrparams.attribute = index.strftime('%Y-%m-%dT%H:%M:%SZ')
        _jrparams.dv = JRDV
        _jrparams.mbs = JRMBS
        _jrparams.feature_name = JRFEATURE_NAME
        _jrparams.value = row["feature"]
        _jrparams.ipp = JRIPP
        _features.append(_jrparams)
    return _features
features = craft_features(fdf)
# Craft payload
payload = JR.format_payload(features)

s = JR.submit_feature(payload)
print(s)
