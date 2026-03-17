# 🚀 AI-Powered Smart Inventory System

An **AI-native backend system** that combines FastAPI, MongoDB, Redis, ML, and LangGraph agents to manage inventory intelligently.

This is not just CRUD — it includes:

* 🤖 AI assistant (Gemini)
* ⚡ Redis caching
* 📊 Demand prediction (ML)
* 🔔 Event-driven alerts
* 🧩 Multi-agent architecture

---

# 🧠 Features

## ✅ Core Backend

* Product CRUD (Create, Read, Update, Delete)
* MongoDB integration
* Pydantic validation

## ⚡ Performance

* Redis caching (TTL-based)
* Cache invalidation on updates

## 🤖 AI Assistant (LangGraph + Gemini)

Supports natural language:

### Queries

* "Which products are low in stock?"
* "What is total inventory value?"
* "Predict demand for Laptop"

### Actions

* "Add 10 laptops priced 65000 in electronics"
* "Update laptop stock to 5"

---

## 📊 Analytics

* Inventory value calculation
* Category aggregation
* Demand prediction (Moving Average)

---

## 🔔 Event System

* Redis Pub/Sub for low stock alerts

---

## 🧩 Architecture

Multi-agent system:

* Inventory Agent (CRUD)
* Analytics Agent (ML + stats)
* Supervisor Agent (routing)

---

# 🏗️ Project Structure

```

inventory-ai/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── redis_client.py
│   │
│   ├── routes/
│   │   └── inventory.py
│   │
│   ├── services/
│   │   └── inventory_service.py
│   │
│   ├── agents/
│   │   ├── langgraph_agent.py
│   │   ├── inventory_agent.py
│   │   ├── analytics_agent.py
│   │   └── supervisor.py
│   │
│   ├── ml/
│   │   └── predictor.py
│   │
│   └── alerts_listener.py
│
├── requirements.txt
└── README.md

````

---

# ⚙️ Tech Stack

* FastAPI
* MongoDB
* Redis
* LangGraph
* LangChain
* Google Gemini (LLM)
* NumPy

---

# 🧪 Setup Instructions

## 1️⃣ Clone the Project

```bash
git clone <your-repo-url>
cd inventory-ai
````

---

## 2️⃣ Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Set Environment Variables

Create `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key
```

---

## 5️⃣ Start MongoDB (Docker)

```bash
docker run -d -p 27017:27017 --name inventory-mongo mongo
```

If already created:

```bash
docker start inventory-mongo
```

---

## 6️⃣ Start Redis (Docker)

```bash
docker run -d -p 6379:6379 --name inventory-redis redis
```

If already created:

```bash
docker start inventory-redis
```

---

## 7️⃣ Run FastAPI Server

```bash
uvicorn app.main:app --reload --port 8001
```

Open Swagger:

```
http://127.0.0.1:8001/docs
```

---

## 8️⃣ (Optional) Run Alert Listener

```bash
python app/alerts_listener.py
```

---

# 🤖 AI Assistant Usage

### Endpoint

```
POST /assistant
```

### Example Queries

```
Which products are low in stock?
```

```
Add 15 laptops priced 65000 in electronics
```

```
Update laptop stock to 3
```

```
Predict demand for Laptop
```

---

# 📊 Example Product Schema

```json
{
  "name": "Laptop",
  "stock": 10,
  "price": 60000,
  "category": "electronics",
  "sales_history": [10, 12, 15],
  "last_updated": "timestamp"
}
```

---

# ⚠️ Important Notes

## MongoDB Errors

If you see:

```
Connection refused
```

Run:

```bash
docker start inventory-mongo
```

---

## Redis Errors

```bash
docker start inventory-redis
```

---

## API Key Safety

* Never print API keys
* Always store in `.env`

---

## Product Name Ambiguity

* System internally uses `_id`
* Avoid duplicate names OR use ID-based updates

---

# 🧠 System Architecture

```
User
  ↓
FastAPI
  ↓
Supervisor Agent
  ↓
 ┌───────────────────────┐
 │                       │
Inventory Agent      Analytics Agent
 │                       │
CRUD Tools         ML + Aggregation
 │                       │
MongoDB           Redis + ML Model
```

---

# 🚀 Future Improvements

* Vector search (RAG over inventory)
* Authentication & authorization
* Full Docker Compose setup
* Cloud deployment (AWS/GCP)
* Streaming responses
* Memory-enabled agents

---

# 💡 Resume Highlight

Built an AI-powered inventory system using FastAPI, MongoDB, Redis, and LangGraph multi-agent architecture with demand forecasting and a natural language interface powered by Gemini.

---

# 👩‍💻 Author

Suhani

```

If you want next-level polish (badges, architecture diagram image, demo GIF, GitHub stars section), say the word — I’ll upgrade this to a *seriously impressive* README 🚀
```
