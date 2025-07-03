"""
Batch loader:
• Scans landing/users & landing/orders once per minute
• Cleans data with pandas (see transform.py)
• Uploads to Snowflake RAW_*_STAGE via Arrow
• Calls stored procs to MERGE into fact/dim tables
Run:  python etl/load_to_snowflake.py
"""

import time, glob
from pathlib import Path

import pandas as pd
import snowflake.connector as sf
from snowflake.connector.pandas_tools import write_pandas

from transform import clean_users, clean_orders
from config import SNOWFLAKE, LANDING_DIR


# ---------- Connection helper ----------
def get_conn():
    
    return sf.connect(insecure_mode=True,**SNOWFLAKE)


# ---------- Upload helper ----------
def copy_df(conn, df: pd.DataFrame, table: str):
   
    result = write_pandas(
        conn,
        df,
        table_name=table,
        quote_identifiers=False,
        use_logical_type=True,  # <- important for tz‑aware datetimes
    )
    # Connector <3.6 -> tuple ; 3.6+ -> WriteResult object
    success = result[0] if isinstance(result, tuple) else result.success
    if not success:
        raise RuntimeError(f"write_pandas failed for {table}")


# ---------- Main ingest cycle ----------
def process_once():
    conn = get_conn()
    cur = conn.cursor()
    try:
        # ----- USERS -----
        for path in glob.glob(str(LANDING_DIR / "users" / "*.json")):
            df = clean_users(path)
            copy_df(conn, df, "RAW_USERS_STAGE")
            Path(path).unlink()  # remove after load

        # ----- ORDERS -----
        for path in glob.glob(str(LANDING_DIR / "orders" / "*.json")):
            df = clean_orders(path)
            copy_df(conn, df, "RAW_ORDERS_STAGE")
            Path(path).unlink()

        # ----- Merge stored procs -----
        cur.execute("CALL ETL.MERGE_USERS();")
        cur.execute("CALL ETL.MERGE_ORDERS();")

    finally:
        cur.close()
        conn.close()


# ---------- Daemon loop ----------
if __name__ == "__main__":
    while True:
        process_once()
        time.sleep(60)  # wait 1 minute
