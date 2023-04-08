import json
import os

USER_DIR = "users"

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
        json.dump(user_data, f)
    return user_id

def update_user(user_id, user_data):
    file_path = os.path.join(USER_DIR, f"{user_id}.json")
    if not os.path.exists(file_path):
        raise ValueError("User not found")
    with open(file_path, "w") as f:
        json.dump(user_data, f)

def delete_user(user_id):
    file_path = os.path.join(USER_DIR, f"{user_id}.json")
    if not os.path.exists(file_path):
        raise ValueError("User not found")
    os.remove(file_path)
