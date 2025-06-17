import getpass
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

llm = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ("system", """
     I want you to act as a Financial Analyst.
     Want assistance provided by qualified individuals enabled with experience on understanding charts using technical analysis tools while interpreting macroeconomic environment prevailing across world consequently assisting customers acquire long term advantages requires clear verdicts therefore seeking same through informed predictions written down precisely! First statement contains following content- “Can you tell us what future stock market looks like based upon current conditions ?".
     """),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser
response = chain.invoke({"input": "월마트의 주간 차트를 분석해주세요."})