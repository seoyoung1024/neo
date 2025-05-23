from openai import OpenAI
client = OpenAI()

prompt = '좋아하는 음식은 무엇인가요 ->'
response = client.chat.completions.create(
    model = 'gpt-3.5-turbo-0125',
    messages = [
        {'role':'user', 'content': prompt}
    ]
)

print(response.choices[0].message.content.strip())