import collections

class FriendParser:
    def __init__(self):
        self.friends = collections.defaultdict(dict)

    def load_friends(self, path):
        sub_dict = {}
        with open(path, 'r') as f:
            for line in f:
                if '{' in line or '}' in line or line == '\n':
                    continue
                key, value = line.split(':')
                key = key.lstrip().rstrip().strip(',\"')
                value = value.lstrip().rstrip().strip(',\"')
                sub_dict[key] = value
                if key == 'feed':
                    full_name = sub_dict['name']
                    names = full_name.split(' ')
                    first_name, last_name = names[0], names[-1]
                    self.friends[first_name][last_name] = sub_dict
                    sub_dict = {}

if __name__ == '__main__':
    fp = FriendParser()
    fp.load_friends('./fb_friend_graph_subset')