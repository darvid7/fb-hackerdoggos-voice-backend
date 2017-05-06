from wit import Wit
import json

class WitFetcher:
    with open('./wit_server_config', 'r') as f:
        config = f.readlines()
    access_token = config[0].strip()
    wit_client = Wit(access_token=access_token)

    @staticmethod
    def debugAccessToken():
        print(WitFetcher.access_token)

    @staticmethod
    def getBirthdayResponse(query):
        raw = WitFetcher.wit_client.message(query)
        out = {}
        out['name'] = raw['entities']['person'][0]['value']
        return out

if __name__ == "__main__":
    WitFetcher.debugAccessToken()
    res = WitFetcher.getBirthdayResponse("When is David Lei's birthday?")
    print(res['name'])
