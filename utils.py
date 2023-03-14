import os
import tiktoken
import pymongo
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.environ.get("MONGO_URL")
MONGO_CLIENT = pymongo.MongoClient(MONGO_URL)
MONGO_TYPE = {
    "id": int,
    "messages": [
        {
            "role": str, 
            "content": str
        },]
}

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_chats_len():
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    return col.count_documents({})

def get_chat(id):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    return col.find_one({"id":int(id)})

def get_last_chat_message(id):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    return col.find_one({},{"id":int(id)})

def add_message(id, message, role):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    col.update_one({"id":int(id)}, {"$push":{"messages":{"role":role, "content":message}}})

def start_conversation(id, message, role):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    col.insert_one({"id":int(id), "messages":[{"role":role, "content":message}]})
    
def get_all_chats():
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    return col.find()