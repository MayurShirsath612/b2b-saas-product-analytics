# Script Purpose :  Creates and populates all Bronze layer tables from the raw data sources.


#imports
from logger import logging
import duckdb
import pandas as pd
from pathlib import Path
db_path = Path.cwd() / "product_analytics_light.duckdb"

try:
    #connection 
    con = duckdb.connect(str(db_path))
    logging.info("Database Connection Successful.")


    # ====================================================================#
    #Creates and populates the bronze__accounts table
    #from the raw__accounts table.
    bronze__accounts = """
        CREATE OR REPLACE TABLE bronze__accounts AS
        SELECT
            account_id,
            account_name,
            country_code,
            city,
            industry,
            employee_band,
            segment,
            created_at,
            trial_start_date,
            trial_end_date,
            account_status,
            acquisition_channel
        FROM raw__accounts;
        """

    con.execute(bronze__accounts)
    print("Bronze Accounts table successfully created.")
    logging.info("Bronze accounts table successfully created.")


    # ====================================================================#

    #Creates and populates the bronze__deals table
    #from the raw__deals table.
    bronze__deals = """
        CREATE OR REPLACE TABLE bronze__deals AS
        SELECT
        deal_id,
        account_id,
        owner_user_id,
        pipeline_id,
        current_stage_id,
        status,
        created_at,
        closed_at,
        last_stage_changed_at,
        amount,
        currency,
        country_code,
        source_system
        FROM raw__deals;
        """

    con.execute(bronze__deals)
    print("Bronze deals table successfully created.")
    logging.info("Bronze deals table successfully created.")


    # ====================================================================#
    #Creates and populates the bronze__geography table
    #from the raw__geography.xlsx file.
    excel_path = Path.cwd() /"raw__geography.xlsx"
    df_geography = pd.read_excel(excel_path)

        
    con.register("df_geography_temp", df_geography)

    bronze__geography = """
        CREATE OR REPLACE TABLE bronze__geography AS
        SELECT *
        FROM df_geography_temp;
        """
    

    con.execute(bronze__geography)
    print("Bronze Geography table successfully created from Excel.")
    logging.info("Bronze geography table successfully created")


    # ====================================================================#
    # Creates and populates the bronze__product_events table
    # from the raw__product_events table.
    bronze__product_events = """
        CREATE OR REPLACE TABLE bronze__product_events AS
        SELECT
        event_id,
        event_name,
        user_id,
        account_id,
        deal_id,
        event_timestamp,
        ingested_at,
        event_date,
        platform,
        device_type,
        app_version,
        country_code,
        event_properties,
        is_test_event,
        source_system
        FROM raw__product_events
        """

    con.execute(bronze__product_events)
    print("Bronze product events table successfully created.")
    logging.info("Bronze product events table successfully created.")


    # ====================================================================#
    # Creates and populates the bronze__users table
    # from the raw__users table.
    bronze__users = """
        CREATE OR REPLACE TABLE bronze__users AS
        SELECT
        user_id,
        account_id,
        full_name,
        email,
        job_role,
        user_status,
        created_at,
        last_seen_at,
        timezone,
        locale,
        is_admin
        FROM raw__users;
        
        """

    con.execute(bronze__users)
    print("Bronze users table successfully created.")
    logging.info("Bronze users table successfully created.")



    # ============================================
    #closing the connection
    con.close()
    logging.info("Connection Closed Successfully.")


# =========================
#checking for errors
except Exception as e:
    logging.error(f"Failed to create bronze layer: {e}")
    raise
 
