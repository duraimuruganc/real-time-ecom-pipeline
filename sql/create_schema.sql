-- Warehouse & database (idempotent)
CREATE WAREHOUSE IF NOT EXISTS DEMO_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND   = 60;

CREATE DATABASE  IF NOT EXISTS ECOM_DB;
USE DATABASE ECOM_DB;

-- ---------- RAW STAGING TABLES ----------
CREATE OR REPLACE TABLE RAW_USERS_STAGE (
  USER_ID     STRING,
  CREATED_AT  TIMESTAMP_NTZ,      --   ▼ changed
  COUNTRY     STRING
);

CREATE OR REPLACE TABLE RAW_ORDERS_STAGE (
  ORDER_ID    STRING,
  TS          TIMESTAMP_NTZ,      --   ▼ changed
  USER_ID     STRING,
  SKU         STRING,
  QTY         INTEGER,
  UNIT_PRICE  NUMBER(10,2),
  AMOUNT      NUMBER(10,2)
);

-- ---------- STAR‑SCHEMA TABLES ----------
CREATE OR REPLACE TABLE DIM_CUSTOMERS (
  USER_ID     STRING PRIMARY KEY,
  COUNTRY     STRING,
  CREATED_AT  TIMESTAMP_NTZ       --   ▼ changed
);

CREATE OR REPLACE TABLE DIM_PRODUCTS (
  SKU         STRING PRIMARY KEY,
  UNIT_PRICE  NUMBER(10,2)
);

CREATE OR REPLACE TABLE FACT_ORDERS (
  ORDER_ID    STRING PRIMARY KEY,
  USER_ID     STRING,
  SKU         STRING,
  TS          TIMESTAMP_NTZ,      --   ▼ changed
  QTY         INTEGER,
  AMOUNT      NUMBER(10,2)
);