import os
import dotenv
import openai
from utils import num_tokens_from_string
dotenv.load_dotenv()
openai.api_key = os.environ.get("OPENAI_API_KEY")
MODEL = os.environ.get("MODEL") or "gpt-3.5-turbo"

messages = [
    { "role": "system", "content": "You are a general, respond with a guy who is a general." },
    { "role": "user", "content": "You are Bob Manley reincarnated, Respond with a guy believe in Rasta and Bob Marley." },
    { "role": "assistant", "content": "ChatGPT response here..." },
]
total_token = 0
for i in messages:
    message = i["content"]
    token_count = num_tokens_from_string(message, MODEL)
    #print("this message costs", token_count, "tokens")
    total_token+=token_count

if total_token > 4096:
    print("total token is more than 4096, please reduce the message")
    exit()

# 0.002 / 1000 tokens
total_cost = total_token * (0.002 / 1000)
input_response = input(f"Total message costs {total_cost}$.\nTotal tokens {total_token}.\nDo you want to process tokens and get reponse Y/N ?\n")
if input_response.lower() != "y":
    exit()
# create a completion
completion = openai.ChatCompletion.create(model=MODEL, messages=messages)

# print the completion
breakpoint()
print(completion.choices[0].text)