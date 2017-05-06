from config_parser import ConfigParser
from friend_parser import FriendParser
import facebook
import requests
import collections
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

    def __init__(self, path):
        self.config = {}
        ConfigParser.load_config(path, self.config)
        self.application_access_token = None
        self._authenticate_app()
        self.graph = facebook.GraphAPI(access_token=self.application_access_token)
        self.user_graph_query_map = collections.defaultdict(dict)

        # self.authenticated_user_graph = facebook.GraphAPI(access_token=self.config['user_refreshable_token'])
        # self.authenticated_user_id = self.authenticated_user_graph.get_object(id='me', fields='id')['id']
        #  print('id: ' + self.authenticated_user_id)

        # fp = FriendParser()
        # fp.load_friends('../fb_friend_graph_subset')
        # self.friends = fp.friends
        # print('friends: ' + str(len(self.friends)))

    def add_user(self, user_token):
        if user_token in self.user_graph_query_map:
            pass
        else:
            self.user_graph_query_map[user_token] = {'graph': facebook.GraphAPI(access_token=user_token)}
            user_data = self.user_graph_query_map[user_token]['graph'].get_object(id='me', fields='id, name')
            self.user_graph_query_map[user_token]['id'] = user_data['id']
            print('FB Graph >> set id: %s, for user: %s' % (user_data['id'], user_data['name']))


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

    def parse_friend(self, user_token, friend_full_name):
        names = friend_full_name.split(' ')
        if len(names) > 1 and [x for x in names if x != '']: # Has at least 2 in names (first name, last name)
            first_name, last_name = names[0], names[1]
        else:
            first_name = names[0]
            last_name = False

        # Check friend is in friend dict.
        if 'friends' not in self.user_graph_query_map[user_token]:
            self.get_all_registered_friends(user_token)

        # Get friend.
        friend_mappings = self.user_graph_query_map[user_token]['friends']
        try:
            if not last_name:
                friend = friend_mappings[first_name]
                print('Only first name: ' + str(friend))
                if len(friend) > 1:
                    raise KeyError('More than 1 friend with name %s, specify last name' % first_name)
                if len(friend) < 1:
                    raise KeyError('No friends found with name %s' % first_name)
                else:
                    friend_id = list(friend.values())[0]
            else:
                friend_id = friend_mappings[first_name][last_name]
            return friend_id
        except KeyError:
            return False

    def get_all_registered_friends(self, user_token):
        user_graph = self.user_graph_query_map[user_token]['graph']
        response = user_graph.get_object(id='me/friends', fields='id,name')
        friends = response['data']
        friend_dict = collections.defaultdict(dict)
        for friend_json_data in friends:
            name = friend_json_data['name']
            names = name.split(' ')
            first_name, last_name = names[0], names[1]
            id = friend_json_data['id']
            friend_dict[first_name][last_name] = id
        print('Friends: ' + str(friend_dict))
        self.user_graph_query_map[user_token]['friends'] = friend_dict

    def get_feed(self, user_token, friend_full_name):
        if user_token not in self.user_graph_query_map:
            self.add_user(user_token)
        friend_id = self.parse_friend(user_token, friend_full_name)
        if not friend_id:
            return False
        query = '%s/feed' % friend_id
        print('Feed query: ' + query)
        wall_feed = self.user_graph_query_map[user_token]['graph'].get_object(id=query, fields='story,id,permalink_url,created_time,message')
        print(wall_feed)
        return wall_feed

    def get_birthday(self, user_token, friend_full_name):
        if user_token not in self.user_graph_query_map:
            self.add_user(user_token)

        if friend_full_name.lower() in ['my', 'me', 'i', 'myself']:
            birthday = self.user_graph_query_map[user_token]['graph'].get_object(id=self.user_graph_query_map[user_token]['id'], fields='birthday')
            print('query: my birthday ' + str(birthday))
            return birthday

        friend_id = self.parse_friend(user_token, friend_full_name)
        if not friend_id:
            return False
        birthday = self.user_graph_query_map[user_token]['graph'].get_object(id=friend_id, fields='birthday')
        print('%s birthday: %s' % (friend_full_name, birthday))
        return birthday

    def get_likes(self, user_token, friend_full_name):
        if user_token not in self.user_graph_query_map:
            self.add_user(user_token)

        if friend_full_name.lower() in ['my', 'me', 'i', 'myself']:
            query = '%s/likes' % self.user_graph_query_map[user_token]['id']
            print('Likes query: ' + str(query))
            likes = self.user_graph_query_map[user_token]['graph'].get_object(id=query, fields='about,overall_star_rating,fan_count,rating_count,link,name,picture{url}')
            print('All likes: ' + str(likes))
            return likes

        friend_id = self.parse_friend(user_token, friend_full_name)
        if not friend_id:
            return False

        query = '%s/likes' % friend_id
        print('Like query for friend: ' + query)
        likes = self.user_graph_query_map[user_token]['graph'].get_object(id=query, fields='about,overall_star_rating,fan_count,rating_count,link,name,picture{url}')
        print('All likes: ' + str(likes))
        likes_data = likes['data']
       #  return likes

    def get_events(self, user_token):
        if user_token not in self.user_graph_query_map:
            self.add_user(user_token)
        event_ids = [
            '1837139043276401',
            '214948752319763',
            '1252150611568955',
            '1325364077532723',
            '1548708398495787'
        ]
        events = []
        for event_id in event_ids:
            events.append(self.user_graph_query_map[user_token]['graph'].get_object(id=event_id))
        # print(events)
        return events

# David temp id: 749012631926082

# 218613405205017?fields=about,link,bio,checkins,general_info,name,overall_star_rating

# Object id/edge
if __name__ == '__main__':
    # Testing.
    fb = FacebookGraphHelper('../fb_app_config')
    # l = fb.graph.get_object(id='218613405205017')
    # print(l)
    fb.add_user('EAADxJ5QX8c0BAIZCHiKzTsDj1BAebA4mZANH7QYZAZBnVKOsnJZCotEn7VSsjfCFSbvWKF8cRiUdARTofeqLeQoRZAMpy0JAxbaO7cUrmrHHvVfv7ArYdD14vXHOYOknN9TMeNYZCBnDLvOGTCIuV3ZBGUtZBkTNeB1wZD')
    fb.get_all_registered_friends('EAADxJ5QX8c0BAIZCHiKzTsDj1BAebA4mZANH7QYZAZBnVKOsnJZCotEn7VSsjfCFSbvWKF8cRiUdARTofeqLeQoRZAMpy0JAxbaO7cUrmrHHvVfv7ArYdD14vXHOYOknN9TMeNYZCBnDLvOGTCIuV3ZBGUtZBkTNeB1wZD')
    fb.get_birthday('EAADxJ5QX8c0BAIZCHiKzTsDj1BAebA4mZANH7QYZAZBnVKOsnJZCotEn7VSsjfCFSbvWKF8cRiUdARTofeqLeQoRZAMpy0JAxbaO7cUrmrHHvVfv7ArYdD14vXHOYOknN9TMeNYZCBnDLvOGTCIuV3ZBGUtZBkTNeB1wZD',
                    'David Lei')
    fb.get_likes('EAADxJ5QX8c0BAJj0xKG9vP1u0VFXpWeHzaqXuLTZCE9YbKJtPZBvKcbvUfQth9UraL7hrTJpKvT0MPl6WfJ0pVAM7ovkbkWZCtYxDxeITBsnsL8sE5fXyCdduVgusksJbTtyfaBEXCEZADGkA7uvo5kDQZCHE5dci9j5Qli54HtbDE2AO37fCaF0y2x362YUZD',
                 'Joanna')


    # fb.get_birthday('Joanna', 'Lee')

    # fb.get_birthday()
    # fb.get_feed()
    # fb.get_friends()

    # friends = fb.get_friends()
    # fb.get_all_friends()
    # print(friends)
    # for f in friends:
    #     print(f)
    # print('here--')
    # x = fb.authenticated_user_graph.get_object(id='10153036881648177/feed')
    # print(x)
