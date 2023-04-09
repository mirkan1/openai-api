'''
    This version of application is using localstorage of pythonanwywhere instead of using mongodb.
    Same performance, but less secure.
'''
import os
from datetime import datetime
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from filestorage_user import *  # get_user_by_id, create_user, update_user, delete_user
from filestorage_user_helper import get_chats_len, get_chat, get_last_chat_message, \
    add_message, delete_chat, start_conversation, get_all_chats
from gpt_api import get_response
from utils import create_session

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/v2/*": {"origins": "*"}})

ENVIRONMENT = os.environ.get("ENVIRONMENT")
MODEL = os.environ.get("MODEL")

@app.route('/api/v2/start_conversation', methods=['POST'])
def api_start_conversation():
    api_key = request.headers.get("Api-Key")
    if not api_key:
        request.status_code = 401
        return jsonify({"error": "No Authorization"})
    message = request.json['message']
    role = request.json['role'] or "user"
    response = get_response([{
        "role": role,
        "content": message
    }], api_key)
    _id = start_conversation(message, role, api_key)
    add_message(_id, response, "bot", api_key)
    return jsonify({"response":response, "id":_id})

@app.route("/api/v2/chat/<id>", methods=['GET'])
def get_chat_by_id(id):
    api_key = request.headers.get("Api-Key")
    if not api_key:
        request.status_code = 401
        return jsonify({"error": "No Authorization"})
    return jsonify(get_chat(id, api_key))

@app.route("/api/v2/last_chat_message/<id>", methods=['GET'])
def last_chat_message(id):
    api_key = request.headers.get("Api-Key")
    if not api_key:
        request.status_code = 401
        return jsonify({"error": "No Authorization"})
    return jsonify(get_last_chat_message(id, api_key))

@app.route("/api/v2/add_message", methods=['POST'])
def add_message_to_chat():
    api_key = request.headers.get("Api-Key")
    if not api_key:
        request.status_code = 401
        return jsonify({"error": "No Authorization"})
    id = request.json['id']
    message = request.json['message']
    role = request.json['role']
    chat = get_chat(id, api_key)
    messages = []
    for i in chat["messages"]:
        messages.append(i)
    messages.append({"role":role, "content":message})
    response = get_response(messages, api_key)
    add_message(id, message, role, api_key)
    add_message(id, response, "bot", api_key)
    return jsonify(response)

@app.route("/api/v2/chat_list", methods=['GET'])
def chat_list():
    api_key = request.headers.get("Api-Key")
    if not api_key:
        request.status_code = 401
        return jsonify({"error": "No Authorization"})
    return jsonify(get_all_chats(api_key))

# delete
@app.route("/api/v2/delete_chat", methods=['POST'])
def api_delete_chat():
    api_key = request.headers.get("Api-Key")
    if not api_key:
        request.status_code = 401
        return jsonify({"error": "No Authorization"})
    id = request.json['id']
    delete_chat(id, api_key)
    return jsonify({"status":"success"})

models_url = "https://api.openai.com/v1/models"
@app.route("/api/v2/login", methods=['POST'])
def login():
    api_key = request.headers.get("Api-Key")
    if not api_key:
        request.status_code = 401
        return jsonify({"error": "No Authorization"})
    if not api_key:
        return jsonify({"status":"error", "message":"api_key is required"})
    user_found = get_user_by_id(api_key)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = requests.get(models_url, headers=headers, timeout=12)
    req_json = req.json()
    if "error" not in req_json:
        user_data = {
            "id": create_session(),
            "firstCreated": str(datetime.now()),
            "file": f"{api_key}.txt",
            "isPremium": False,
            "gptVersion": MODEL,
            "email": "",
        }
        print(user_data)
        create_user(api_key, user_data)
        return "OK"
    elif user_found:
        isPremium = user_found["isPremium"]
        if isPremium:
            id = user_found["id"]
            print(f"User {id} is premium")
            return "OK"
    return str(req_json["error"])

@app.route("/api/v2/models", methods=['GET'])
def models():
    api_key = request.headers.get("Api-Key")
    if not api_key:
        request.status_code = 401
        return jsonify({"error": "No Authorization"})
    if not api_key:
        return jsonify({"status":"error", "message":"api_key is required"})
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = requests.get(models_url, headers=headers, timeout=12)
    return req.json()

if __name__ == '__main__':
    DEBUG = os.environ.get('DEBUG', False)
    app.run(debug=True, port=1111)
