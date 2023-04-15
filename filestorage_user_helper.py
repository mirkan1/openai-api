import json
import os
from dotenv import load_dotenv
load_dotenv()
INDENT = int(os.environ.get("INDENT") or 0)
USER_DIR = os.environ.get("USER_DIR")

def enforce_data_file_path(api_key):
    data_file_path = get_data_file_path(api_key)
    if not os.path.exists(data_file_path):
        with open(data_file_path, "w") as f:
            f.write("[]")

def get_chats_len(api_key):
    data_file_path = get_data_file_path(api_key)
    enforce_data_file_path(api_key)
    with open(data_file_path, "r") as f:
        data = f.read()
        chats = json.loads(data)
        return len(chats)

def get_chat(_id, api_key):
    data_file_path = get_data_file_path(api_key)
    enforce_data_file_path(api_key)
    with open(data_file_path, "r") as f:
        data = f.read()
        chats = json.loads(data)
        for chat in chats:
            if str(chat["_id"]) == str(_id):
                return chat
        return None

def get_last_chat_message(_id, api_key):
    data_file_path = get_data_file_path(api_key)
    enforce_data_file_path(api_key)
    with open(data_file_path, "r") as f:
        data = f.read()
        chats = json.loads(data)
        for chat in chats:
            if str(chat["_id"]) == str(_id):
                return chat["messages"][-1]
        return None

def add_message(_id, message, role, api_key):
    data_file_path = get_data_file_path(api_key)
    enforce_data_file_path(api_key)
    with open(data_file_path, "r") as f:
        data = f.read()
        chats = json.loads(data)
    for chat in chats:
        if str(chat["_id"]) == str(_id):
            chat["messages"].append({"role": role, "content": message})
            with open(data_file_path, "w") as f:
                f.write(json.dumps(chats, indent=INDENT))
            return
    raise ValueError("Chat not found")

def get_file_path(api_key):
    return os.path.join(USER_DIR, api_key + ".json")

def get_data_file_path(api_key):
    return os.path.join(USER_DIR, api_key + "_DATA_.json")

def start_conversation(message, role, api_key):
    file_path = get_file_path(api_key)
    data_file_path = get_data_file_path(api_key)
    enforce_data_file_path(api_key)
    with open(data_file_path, "r") as f:
        data = f.read()
        chats = json.loads(data)
    selected_id = 0
    for chat in chats:
        chat_id = chat["_id"]
        if chat_id > selected_id:
            selected_id = chat_id
    print(selected_id)
    new_chat = {"_id": selected_id + 1, "messages": [{"role": role, "content": message}]}
    chats.append(new_chat)
    with open(data_file_path, "w") as f:
        f.write(json.dumps(chats, indent=INDENT))
    return str(new_chat["_id"])

def get_all_chats(api_key):
    data_file_path = get_data_file_path(api_key)
    enforce_data_file_path(api_key)
    with open(data_file_path, "r") as f:
        data = f.read()
        chats = json.loads(data)
        return chats

def delete_chat(_id, api_key):
    data_file_path = get_data_file_path(api_key)
    enforce_data_file_path(api_key)
    with open(data_file_path, "r") as f:
        data = f.read()
        chats = json.loads(data)
    for i, chat in enumerate(chats):
        if str(chat["_id"]) == str(_id):
            del chats[i]
            with open(data_file_path, "w") as f:
                f.write(json.dumps(chats, indent=INDENT))
            return
    raise ValueError("Chat not found")