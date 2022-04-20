from datetime import datetime


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
        self.url_root = ""
        self.api_key = ""

    def with_api_key(self, key):
        self.api_key = key

    def fmt_time(self, timestamp):
        """format time per API doc"""
        return datetime.strftime("%Y-%m-%dT%H:%M:%SZ")

    def format_payload(featuredata):
        pass

    def submit_feature(payload):
        pass
