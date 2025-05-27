from langchain.chains import LLMChain, SimpleSequentialChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# 첫번째 체인 - 시놉시스 작성
template1 = """당신은 극작가입니다. 연극 제목이 주어졌을 때, 그 줄거리를 작성하는 것이 당신의 임무입니다.
제목 : {title}
시놉시스 : 
"""

prompt1 = PromptTemplate(
    input_variables=["title"],
    template=template1,
)

chain1 = LLMChain(
    llm=OpenAI(
        model='gpt-3.5-turbo-instruct',
        temperature=0,
    ),
    prompt=prompt1,
)

# 두번째 체인 - 리뷰 작성
template2 = """당신은 연극 평론가입니다. 연극의 시놉시스가 주어졌을 때 그 리뷰를 작성하는 것이 당신의 임무입니다.
시놉시스 : {synopsis}
리뷰 : 
"""

prompt2 = PromptTemplate(
    input_variables=["synopsis"],
    template=template2,
)

chain2 = LLMChain(
    llm=OpenAI(
        model='gpt-3.5-turbo-instruct',
        temperature=0,
    ),
    prompt=prompt2,
)

# 체인 연결
overall_chain = SimpleSequentialChain(
    chains=[chain1, chain2],
    verbose=True
)

# 실행
print(overall_chain.run("서울 랩소디"))
