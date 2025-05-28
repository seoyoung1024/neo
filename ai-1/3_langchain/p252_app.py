from langchain.agnets import load_tools
from langchain.models import ChatOpenAI
from langchain.chain.conversation.memory import conversationBufferWindowMemory
from langchain.agnets import initialize_agent

tools = load_tools(
    tools_name = ["serpapi", "llm-math"],
    llm = ChatOpenAI(
        model = "gpt-3.5-turbo"
        temperature = 0
    )
)

memory = conversationBufferWindowMemory(
    memory_key = "chat_history",
    return_messages = True,
)

agnet = initialize_agent(
    agnet = "conversational-react-description",
    llm = ChatOpenAI(
        model = "gpt-3.5-turbo",
        temperature = 0
    ),
    tools = tools,
    verbose = True,
    memory = memory
)

print(agnet.run("좋은 아침입니다."))
print('-' * 50)

print(agnet.run("우리집 반려견 이름은 보리입니다."))
print('-' * 50)

print(agnet.run("우리집 반려견 이름을 불러주세요."))
print('-' * 50)

