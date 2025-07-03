import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE = dict(
    user      = os.getenv("SNOWFLAKE_USER"),
    password  = os.getenv("SNOWFLAKE_PASSWORD"),
    account   = os.getenv("SNOWFLAKE_ACCOUNT"),
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "DEMO_WH"),
    database  = os.getenv("SNOWFLAKE_DATABASE",  "ECOM_DB"),
    schema    = os.getenv("SNOWFLAKE_SCHEMA",    "RAW"),
    timezone  = "UTC",
)

LANDING_DIR = Path(__file__).resolve().parents[1] / "landing"
