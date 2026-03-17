from app.database import collection
from datetime import datetime
from bson import ObjectId


def create_product(name, stock, price, category, sales_history=None):
    product = {
        "name": name,
        "stock": stock,
        "price": price,
        "category": category,
        "sales_history": sales_history or [],
        "last_updated": datetime.utcnow(),
    }

    result = collection.insert_one(product)
    return str(result.inserted_id)


def update_product_stock(product_name, stock):
    product = collection.find_one({"name": product_name})

    if not product:
        return "Product not found"

    collection.update_one(
        {"_id": ObjectId(product["_id"])},
        {"$set": {"stock": stock, "last_updated": datetime.utcnow()}}
    )

    return f"Stock updated for {product_name}"