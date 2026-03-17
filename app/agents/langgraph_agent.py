from langchain.tools import tool
from app.database import collection
from bson import ObjectId
from app.ml.predictor import moving_average_prediction
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
import os
from app.services.inventory_service import create_product, update_product_stock
from dotenv import load_dotenv
from pydantic import BaseModel

class AddProductInput(BaseModel):
    name: str
    stock: int
    price: float
    category: str
    
class UpdateStockInput(BaseModel):
    product_name: str
    stock: int
    
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")



@tool
def get_low_stock():
    """Returns products with stock less than 5"""
    products = []
    for product in collection.find({"stock": {"$lt": 5}}):
        products.append(product["name"])
    return f"Low stock products: {products}"


@tool
def get_inventory_value():
    """Returns total inventory value"""
    total = 0
    for product in collection.find():
        total += product["stock"] * product["price"]
    return f"Total inventory value is {total}"


@tool
def predict_product_demand(product_name: str):
    """Predict demand for a given product"""
    product = collection.find_one({"name": product_name})
    if not product:
        return "Product not found"
    sales_history = product.get("sales_history", [])
    if not sales_history:
        return "No sales history available"
    prediction = moving_average_prediction(sales_history)
    return f"Predicted demand for {product_name} is {round(float(prediction), 2)}"

@tool(args_schema=AddProductInput)
def add_inventory_product(name: str, stock: int, price: float, category: str):
    """Add a new product to the inventory"""
    product_id = create_product(name, stock, price, category)
    return f"Product {name} added with id {product_id}"


@tool(args_schema=UpdateStockInput)
def update_inventory_stock(product_name: str, stock: int):
    """Update stock for an existing product"""
    return update_product_stock(product_name, stock)

# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",
#     temperature=0
# )

# print("DEBUG API KEY:", api_key)  # temporary debug

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    api_key=api_key
)

tools = [
    get_low_stock,
    get_inventory_value,
    predict_product_demand,
    add_inventory_product,
    update_inventory_stock
]

agent = create_react_agent(llm, tools)