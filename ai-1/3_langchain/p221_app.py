from langchain.llms import OpenAI
from langchain.callbacks.streaming_s

llm = OpenAI(
    model = 'gpt-3.5-turbo-instruct',
        temperature = 0,
        streaming = True,
        callbacks = [streamingStdOutCallbackHandler()],
        verbose = True
)

res = llm("즐거운 ChatGPT 생활을 가사로 노래를 만들어주세요")
print(res)