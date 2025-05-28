import os
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory

# 환경 변수에서 Wolfram Alpha App ID 불러오기
wolfram_alpha_appid = os.environ.get("WOLFRAM_ALPHA_APPID")

# 도구 준비
tools = load_tools(['wolfram-alpha'], wolfram_alpha_appid=wolfram_alpha_appid)

# 메모리 생성
memory = ConversationBufferWindowMemory(
    memory_key="chat_history",
    return_messages=True,
)

# 에이전트 생성
agent = initialize_agent(
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0
    ),
    tools=tools,
    verbose=True,
    memory=memory
)

# 질의 실행
query = "How many kilometers is the distance between Seoul and Busan?"
print('-' * 50)
print(query)
print(agent.run(query))
