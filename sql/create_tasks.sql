/* ---------- create_tasks.sql (fixed) ---------- */
USE DATABASE ECOM_DB;
USE SCHEMA PUBLIC;

CREATE SCHEMA IF NOT EXISTS ETL;

/* Streams */
CREATE OR REPLACE STREAM RAW_USERS_STREAM
  ON TABLE PUBLIC.RAW_USERS_STAGE
  APPEND_ONLY = TRUE;

CREATE OR REPLACE STREAM RAW_ORDERS_STREAM
  ON TABLE PUBLIC.RAW_ORDERS_STAGE
  APPEND_ONLY = TRUE;

/* Stored procedures */
CREATE OR REPLACE PROCEDURE ETL.MERGE_USERS()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN
  MERGE INTO PUBLIC.DIM_CUSTOMERS tgt
  USING PUBLIC.RAW_USERS_STREAM src
  ON tgt.USER_ID = src.USER_ID
  WHEN NOT MATCHED THEN
    INSERT (USER_ID, COUNTRY, CREATED_AT)
    VALUES (src.USER_ID, src.COUNTRY, src.CREATED_AT);

  RETURN 'DIM_CUSTOMERS MERGED';
END;
$$;

CREATE OR REPLACE PROCEDURE ETL.MERGE_ORDERS()
RETURNS STRING
LANGUAGE SQL
EXECUTE AS CALLER
AS
$$
BEGIN
  MERGE INTO PUBLIC.FACT_ORDERS tgt
  USING PUBLIC.RAW_ORDERS_STREAM src
  ON tgt.ORDER_ID = src.ORDER_ID
  WHEN NOT MATCHED THEN
    INSERT (ORDER_ID, USER_ID, SKU, TS, QTY, AMOUNT)
    VALUES (src.ORDER_ID, src.USER_ID, src.SKU, src.TS, src.QTY, src.AMOUNT);

  RETURN 'FACT_ORDERS MERGED';
END;
$$;

/* Tasks */
CREATE OR REPLACE TASK TASK_MERGE_USERS
  WAREHOUSE = DEMO_WH
  SCHEDULE  = '1 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('PUBLIC.RAW_USERS_STREAM')
AS
CALL ETL.MERGE_USERS();

CREATE OR REPLACE TASK TASK_MERGE_ORDERS
  WAREHOUSE = DEMO_WH
  SCHEDULE  = '1 MINUTE'
  WHEN SYSTEM$STREAM_HAS_DATA('PUBLIC.RAW_ORDERS_STREAM')
AS
CALL ETL.MERGE_ORDERS();
