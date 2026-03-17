from fastapi import APIRouter
from app.database import collection
from app.models import Product
from datetime import datetime
from bson import ObjectId
from app.redis_client import redis_client
from app.ml.predictor import moving_average_prediction
from app.agents.langgraph_agent import agent
from app.agents.supervisor import supervisor_router


router = APIRouter()

# CREATE PRODUCT
@router.post("/products")
def add_product(product: Product):
    product_dict = product.dict()
    product_dict["last_updated"] = datetime.utcnow()
    result = collection.insert_one(product_dict)
    redis_client.delete("inventory_value")  # 👈 invalidate cache
    # 🔥 Low stock alert
    if product.stock < 5:
        redis_client.publish(
            "low_stock_channel",
            f"Low stock alert for {product.name}"
        )
    return {"id": str(result.inserted_id)}


# GET ALL PRODUCTS
@router.get("/products")
def get_products():
    products = []
    for product in collection.find():
        product["_id"] = str(product["_id"])
        products.append(product)
    return products


# UPDATE STOCK
@router.put("/products/{product_id}")
def update_stock(product_id: str, stock: int):
    collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": {"stock": stock, "last_updated": datetime.utcnow()}}
    )
    redis_client.delete("inventory_value")  # 👈 invalidate cache
    # 🔥 Fetch product to check
    product = collection.find_one({"_id": ObjectId(product_id)})
    if product and product["stock"] < 5:
        redis_client.publish(
            "low_stock_channel",
            f"Low stock alert for {product['name']}"
        )
    return {"message": "Stock updated"}

# DELETE PRODUCT
@router.delete("/products/{product_id}")
def delete_product(product_id: str):
    collection.delete_one({"_id": ObjectId(product_id)})
    redis_client.delete("inventory_value")  # 👈 invalidate cache
    return {"message": "Product deleted"}

@router.get("/low-stock")
def get_low_stock(threshold: int = 5):
    products = []
    for product in collection.find({"stock": {"$lt": threshold}}):
        product["_id"] = str(product["_id"])
        products.append(product)
    return products

@router.get("/inventory-value")
def inventory_value():
    cached_value = redis_client.get("inventory_value")
    if cached_value:
        return {"total_inventory_value": float(cached_value), "source": "cache"}
    total_value = 0
    for product in collection.find():
        total_value += product["stock"] * product["price"]
    redis_client.setex("inventory_value", 60, total_value)
    return {"total_inventory_value": total_value, "source": "database"}

@router.get("/category-summary")
def category_summary():
    pipeline = [
        {
            "$group": {
                "_id": "$category",
                "total_products": {"$sum": 1},
                "total_stock": {"$sum": "$stock"},
                "total_value": {
                    "$sum": {"$multiply": ["$stock", "$price"]}
                }
            }
        }
    ]

    results = list(collection.aggregate(pipeline))
    for r in results:
        r["_id"] = r["_id"]

    return results


@router.get("/predict-demand/{product_id}")
def predict_demand(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})

    if not product:
        return {"error": "Product not found"}

    sales_history = product.get("sales_history", [])

    if not sales_history:
        return {"error": "No sales history available"}

    prediction = moving_average_prediction(sales_history)

    return {
        "product": product["name"],
        "predicted_next_demand": round(float(prediction), 2)
    }
    
@router.post("/assistant")
def assistant(query: str):
    response = supervisor_router(query)
    return {"response": response["messages"][-1].content}

