import os
from flask import Flask, render_template, request, redirect, jsonify
from dotenv import load_dotenv
from utils import get_chat, get_last_chat_message, add_message, \
    delete_chat, start_conversation, get_all_chats, get_chats_len
from gpt_api import get_response
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

MONGO_DB_LENGTH = get_chats_len()
ENVIRONMENT = os.environ.get("ENVIRONMENT")
if ENVIRONMENT == "dev":
    from speech import speak
else:
    def speak(text):
        pass

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
    silence = request.json['silence']
    response = get_response([{
        "role": role,
        "content": message
    }])
    if not silence:
        speak(response)
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
    silence = request.json['silence']
    chat = get_chat(id)
    messages = []
    for i in chat["messages"]:
        role = i["role"]
        messages.append(i)
    messages.append({"role":role, "content":message})
    response = get_response(messages)
    if not silence:
        speak(response)
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

# END API

if __name__ == '__main__':
    DEBUG = os.environ.get('DEBUG', False)
    app.run(debug=True, port=1111)
