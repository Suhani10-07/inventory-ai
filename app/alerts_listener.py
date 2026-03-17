import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

pubsub = r.pubsub()
pubsub.subscribe("low_stock_channel")

print("Listening for low stock alerts...")

for message in pubsub.listen():
    if message["type"] == "message":
        print("🚨 ALERT:", message["data"])