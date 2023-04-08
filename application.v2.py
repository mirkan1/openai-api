'''
    This version of application is using localstorage of pythonanwywhere instead of using mongodb.
    Same performance, but less secure.
'''
import os
import requests
from flask import Flask, render_template, request, redirect, jsonify
from dotenv import load_dotenv
from filestorage import get_chats_len, get_chat, get_last_chat_message, \
    add_message, delete_chat, start_conversation, get_all_chats
from gpt_api import get_response
from utils import create_session
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

ENVIRONMENT = os.environ.get("ENVIRONMENT")

# HTML
@app.route("/", methods=['GET'])
def home():
    chats = get_all_chats()
    return render_template("index.html", chats=chats, title="Home")

@app.route("/chat/<id>", methods=['GET'])
def chat(id):
    chat = get_chat(id)
    title = chat['messages'][0]['content'][:64]
    return render_template("chat.html", chat=chat, id=id, title=title)
# END HTML

# API
@app.route('/api/start_conversation', methods=['POST'])
def api_start_conversation():
    message = request.json['message']
    role = request.json['role'] or "user"
    response = get_response([{
        "role": role,
        "content": message
    }])
    _id = start_conversation(message, role)
    add_message(_id, response, "bot")
    return jsonify({"response":response, "id":_id})

@app.route("/api/chat/<id>", methods=['GET'])
def get_chat_by_id(id):
    return jsonify(get_chat(id))

@app.route("/api/last_chat_message/<id>", methods=['GET'])
def last_chat_message(id):
    return jsonify(get_last_chat_message(id))

@app.route("/api/add_message", methods=['POST'])
def add_message_to_chat():
    id = request.json['id']
    message = request.json['message']
    role = request.json['role']
    chat = get_chat(id)
    messages = []
    for i in chat["messages"]:
        role = i["role"]
        messages.append(i)
    messages.append({"role":role, "content":message})
    response = get_response(messages)
    add_message(id, message, role)
    add_message(id, response, "bot")
    return jsonify(response)

@app.route("/api/chat_list", methods=['GET'])
def chat_list():
    return jsonify(get_all_chats())

# delete
@app.route("/api/delete_chat", methods=['POST'])
def api_delete_chat():
    id = request.json['id']
    delete_chat(id)
    return jsonify({"status":"success"})

models_url = "https://api.openai.com/v1/models"
@app.route("/api/v2/login", methods=['POST'])
def login():
    api_key = request.headers.get("Api-Key")
    if not api_key:
        return jsonify({"status":"error", "message":"api_key is required"})
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = requests.get(models_url, headers=headers, timeout=12)
    req_json = req.json()
    if "error" not in req_json:
        # for i in req['data']:
        #     if i['id'] == "davinci":
        #         return jsonify({"status":"success"}) 
        return "OK"
    return str(req_json["error"])

@app.route("/api/v2/models", methods=['GET'])
def models():
    api_key = request.headers.get("Api-Key")
    if not api_key:
        return jsonify({"status":"error", "message":"api_key is required"})
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    req = requests.get(models_url, headers=headers, timeout=12)
    return req.json()
# END API

if __name__ == '__main__':
    DEBUG = os.environ.get('DEBUG', False)
    app.run(debug=True, port=1111)
