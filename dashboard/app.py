
import streamlit as st
import snowflake.connector as sf
import pandas as pd
import sys
from pathlib import Path

# --- make project‑root importable ---
sys.path.append(str(Path(__file__).resolve().parents[1]))

from etl.config import SNOWFLAKE


@st.cache_resource(ttl=300)
def get_conn():
    return sf.connect(insecure_mode=True,**SNOWFLAKE)


def query_df(sql: str) -> pd.DataFrame:
    cur = get_conn().cursor()
    try:
        cur.execute(sql)
        return cur.fetch_pandas_all()
    finally:
        cur.close()


st.set_page_config(page_title="Real‑Time E‑commerce KPIs", layout="wide")
st.title("📊 Real‑Time E‑commerce KPIs")

# ---------- Revenue trend (hourly, last 24 h) ----------
df_rev = query_df("""
    SELECT DATE_TRUNC('hour', TS) AS HOUR,
           SUM(AMOUNT)           AS REVENUE
    FROM   FACT_ORDERS
    WHERE  TS >= DATEADD(hour, -24, CURRENT_TIMESTAMP)
    GROUP  BY 1
    ORDER  BY 1
""")
df_rev["HOUR"] = pd.to_datetime(df_rev["HOUR"])
df_rev.set_index("HOUR", inplace=True)
st.line_chart(df_rev, height=300)

# ---------- Repeat‑customer metric ----------
df_repeat = query_df("SELECT REPEAT_PCT FROM VW_REPEAT_RATE")
st.metric("Repeat customer %", f"{float(df_repeat['REPEAT_PCT'][0]):.2f} %")
