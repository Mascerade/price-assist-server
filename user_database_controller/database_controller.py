from flask import Flask, request
import json
import flask
from flask_cors import cross_origin
import requests
import sys
import os
import plyvel

# Create the databases directory first
if not os.path.exists('databases'):
    os.makedirs('databases')

USER_DB = 'databases/user_db'

ply_db = plyvel.DB(USER_DB, create_if_missing = True)


app = Flask(__name__)

@app.route('/', methods=['POST'])
def add_user():
    uid_token = request.json['uid_token']
    ply_db.put(bytes(uid_token, encoding='utf-8'), bytes(json.dumps({'item_models': []}), encoding='utf-8'))
    return json.dumps({'success': True, 'msg': 'User Created'}), 201

@app.route('/', methods=['PUT'])
def update_item_models():
    uid_token = request.json['uid_token']
    item_model = request.json['item_model']
    item_models = json.loads(ply_db.get(bytes(uid_token, encoding='utf-8')).decode('utf-8'))
    item_models['item_models'].append(item_model)
    print(item_models)
    ply_db.put(bytes(uid_token, encoding='utf-8'), bytes(json.dumps(item_models), encoding='utf-8'))
    return json.dumps({'success': True, 'msg': 'Updated Item Models'}), 204

@app.route('/', methods=['GET'])
def get_user():
    uid_token = request.args.get('uid_token')
    item_models = json.loads(ply_db.get(bytes(uid_token, encoding='utf-8')).decode('utf-8'))
    item_models['success'] = True
    return json.dumps(item_models), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, threaded=True)
