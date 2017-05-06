import facebook
import requests
import json
from flask import request

response = requests.get('https://graph.facebook.com/oauth/access_token?'
                                   'client_id=428403904204305'
                                   '&client_secret=cfd7f9867bdeacd1805360844567c58f'
                                   '&grant_type=client_credentials')
result = bytes.decode(response.content)
auth_data = json.loads(result)
print(auth_data)
app_id, access_token = auth_data['access_token'].split('|')
print(app_id)
print(access_token)
# print(fb_oauth_request.cookies)
# print(fb_oauth_request.raw)
# print(fb_oauth_request.content)
# fb_app_access_token = repr(fb_oauth_request.content)
#
# print(str(fb_app_access_token))
# data = bytes.decode(fb_oauth_request.content)

graph = facebook.GraphAPI(access_token='EAACEdEose0cBANshh9O7lmyDtZAYgeCOPF4tZA9cUtvvIi4Mwoi6ruf18Ke5bfcXlq67SEbttJq36jMhNmZBg7ekPmLP0Xn0V1k6LRImL80iIYhLlqAJi9I23d17tRZBoIj9ggdZBVXP9KS3D9Fquqtk1hIVlTeZBm8l4ajpU1ZCgQdE4UZAumHj9ZAIZCbVU32VcvamdCUDusWQZDZD', version='2.9')
print(graph)
print(graph.access_token)


app_id = 428403904204305
canvas_url = 'https://domain.com/that-handles-auth-response/'
perms = ['manage_pages','publish_pages']
fb_login_url = facebook.auth_url(app_id, canvas_url, perms)
print(fb_login_url)


fb_res = graph.put_comment(object_id='101701333739049_101702540405595', message='Great post...')

# graph.put_like(object_id='101701333739049_101702540405595')
friends = graph.get_connections(id='me', connection_name='friends')
print('friends: ' + str(friends))
# user_login = facebook.auth_url()
print(fb_res)
# graph.put_object(parent_object='me', connection_name='feed',
#                   message='Hello, world')


graph.put_object(
   parent_object="me",
   connection_name="feed",
   message="This is a great website. Everyone should visit it.",
   link="https://www.facebook.com")
print("DONE")

test = graph.get_object('375019402658742')
print(test)

test_feed = graph.get_object(id='375019402658742', fields='feed')
print('TEST FEED')
print(test_feed)
print("TESTFEED")
feed = graph.get_all_connections(id='375019402658742', connection_name='feed')
for f in feed:
    print(f)
# friends = graph.get_connections(id='me', connection_name='friends')
# #
# "610481219112558"  "id": "375019402658742",
