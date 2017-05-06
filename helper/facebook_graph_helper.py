from config_parser import ConfigParser
from friend_parser import FriendParser
import facebook
import requests
import json

name_maps = {
    'jo': 'joanna',
    'joanna': 'joanna',
    'arv': 'arvin',
    'lee': 'lee',
    'callis': 'Callistus',
    'Callistus': 'Callistus',
    'cal': 'Callistus',
    'Tan': 'Tan',
}

class FacebookGraphHelper:

    def __init__(self):
        self.config = {}
        ConfigParser.load_config('../fb_app_config', self.config)
        self.application_access_token = None
        self._authenticate_app()
        # self.graph = facebook.GraphAPI(access_token=self.application_access_token)
        self.graph_map = {}

        # self.authenticated_user_graph = facebook.GraphAPI(access_token=self.config['user_refreshable_token'])
        # self.authenticated_user_id = self.authenticated_user_graph.get_object(id='me', fields='id')['id']
        #  print('id: ' + self.authenticated_user_id)

        # fp = FriendParser()
        # fp.load_friends('../fb_friend_graph_subset')
        # self.friends = fp.friends
        # print('friends: ' + str(len(self.friends)))

    def add_user(self, user_token):
        if user_token in self.graph_map:
            pass
        else:
            self.graph_map[user_token] = facebook.GraphAPI(access_token=user_token)

    # def parse_name(self, accepted_name):
    #     names = accepted_name.split(' ')
    #     if len(names) > 1 and [x for x in names if x != '']:
    #         first_name, last_name = names
    #     else:
    #         first_name = names[0]
    #
    #     for name in self.friends.keys:
    #         if first_name in name:
    #             pass

    def _authenticate_app(self):
        response = requests.get('https://graph.facebook.com/oauth/access_token?'
                                'client_id=%s'
                                '&client_secret=%s'
                                '&grant_type=client_credentials'
                                % (self.config['client_id'], self.config['client_secret']))
        parsed_response = bytes.decode(response.content)
        auth_data = json.loads(parsed_response)
        self.application_access_token = auth_data['access_token']

    # Returns generator of 15 friends
    # def get_friends(self):
    #     friends = self.authenticated_user_graph.get_all_connections(id='me/friends', connection_name='')
    #     return friends

    def get_all_friends(self, user_token):
        friends = self.authenticated_user_graph.get_object(id='me/friends', limit=50, fields='id,name')

        print(friends)

    def get_feed(self): # , friend_first_name, friend_last_name):
        # id = self.friends[friend_first_name][friend_last_name]['id']
        query = '%s/feed' % id
        wall_feed = self.authenticated_user_graph.get_object(id='749012631926082/feed')
        print(wall_feed)
        return wall_feed

    def get_birthday(self): # , friend_first_name, friend_last_name):
        # id = self.friends[friend_first_name][friend_last_name]['id']
        birthday = self.authenticated_user_graph.get_object(id='749012631926082', fields='birthday')
        print(birthday)

    def get_friends(self):
        friends = self.authenticated_user_graph.get_object(id='me/friends' )
        return friends

    def test(self):
        x = self.graph.get_object(id='749012631926082', fields='birthday')
        print(x)
        y = self.graph.get_object(id='749012631926082/feed')
        print(y)

# David temp id: 749012631926082

# Object id/edge
if __name__ == '__main__':
    fb = FacebookGraphHelper()
    # fb.get_birthday('Joanna', 'Lee')
    fb.test()
    print('--')
    fb.get_birthday()
    fb.get_feed()
    fb.get_friends()
    # friends = fb.get_friends()
    # fb.get_all_friends()
    # print(friends)
    # for f in friends:
    #     print(f)
    # print('here--')
    # x = fb.authenticated_user_graph.get_object(id='10153036881648177/feed')
    # print(x)
