from datetime import datetime


import requests

class JRParams:
    """
    Collect feature information
    """

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
    """
    Conduit to JudgeResearch API
    """

    def __init__(self):
        self.url = "https://ct6gu86m3d.execute-api.us-east-2.amazonaws.com/dev"
        self.api_key = ""

    def with_api_key(self, key):
        self.api_key = key
        self.headers = {"x-api-key": key}

    def fmt_time(self, timestamp):
        """format time per API doc"""
        return datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    def format_payload(self, features):
        """Accepts list of jrparam objects and generates JSON payload"""
        _data = []
        for feature in features:
            _payload = {
                "attribute": feature.attribute,
                "DV": feature.dv,
                "MBS": feature.mbs,
                "featureName": feature.feature_name,
                "value": feature.value,
                "IPP": feature.ipp,
            }
            _data.append(_payload)
        data = {"data": _data}
        return data

    def submit_feature(self, data):
        featureupdate = requests.put(self.url, headers=self.headers, json=data)
        return featureupdate
