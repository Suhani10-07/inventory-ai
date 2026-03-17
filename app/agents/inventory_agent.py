from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI

from app.agents.langgraph_agent import (
    add_inventory_product,
    update_inventory_stock,
    get_low_stock
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

inventory_tools = [
    add_inventory_product,
    update_inventory_stock,
    get_low_stock
]

inventory_agent = create_react_agent(llm, inventory_tools)