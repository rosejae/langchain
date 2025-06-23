import getpass
import os
import json

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
# from dotenv import load_dotenv

from stock_info import Stock

# load_dotenv()

now_path = './'
with open(f'{now_path}/metadata/setting.json', 'r', encoding='utf-8') as file:
    config_dict = json.load(file)
    
ACCESS_KEY = config_dict['ACCESS_KEY']

if not os.environ.get("OPENAI_API_KEY"):
    if ACCESS_KEY:
        os.environ["OPENAI_API_KEY"] = ACCESS_KEY
    else:
        os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter API key for OpenAI: ")

llm = ChatOpenAI()

def AI_report(ticker):
    prompt = ChatPromptTemplate.from_messages([
        ("system", """
        I want you to act as a Financial Analyst.
        Want assistance provided by qualified individuals enabled with experience on understanding charts using technical analysis tools while interpreting macroeconomic environment prevailing across world consequently assisting customers acquire long term advantages requires clear verdicts therefore seeking same through informed predictions written down precisely! First statement contains following content- “Can you tell us what future stock market looks like based upon current conditions ?".
        """),
        ("user", f'''
        I'll give you information for analysis.
        Provide your opinion in Korean as a Financial Analyst based on the markdown reports.
        """
        {{markdown}}
        """
        ''')
    ])

    output_parser = StrOutputParser()

    chain = prompt | llm | output_parser
    return chain.invoke({
        "markdown": Stock(ticker).report_support(),
    })