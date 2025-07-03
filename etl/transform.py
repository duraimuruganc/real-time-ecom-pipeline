"""
Transform helpers:
• Parse JSON lines
• Clean / enrich data
• Ensure timezone‑aware UTC datetimes, rounded to microseconds
"""

import json
import pandas as pd


def read_json_lines(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


# ---------- USERS ----------
def clean_users(path):
    df = pd.DataFrame(read_json_lines(path))

    
    df["created_at"] = (
        pd.to_datetime(df["created_at"], utc=True) 
          .dt.floor("us")                           
    )

    df["country"] = df["country"].str.upper()
    return df


# ---------- ORDERS ----------
def clean_orders(path):
    df = pd.DataFrame(read_json_lines(path))

    df["ts"] = (
        pd.to_datetime(df["ts"], utc=True)  
          .dt.floor("us")                   
    )

    df = df[df["qty"] > 0]
    df["amount"] = df["qty"] * df["unit_price"]
    return df
