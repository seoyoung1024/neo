import os
from langchain.agnets import load_tools
from langchain.models import ChatOpenAI
from langchain.chain.conversation.memory import conversationBufferWindowMemory
from langchain.agnets import initialize_agent

google_cse_id = os.environ.get("GOOGLE_CSE_ID")
google_api_key = os.environ.get("GOOGLE_API_KEY")

#도구 준비
tools = load_tools(
    tools_name = ['google-search'],
    llm = ChatOpenAI(
        model = "gpt-3.5-turbo"
        temperature = 0
    )
)

#메모리 생성
memory = conversationBufferWindowMemory(
    memory_key = "chat_history",
    return_messages = True,
)

#에이전트 생성
agnet = initialize_agent(
    agnet = "zero-shot-react-description",
    llm = ChatOpenAI(
        model = "gpt-3.5-turbo",
        temperature = 0
    ),
    tools = tools,
    verbose = True,
    memory = memory
)

query = "영화 명량의 감독은?"
print('-' * 50)
print(query)
print(agnet.run(query))