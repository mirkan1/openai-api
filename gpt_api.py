import os
import dotenv
import openai
from utils import num_tokens_from_string
dotenv.load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("MODEL", "gpt-3.5-turbo")

# messages = [
#     { "role": "system", "content": "You are a helpful assistant." },
#     { "role": "user", "content": "You are Bob Manley reincarnated, Respond with a guy believe in Rasta and Bob Marley." },
#     { "role": "assistant", "content": "..." },
# ]

def get_response(messages):
    total_token = 0
    for i in messages:
        message = i["content"]
        role = i["role"]
        token_count = num_tokens_from_string(message, MODEL)
        # print("this message costs", token_count, "tokens", message[:20], "...")
        total_token+=token_count
        if role=="bot":
            i['role'] = "assistant"
    if total_token > 4096:
        return "Message too long, please try again."

    # 0.002 / 1000 tokens
    total_cost = total_token * (0.002 / 1000)
    # input_response = input(f"Total message costs {total_cost}$.\nTotal tokens {total_token}.\nDo you want to process tokens and get reponse Y/N ?\n")
    # if input_response.lower() != "y":
    #     exit()
    # create a completion
    print(f"Total message costs {total_cost}$.\nTotal tokens {total_token}.")
    completion = openai.ChatCompletion.create(model=MODEL, messages=messages)
    return completion.choices[0].message.content