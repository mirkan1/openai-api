import os
import tiktoken
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv

load_dotenv()
MONGO_URL = os.environ.get("MONGO_URL")
MONGO_CLIENT = MongoClient(MONGO_URL)
MONGO_TYPE = {
    "id": int,
    "messages": [
        {
            "role": str, # user or system, assistant is for bot
            "content": str
        },]
}

def num_tokens_from_string(string: str, encoding_name: str, encoding_type: str="cl100k_base") -> int:
    """Returns the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(encoding_name)
    except:
        encoding = tiktoken.get_encoding(encoding_type)

    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_chats_len():
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    return col.count_documents({})

def get_chat(_id):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    return col.find_one({"_id":ObjectId(_id)})

def get_last_chat_message(_id):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    return col.find_one({},{"_id":ObjectId(_id)})

def add_message(_id, message, role):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    col.update_one({"_id":ObjectId(_id)}, {"$push":{"messages":{"role":role, "content":message}}})

def start_conversation(message, role):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    _id = col.insert_one({"messages":[{"role":role, "content":message}]})
    return str(_id.inserted_id)
    
def get_all_chats():
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    return col.find()

def delete_chat(_id):
    db = MONGO_CLIENT["chat-gpt-api"]
    col = db["chats"]
    col.delete_one({"_id":ObjectId(_id)})
