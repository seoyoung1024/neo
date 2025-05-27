from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain

prompt = PromptTemplate(
    input_variables = ["product"],
    template = "{product}을 만드는 새로운 회사이름을 하나 제안해 주세요"
)

chains = LLMChain(
    llm=OpenAI(
        model = 'gpt-3.5-turbo-instruct',
        temperature = 0.9
    ),
    prompt=prompt
)
product = "컴퓨터게임"
print(prompt.format(product=product))
print(chains.run(product))