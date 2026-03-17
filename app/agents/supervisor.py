from app.agents.inventory_agent import inventory_agent
from app.agents.analytics_agent import analytics_agent


def supervisor_router(query: str):

    inventory_keywords = ["add", "update", "stock", "low stock"]
    analytics_keywords = ["value", "predict", "demand"]

    if any(word in query.lower() for word in inventory_keywords):
        return inventory_agent.invoke({"messages": [("user", query)]})

    if any(word in query.lower() for word in analytics_keywords):
        return analytics_agent.invoke({"messages": [("user", query)]})

    return {"messages": [("assistant", "Sorry, I could not determine the task.")]}