from flask import Flask, jsonify, abort, request
from config_parser import ConfigParser
from flask_cors import CORS
# import helper
from helper.wit_fetcher import WitFetcher
from helper.facebook_graph_helper import FacebookGraphHelper

fb_graph = FacebookGraphHelper('fb_app_config')
app = Flask(__name__)
CORS(app)



fb_config = {}
wit_config = {}


def config_set_up():
    ConfigParser.load_config('fb_app_config', fb_config)
    ConfigParser.load_config('wit_server_config', wit_config)


queries = [
    {
        'text': 'Something',
        'id': 1
    }
]

@app.route('/')
def home():
    return "Hello World"

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

# @app.route('/hackerdoggos/api/v1/query', methods=['POST'])
# def post_query():
#     return request

@app.route('/hackerdoggos/api/v1/query', methods=['POST'])
def create_query():
    print('Posted')
    if not request.json or not 'text' in request.json or request.json['text']=='':
        print('About to Abort')
        abort(400)
    print('About to query wit')
    wt = WitFetcher()
    text = request.json['text']
    print("Given text is : " + str(text))
    user_token = request.json['token']
    intent_res = wt.getResponse(text)
    print('Wit response: ' + str(intent_res))
    if intent_res == 'no matches':
        error = 'Query %s was not understood' % text
        return jsonify({'error': error}), 404
    # ------------------------------
    # FB GRAPH QUERY IN HERE.
    print('FB Graph Query')
    intent_type = intent_res['type']
    if 'person' in intent_res:
        person = intent_res['person']
        if person == 'unknown':
            error = 'Person is unknown'
            return jsonify({'error': error}), 404

    print('______')
    print(intent_res)
    # TODO: Return names.
    print(intent_type)
    if intent_type == 'get_recent_posts':
        feed = fb_graph.get_feed(user_token, person)
        if not feed:
            error = '%s not found in friends' % person
            return jsonify({'error': error}), 404
        return jsonify({'feed': feed, 'intent': intent_res}), 201

    elif intent_type == 'get_birthday':
        birthday = fb_graph.get_birthday(user_token, person)
        if not birthday:
            error = '%s not found in friends' % person
            return jsonify({'error': error}), 404
        return jsonify({'birthday': birthday, 'intent': intent_res}), 201

    elif intent_type == 'get_friend_online_status':
        return jsonify({'todo': 'this', 'intent': intent_res}), 201

    elif intent_type == 'get_nearby_events':
        events = fb_graph.get_events(user_token)
        return jsonify({'events': events, 'intent': intent_res}), 201

    elif intent_type == 'post_love_emojis':
        return jsonify({'todo': 'this', 'intent': intent_res}), 201

    # print(intent_res)

    # ------------------------------
    # response = jsonify({'query': query, 'intent': intent_res})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    # return response, 201

if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("1337")
    )

# http://0.0.0.0:1337/hackerdoggos/api/v1/query
