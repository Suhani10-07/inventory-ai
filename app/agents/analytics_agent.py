from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.langgraph_agent import (
    get_inventory_value,
    predict_product_demand
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

analytics_tools = [
    get_inventory_value,
    predict_product_demand
]

analytics_agent = create_react_agent(llm, analytics_tools)