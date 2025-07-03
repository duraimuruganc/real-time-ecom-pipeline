""" Continuously generates synthetic e‑commerce events. """
import json, os, random, time, uuid
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1] / "landing"
ORDERS_DIR = BASE_DIR / "orders"
USERS_DIR  = BASE_DIR / "users"
ORDERS_DIR.mkdir(parents=True, exist_ok=True)
USERS_DIR.mkdir(parents=True, exist_ok=True)

PRODUCTS = [("SKU‑101", 15.99), ("SKU‑102", 23.49), ("SKU‑103", 8.50)]
COUNTRIES = ["IN", "US", "DE", "UK", "FR"]

def gen_user():
    return {
        "user_id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        "country": random.choice(COUNTRIES)
    }

def gen_order(user_id):
    sku, price = random.choice(PRODUCTS)
    qty = random.randint(1, 5)
    return {
        "order_id": str(uuid.uuid4()),
        "ts": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "sku": sku,
        "qty": qty,
        "unit_price": price
    }

def write_json(obj, path):
    with open(path, "a") as f:
        f.write(json.dumps(obj) + "\n")

def main():
    users = [gen_user() for _ in range(50)]
    for u in users:
        write_json(u, USERS_DIR / f"{datetime.utcnow():%Y%m%d%H}.json")
    print("Seeded 50 users")

    try:
        while True:
            order = gen_order(random.choice(users)["user_id"])
            write_json(order, ORDERS_DIR / f"{datetime.utcnow():%Y%m%d%H}.json")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped generator")

if __name__ == "__main__":
    main()
