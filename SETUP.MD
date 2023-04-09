
# curl example request
```bash
curl https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
     "model": "gpt-3.5-turbo",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'
```

# output
```
{
   "id":"chatcmpl-abc123",
   "object":"chat.completion",
   "created":1677858242,
   "model":"gpt-3.5-turbo-0301",
   "usage":{
      "prompt_tokens":13,
      "completion_tokens":7,
      "total_tokens":20
   },
   "choices":[
      {
         "message":{
            "role":"assistant",
            "content":"\n\nThis is a test!"
         },
         "finish_reason":"stop",
         "index":0
      }
   ]
}
```

# example user data in python memory and files
```python
data = [
    {
        "user1": {
            "id":132123123123,
            "firstCreated": "2021-04-01 00:00:00",
            "file": "user1.txt",
            "isPremium": False,
            "gptVersion": "gpt2",
            "email": "mirkanbaba1@gmail.com",
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
```