# Real‑Time E‑commerce Analytics Pipeline 🚀

A hands‑on demo that streams synthetic e‑commerce events, lands them locally, loads them into **Snowflake** with Python, and surfaces KPIs.  
Perfect for showcasing **Snowflake Streams + Tasks, Arrow‑based Python ETL, and (optional) Streamlit dashboards**—all on a tiny budget.

---

## ✨ Key Components

| Layer                  | Tech & Files                                     | Highlights |
|------------------------|--------------------------------------------------|------------|
| **Data Generator**     | `data_generation/generate_events.py`             | 1 msg/sec JSON (users & orders) |
| **Landing Zone**       | `landing/users/`, `landing/orders/` (local FS)   | Acts like a mini data lake; easy to swap for S3 |
| **ETL Loader**         | `etl/transform.py`, `etl/load_to_snowflake.py`   | Arrow upload, UTC session, microsecond precision |
| **Staging + CDC**      | `RAW_*_STAGE` + `RAW_*_STREAM`                   | Streams capture inserts for incremental merges |
| **Star‑Schema Tables** | `DIM_CUSTOMERS`, `FACT_ORDERS`                   | Filled via `ETL.MERGE_*` stored procs |
| **Orchestration**      | `TASK_MERGE_USERS`, `TASK_MERGE_ORDERS`          | Runs every minute *only when streams have data* |
| **Analytics Views**    | `VW_DAILY_REVENUE`, `VW_REPEAT_RATE`             | Daily revenue + repeat‑customer % |
| **Dashboard (optional)** | `dashboard/app.py` (Streamlit)                 | Minute‑level revenue trend + KPI tiles |

---

## 🗂️ Project Structure

```
real‑time‑ecom‑pipeline/
├─ data_generation/      # synthetic event producer
├─ etl/                  # config, transforms, loader
├─ sql/                  # DDL, streams, tasks, views
├─ landing/              # JSON sink (auto‑created)
├─ dashboard/            # optional Streamlit UI
├─ requirements.txt
└─ README.md
```

---

## 💸 Cost Cheat‑Sheet

| Item | Typical usage | $/month* |
|------|---------------|----------|
| Snowflake XS warehouse | 1 credit ≈ $2–$3, ~5 credits to demo | $10–$15 |
| Snowflake storage      | < 50 MB | < $1 |
| Streamlit, dbt Cloud   | Free tiers | $0 |

\*All within the $400 Snowflake free trial.

---

## ⚡ Quick Start

```bash
# 1. Clone & create virtual‑env
git clone <your‑fork>
cd real‑time‑ecom‑pipeline
python -m venv .venv && source .venv/bin/activate   # Windows: .\.venv\Scriptsctivate
pip install -r requirements.txt

# 2. Add .env with Snowflake creds
cp .env.example .env  # or create manually; see below

# 3. Bootstrap schema & tasks
snowsql -f sql/create_schema.sql
snowsql -f sql/create_tasks.sql

# 4. Start pipeline
python data_generation/generate_events.py      # ⏩ terminal 1
python etl/load_to_snowflake.py                # ⏩ terminal 2

# 5. (Optional) dashboard
streamlit run dashboard/app.py
```

`.env` example:

```env
SNOWFLAKE_USER=YOUR_USER
SNOWFLAKE_PASSWORD=YOUR_PASSWORD
SNOWFLAKE_ACCOUNT=abcd-qn12345
SNOWFLAKE_WAREHOUSE=DEMO_WH
SNOWFLAKE_DATABASE=ECOM_DB
SNOWFLAKE_SCHEMA=PUBLIC
```

---

## 🐾 Verify It Works

```sql
-- New rows?
SELECT COUNT(*) FROM RAW_ORDERS_STAGE;

-- Revenue trend (last 60 minutes, minute grain)
SELECT DATE_TRUNC('minute', TS) AS MIN, SUM(AMOUNT)
FROM   FACT_ORDERS
WHERE  TS >= DATEADD(minute, -60, CURRENT_TIMESTAMP)
GROUP  BY 1 ORDER  BY 1;
```

---

---

## 📝 License

MIT — use, fork, and improve!
