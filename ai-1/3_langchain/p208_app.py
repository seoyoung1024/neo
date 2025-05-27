import os
from langchain.llms import OpenAI
from langchain.agents import load_tools
from langchain.agents import initialize_agent

serpapi_api_key = os.environ['SERPAPI_API_KEY']

tools = load_tools(["serpapi", "llm-math"], llm=OpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0
    ),
    serpapi_api_key=serpapi_api_key
)

agent = initialize_agent(
    agent="zero-shot-react-description",
    llm=OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0
    ),
    tools=tools,
    verbose=True
)

print('-' * 50)
input_agent = "123 * 4를 계산기로 계산하세요"
agent.run(input_agent)

print('-' * 50)
input_agent = "오늘 한국 서울의 날씨를 웹 검색으로 확인하세요"
agent.run(input_agent)