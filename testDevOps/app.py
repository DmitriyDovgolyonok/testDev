from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)


def get_db():
    client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource="admin")
    db = client["animal_db"]
    return db


@app.route('/')
def ping_server():
    return "Welcome to the world of animals."


@app.route('/get_all', methods=['GET'])
def get_all():
    data = request.get_json()
    db = get_db()
    _animals = db.animal_tb.find()
    animals = [{"key": animal["key"], "value": animal["value"]} for animal in _animals]
    return jsonify({"all_values": animals})


@app.route('/get', methods=['GET'])
def get_by_key():
    data = request.get_json()
    if 'key' in data:
        key = data['key']
        db = get_db()
        collection = db.animal_tb
        animal = collection.find_one({"key": key})
        if animal:
            return jsonify({"key": animal["key"], "value": animal["value"]})
        else:
            return jsonify({"message": "Key not found."}), 404
    else:
        return jsonify({"message": "Missing key in request."}), 400


@app.route('/post', methods=['POST'])
def post_value():
    data = request.get_json()
    if 'key' in data and 'value' in data:
        key = data['key']
        value = data['value']
        db = get_db()
        collection = db.animal_tb
        existing_animal = collection.find_one({"key": key})
        if existing_animal:
            return jsonify({"message": "Value with key " + key + " already exists."})
        else:
            new_animal = {"key": key, "value": value}
            result = collection.insert_one(new_animal)
            return jsonify({"message": "Added with ID: " + str(result.inserted_id)})
    else:
        return jsonify({"message": "Missing key or value in request."}), 400


@app.route('/update', methods=['PUT'])
def update_value():
    data = request.get_json()
    if 'key' in data and 'value' in data:
        key = data['key']
        new_value = data['value']
        db = get_db()
        collection = db.animal_tb
        result = collection.update_one({"key": key}, {"$set": {"value": new_value}})

        if result.modified_count == 1:
            return jsonify({"message": "Updated value for key: " + key})
        else:
            return jsonify({"message": "Key not found."}), 404
    else:
        return jsonify({"message": "Missing key or value in request."}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
