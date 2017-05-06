from flask import Flask
from flask import jsonify
from flask import abort

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
    return 'HI'

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
