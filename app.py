from flask import Flask
from flask import jsonify
from flask import abort
from flask import request
import requests
import json
import facebook



app = Flask(__name__)

queries = [
    {
        'text': 'Hi how is x',
        'id': 1
    },
    {
        'text': 'Potato',
        'id': 2
    },
    {
        'text': 'Facebook',
        'id': 1
    }
]

@app.route('/')
def home():



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

    graph = facebook.GraphAPI(access_token=access_token, version='2.9')
    fb_res = graph.get_permissions("375019402658742")
    print(fb_res)

@app.route('/hackerdoggos/api/v1/queries', methods=['GET'])
def get_queries():
    return jsonify({'queries': queries})


"""
Pass parameter by specifying type:name, pass into function handling route.
"""
@app.route('/hackaerdoggos/api/v1/query/<int:query_id>', methods=['GET'])
def get_specific_query(query_id):
    print(query_id)
    matching_queries = [q for q in queries if q['id'] == query_id]
    if len(matching_queries) == 0:
        abort(404)
    return jsonify({'queries': matching_queries})



if __name__ == '__main__':
    app.run(debug=True)

