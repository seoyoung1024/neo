import ollama
import os


img_path = './data/image.png'
print(os.path.exists(img_path))

response = ollama.chat(
    model="llama3.2-vision:latest",
    messages=[
        {"role":"user", "content": "사진 속의 승용차의 차종과 번호를 알려줘아아아", "image": [img_path]}
    ]
)

print(response['message']['content'])