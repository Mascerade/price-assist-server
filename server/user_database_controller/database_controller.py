from flask import Flask, request
import json
import flask
from flask_cors import cross_origin
import requests
import sys
import os
import plyvel
import firebase_admin
from firebase_admin import auth

# Initialize the firebase app
default_app = firebase_admin.initialize_app()

# Create the databases directory first
if not os.path.exists('databases'):
    os.makedirs('databases')

USER_DB = 'databases/user_db'

ply_db = plyvel.DB(USER_DB, create_if_missing = True)

app = Flask(__name__)

def process_token(token):
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token['uid']
    return uid

@app.route('/test', methods=['GET'])
@cross_origin()
def test():
    token = request.args.get('uid_token')
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token['uid']
    print(uid)
    return json.dumps({'success': True}), 200

@app.route('/', methods=['POST'])
@cross_origin()
def add_user():
    uid_token = process_token(request.json['uid_token'])
    ply_db.put(bytes(uid_token, encoding='utf-8'), bytes(json.dumps({'item_models': []}), encoding='utf-8'))
    return json.dumps({'success': True, 'msg': 'User Created'}), 201

@app.route('/', methods=['PUT'])
@cross_origin()
def update_item_models():
    uid_token = process_token(request.json['uid_token'])
    item_model = request.json['item_model'].lower().strip()
    item_models = ply_db.get(bytes(uid_token, encoding='utf-8'))
    if item_models is None:
        return json.dumps({'success': False, 'msg': 'User does not exists'}), 404
    item_models = json.loads(item_models.decode('utf-8'))
    item_models['item_models'].append(item_model)
    ply_db.put(bytes(uid_token, encoding='utf-8'), bytes(json.dumps(item_models), encoding='utf-8'))
    return json.dumps({'success': True, 'msg': 'Updated Item Models'}), 204

@app.route('/', methods=['GET'])
@cross_origin()
def get_user():
    uid_token = process_token(request.args.get('uid_token'))
    item_models = ply_db.get(bytes(uid_token, encoding='utf-8'))
    if item_models is None:
        return json.dumps({'success': False, 'msg': 'User does not exist'}), 404
    item_models = json.loads(item_models.decode('utf-8'))
    item_models['success'] = True
    return json.dumps(item_models), 200

@app.route('/', methods=['DELETE'])
@cross_origin()
def delete_user():
    uid_token = process_token(request.json['uid_token'])
    result = ply_db.get(bytes(uid_token, encoding='utf-8'))
    if result is None:
        return json.dumps({'success': False, 'msg': 'User does not exist'}), 404
    ply_db.delete(bytes(uid_token, encoding='utf-8'))
    return json.dumps({'success': True, 'msg': 'User deleted'}), 204

@app.route('/del_item_model', methods=['DELETE'])
@cross_origin()
def del_item_model():
    uid_token = process_token(request.json['uid_token'])
    target_item_model = request.json['item_model'].lower().strip()
    user_item_models = ply_db.get(bytes(uid_token, encoding='utf-8'))
    if user_item_models is None:
        return json.dumps({'success': False, 'msg': 'User does not exist'}), 404
    user_item_models = json.loads(user_item_models.decode('utf-8'))
    try:
        user_item_models['item_models'].remove(target_item_model)
        ply_db.put(bytes(uid_token, encoding='utf-8'), bytes(json.dumps(user_item_models), encoding='utf-8'))
        return json.dumps({'success': True, 'msg': 'Removed the item model'}), 204
    except ValueError:
        return json.dumps({'success': False, 'msg': 'Item model never existed'}), 404
            
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, threaded=True)
