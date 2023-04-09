import requests
import os
from dotenv import load_dotenv
load_dotenv()
PORT = os.getenv("PORT")

def test_start_conversation(message="hello", role="user", silence=False):
    url = f"http://localhost:{PORT}/api/start_conversation"
    data = {"message": message, "role": role, "silence": silence}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    res_json = response.json()
    assert "response" in res_json
    assert "id" in res_json
    return res_json