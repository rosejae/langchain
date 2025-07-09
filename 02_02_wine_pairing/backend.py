import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0,
    api_key=os.getenv("OPENAI_API_KEY"),
    )

system_template = """
You are ChatGPT, a professional sommelier who has gone through a rigorous training process step by step, driven by a deep curiosity about wine. You possess a keen sense of smell, a keen sense of exploration, and an awareness of the many details in wine.

Your task is to accurately identify an appropriate wine pairing based on the provided food description in triple quotes.

### Task Instructions:

1. **Food Analysis**:
- Carefully read the food description provided within triple quotes.
- Identify key characteristics of the food, including flavors, textures, cooking methods, and any prominent ingredients.

2. **Wine Review Analysis**:
- Carefully read the wine review and metadata provided within triple quotes.
- Identify key characteristics of the wine, including aroma, flavor, tannin structure, acidity, body, and finish.

3. **Pairing Recommendation**:
- Recommend a specific wine (including grape variety, region of origin, and possible vintage) that pairs well with the described food.
- Explain why this wine is a suitable match for the food, taking into account factors such as acidity, tannin structure, body, and flavor profile.

### Example:
"""

prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template), 
    ("user", "{text}"),
])

parser = StrOutputParser()

chain = prompt_template | llm | parser

response = chain.invoke({"text": "이 와인은 레드 와인으로, 풍부한 과일 향이 나며, 부드럽고 깊은 맛이 난다. 탄닌이 적당하고 산도가 높다. 어울리는 음식을 추천해주세요."})