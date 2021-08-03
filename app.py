import codecs
import csv
import json

import numpy as np
from flask import Flask, jsonify
from tensorflow import keras
from operator import itemgetter
import os

port = int(os.environ.get('PORT', 5000))

app = Flask(__name__)

model_nn = keras.models.load_model('nn_cf/')
# model_svd = load('svd_nn.joblib')


@app.route('/rating/<user_id>/<item_id>', methods=["GET"])
def collaborative_filtering_nn(user_id, item_id):
    resp = 'please enter user id and movie id.'
    try:
        item_id = int(item_id)
        user_id = int(user_id)

        nn_resp = predict_nn(user_id, item_id)
        # svd_resp = predict_svd(user_id, item_id)
        resp = {'userId': user_id, 'itemId': item_id, 'nn': nn_resp}
    except ValueError:
        print('dude log the exceptions')
    return jsonify(resp)


@app.route('/landing', methods=["GET"])
def geo_items():
    geo_text = codecs.open('data/geo/geo.json', 'r', encoding='utf-8').read()
    resp = json.loads(geo_text)

    return jsonify(resp)


@app.route('/similar/<item_id>', methods=["GET"])
def similar_items(item_id):
    resp = 'please enter valid movie id and movie id.'
    data = get_json_data('data/cbf/cbf.json')
    if item_id in data:
        resp = data[item_id]
    return jsonify(resp)


@app.route('/forU/<user_id>')
def for_you(user_id):
    resp = 'please enter valid user id.'
    data = get_json_data('data/nn/nn.json')
    if user_id in data:
        resp = data[user_id]

    return jsonify(resp)


def get_json_data(json_path):
    cbf_text = codecs.open(json_path, 'r', encoding='utf-8').read()
    data = json.loads(cbf_text)
    return data


@app.route('/trainNN')
def cf():
    cache_nn()
    return "done"


def predict_nn(user_id, movie_id):
    pred = model_nn.predict([np.array([user_id]), np.array([movie_id])])
    return pred[0][0]


def convert_to_json(f_path):
    data = {}

    # Open a csv reader called DictReader
    with open(f_path, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        for rows in csvReader:
            # Assuming a column named 'No' to
            # be the primary key
            key = rows['No']
            data[key] = rows


def cache_nn():
    user_rating_predicted = {}
    movies = get_json_data('data/df/idx_movies_min.json')
    user_ids = get_json_data('data/df/idx_users.json')

    for user_id in user_ids:
        user_rate = []
        for m in movies:
            user_rate.append({'movie': m, 'rate': str(predict_nn(user_id, m))})
        user_rating_predicted[user_id] = sorted(user_rate, key=itemgetter('rate'), reverse=True)[:3]

    json.dump(user_rating_predicted, codecs.open('data/nn/nn.json', 'w', encoding='utf-8'), separators=(',', ':'),
              sort_keys=False, indent=4)


if __name__ == '__main__':
    app.run(debug=True)
