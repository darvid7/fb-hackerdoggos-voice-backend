from wit import Wit
import json

class WitFetcher:
    def __init__(self):
        config = None
        try:
            with open('./wit_server_config', 'r') as f:
                config = f.readlines()
        except:
            # running locally
            with open('./../wit_server_config', 'r') as f:
                config = f.readlines()

        self.access_token = config[0].strip()
        self.wit_client = Wit(access_token=self.access_token)

    def debugAccessToken(self):
        print(self.access_token)

    def parseBirthdayResponse(self, res):
        # return res
        out = {}
        out['type'] = 'get_birthday'
        out['person'] = self.getPerson(res)
        return out

    def parseCheckFriendResponse(self, res):
        out = {}
        out['type'] = 'get_recent_posts'
        out['person'] = self.getPerson(res)
        return out
        # return res

    def parseCheckFriendOnlineStatusResponse(self, res):
        out = {}
        out['type'] = 'get_friend_online_status'
        out['person'] = self.getPerson(res)
        return out

    def parseCheckEventsResponse(self, res):
        out = {}
        out['type'] = 'get_nearby_events'
        return out

    def parseSendLovesResponse(self, res):
        out = {}
        out['type'] = 'post_love_emojis'
        out['person'] = self.getPerson(res)
        return out

    def parseGetLikesResponse(self, res):
        out = {}
        out['type'] = 'get_likes'
        out['person'] = self.getPerson(res)
        return out

    def getPerson(self, res):
        person = None
        try:
            person = res['person'][0]['value']
        except KeyError:
            person = 'unknown'
        return person

    def getResponse(self, query):
        res = self.wit_client.message(query)['entities']
        keys = []
        intent = None
        for key in res:
            if "Intent" in key:
                intent = key
        if intent == 'IntentGetBirthDate' or intent == 'IntentGetBirthday':
            return self.parseBirthdayResponse(res)
        elif intent == 'IntentCheckFriend':
            return self.parseCheckFriendResponse(res)
        elif intent == 'IntentCheckFriendOnlineStatus':
            return self.parseCheckFriendOnlineStatusResponse(res)
        elif intent == 'IntentCheckEvents':
            return self.parseCheckEventsResponse(res)
        elif intent == 'IntentSendLoves':
            return self.parseSendLovesResponse(res)
        elif intent == 'IntentGetLikes':
            return self.parseGetLikesResponse(res)
        else:
            return 'no matches'

if __name__ == "__main__":
    wt = WitFetcher()
    wt.debugAccessToken()
    res = wt.getResponse("When is David Lei's birthday?")
    print(res)
    res = wt.getResponse("What is Cal up to?")
    print(res)
