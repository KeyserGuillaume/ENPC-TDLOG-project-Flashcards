#!flask/bin/python
from flask import Flask, jsonify, make_response
from flask_cors import CORS

import database

app = Flask(__name__)
CORS(app, resources={r"/flashcards/*": {"origins": "*"}})

@app.errorhandler(500)
def error_message(message):
    return make_response(jsonify({'error': message}), 500)

@app.route('/flashcards/<table_name>', methods=['GET'])
def get_all_cards(table_name):
    try:
        cards = database.getAllCards(table_name)
    except:
        return error_message('{} not found'.format(table_name))
    return jsonify({'cards': cards})

if __name__ == '__main__':
    app.run(debug=True)
