import json
import os
from dotenv import load_dotenv
load_dotenv()
INDENT = int(os.environ.get("INDENT") or 0)
USER_DIR = os.environ.get("USER_DIR")

def set_user_data(user_id, data):
    user_data = get_user_by_id(user_id)
    if user_data is None:
        user_data = {}
    user_data.update(data)
    create_user(user_id, user_data)
    return user_data

def set_environment():
    if not os.path.exists(USER_DIR):
        os.mkdir(USER_DIR)

def get_user_by_id(user_id):
    file_path = os.path.join(USER_DIR, f"{user_id}.json")
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        user_data = json.load(f)
    return user_data

def create_user(api_key, user_data):
    user_id = api_key
    file_path = os.path.join(USER_DIR, f"{user_id}.json")
    with open(file_path, "w") as f:
        json.dump(user_data, f, indent=INDENT)
    return user_id

def update_user(user_id, user_data):
    file_path = os.path.join(USER_DIR, f"{user_id}.json")
    if not os.path.exists(file_path):
        raise ValueError("User not found")
    with open(file_path, "w") as f:
        json.dump(user_data, f, indent=INDENT)

def delete_user(user_id):
    file_path = os.path.join(USER_DIR, f"{user_id}.json")
    if not os.path.exists(file_path):
        raise ValueError("User not found")
    os.remove(file_path)

set_environment()
