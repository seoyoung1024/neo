import ollama

response = ollama.chat(
    model = 'llama3.2:latest',
    messages = [
        {'role': 'system', 'content': 'You are a python expoert. '},
        {'role': 'user', 'content': 'Code a Python function to generate a Fibonaccisequence.'}
    ]
)

print(response['message']['content'])