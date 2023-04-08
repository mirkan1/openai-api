import json
import os
user = "user1"
data = [
    {
        "user1": {
            "firstCreated": "2021-04-01 00:00:00",
            "file": "user1.txt",
            "isPremium": False,
            "gptVersion": "gpt2",
            "data": [
                {
                    "_id": 1,
                    "messages": [
                        {
                            "role": "user",
                            "content": "Hello"
                        },
                        {
                            "role": "bot",
                            "content": "Hi, How can I help you?"
                        }
                    ]
                }
            ]
        }
    }
]
FILE_PATH = "chats.txt"
if not os.path.exists(FILE_PATH):
    with open(FILE_PATH, "w") as f:
        f.write("[]")

def get_chats_len():
    with open(FILE_PATH, "r") as f:
        data = f.read()
        chats = json.loads(data)
        return len(chats)

def get_chat(_id):
    with open(FILE_PATH, "r") as f:
        data = f.read()
        chats = json.loads(data)
        for chat in chats:
            if str(chat["_id"]) == _id:
                return chat
        return None

def get_last_chat_message(_id):
    with open(FILE_PATH, "r") as f:
        data = f.read()
        chats = json.loads(data)
        for chat in chats:
            if str(chat["_id"]) == _id:
                return chat["messages"][-1]
        return None

def add_message(_id, message, role):
    with open(FILE_PATH, "r") as f:
        data = f.read()
        chats = json.loads(data)
    for chat in chats:
        if str(chat["_id"]) == _id:
            chat["messages"].append({"role": role, "content": message})
            with open(FILE_PATH, "w") as f:
                f.write(json.dumps(chats))
            return
    raise ValueError("Chat not found")

def start_conversation(message, role):
    with open(FILE_PATH, "r") as f:
        data = f.read()
        chats = json.loads(data)
    new_chat = {"_id": len(chats) + 1, "messages": [{"role": role, "content": message}]}
    chats.append(new_chat)
    with open(FILE_PATH, "w") as f:
        f.write(json.dumps(chats))
    return str(new_chat["_id"])

def get_all_chats():
    with open(FILE_PATH, "r") as f:
        data = f.read()
        chats = json.loads(data)
        return chats

def delete_chat(_id):
    with open(FILE_PATH, "r") as f:
        data = f.read()
        chats = json.loads(data)
    for i, chat in enumerate(chats):
        if str(chat["_id"]) == _id:
            del chats[i]
            with open(FILE_PATH, "w") as f:
                f.write(json.dumps(chats))
            return
    raise ValueError("Chat not found")