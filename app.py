from flask import Flask, jsonify, abort, request
import helper

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
        'id': 3
    }
]

@app.route('/')
def home():
    return 'Hi'

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
def create_task():
    if not request.json or not 'text' in request.json:
        abort(400)
    query = {
        'id': queries[-1]['id'] + 1,
        'text': request.json['text']
    }
    queries.append(query)
    return jsonify({'task': query}), 201

if __name__ == '__main__':
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int("23232")
    )
