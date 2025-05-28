## p160_app.py

import openai 

messages = [
    {"role": "user", "content": "대한민국의 수도는 어디인가요?"},
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=messages,
    max_tokens=100,
    temperature=0.7,
    n = 1
)

print(response['choices'][0]['message']['content'])