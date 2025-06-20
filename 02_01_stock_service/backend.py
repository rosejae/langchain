import getpass
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from stock_info import financial_statements, value_evaluation, blue_chip_stock, volume

if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

llm = ChatOpenAI()

prompt = ChatPromptTemplate.from_messages([
    ("system", """
     I want you to act as a Financial Analyst.
     Want assistance provided by qualified individuals enabled with experience on understanding charts using technical analysis tools while interpreting macroeconomic environment prevailing across world consequently assisting customers acquire long term advantages requires clear verdicts therefore seeking same through informed predictions written down precisely! First statement contains following content- “Can you tell us what future stock market looks like based upon current conditions ?".
     """),
    ("user", f'''
     I'll give you the indicators of a company. Please summarize the information.
     Balance Sheet: """{{balance_sheet}}"""
     Value Stock: """{{value_stock}}"""
     Blue Chip Stock: """{{blue_chip_stock}}"""
     Volume: """{{volume}}"""
     
     {input}
     
     한글로 답변해 주세요.
     ''')
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser
response = chain.invoke({"input": "애플의 주간 차트를 분석해주세요.",
                        "balance_sheet": financial_statements(),
                        "value_stock": value_evaluation(),
                        "blue_chip_stock": blue_chip_stock(),
                        "volume": volume(),
                         })