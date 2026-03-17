from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    name: str
    stock: int
    price: float
    category: str
    sales_history: Optional[List[int]] = []
    last_updated: Optional[datetime] = None