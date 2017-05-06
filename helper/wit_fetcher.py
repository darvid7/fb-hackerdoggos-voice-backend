from wit import Wit
import json

class WitFetcher:
    def __init__(self):
        with open('./../wit_server_config', 'r') as f:
            config = f.readlines()
        self.access_token = config[0].strip()
        self.wit_client = Wit(access_token=self.access_token)

    def debugAccessToken(self):
        print(self.access_token)

    def getResponse(self, query):
        res = self.wit_client.message(query)
        return res

if __name__ == "__main__":
    wt = WitFetcher()
    wt.debugAccessToken()
    res = wt.getResponse("When is David Lei's birthday?")
    print(res)
