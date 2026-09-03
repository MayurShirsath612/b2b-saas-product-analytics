# Creates and transforms all Silver layer tables from the Bronze layer tables.

#imports 
from logger import logging
import duckdb
from pathlib import Path
db_path = Path.cwd() / "product_analytics_light.duckdb"

#connection
con = duckdb.connect(str(db_path))
logging.info("Database Connection Successful.")
print("Database Connection Successful.")

try:
    # =================================================== #
        # creates silver__geography from bronze__geography
        # with transformations
        
    silver__geography = ("""
                CREATE OR REPLACE TABLE silver__geography AS
                WITH base AS (
                    SELECT
                        UPPER(TRIM(country_code)) AS country_code,
                        country_name,
                        region,
                        market,
                        currency,
                        sales_region
                    FROM bronze__geography
                ),
                deduped AS (
                    SELECT
                        *,
                        ROW_NUMBER() OVER (
                            PARTITION BY country_code
                            ORDER BY country_name
                        ) AS rn
                    FROM base
                )
                SELECT
                    country_code,
                    country_name,
                    region,
    
                    -- Fill a small known gap from the raw sheet
                    CASE
                        WHEN country_code = 'UK' AND market IS NULL THEN 'UK'
                        ELSE market
                    END AS market,
    
                    currency,
                    sales_region
    
                FROM deduped
                WHERE rn = 1;
                """)
    
    con.execute(silver__geography)
    print("silver geography table successfully created.")
    logging.info("Silver geography table successfully created.")



    # =================================================== #
    # creates silver__accounts from bronze__accounts
    # with transformations
    silver__accounts = ("""
        CREATE OR REPLACE TABLE silver__accounts AS
        SELECT
            a.account_id,

            -- Core descriptors
            TRIM(a.account_name)        AS account_name,
            UPPER(a.country_code)       AS country_code,
            a.industry,
            a.employee_band,
            UPPER(a.segment)            AS segment,
            UPPER(a.acquisition_channel) AS acquisition_channel,

            -- Geography attributes (account-level enrichment)
            g.country_name,
            g.region,
            g.market,
            g.sales_region,
            g.currency AS local_currency,

            -- Dates
            a.created_at,
            CAST(a.created_at AS DATE)  AS created_date,
            a.trial_start_date,
            a.trial_end_date,

            -- Age metrics
            CASE
                WHEN CAST(a.created_at AS DATE) > CURRENT_DATE THEN 0
                ELSE DATE_DIFF('day', CAST(a.created_at AS DATE), CURRENT_DATE)
            END AS account_age_days,

            CASE
                WHEN CAST(a.created_at AS DATE) > CURRENT_DATE THEN 'future'
                WHEN DATE_DIFF('day', CAST(a.created_at AS DATE), CURRENT_DATE) < 30 THEN '<30 days'
                WHEN DATE_DIFF('day', CAST(a.created_at AS DATE), CURRENT_DATE) < 90 THEN '30-89 days'
                WHEN DATE_DIFF('day', CAST(a.created_at AS DATE), CURRENT_DATE) < 180 THEN '90-179 days'
                ELSE '180+ days'
            END AS account_age_bucket,

            -- Trial metrics
            CASE
                WHEN a.trial_start_date IS NOT NULL AND a.trial_end_date IS NOT NULL
                    THEN DATE_DIFF('day', a.trial_start_date, a.trial_end_date)
                ELSE NULL
            END AS trial_length_days,

            -- Status and flags
            a.account_status,
            (a.account_status = 'active') AS is_active_account,
            (a.trial_start_date IS NOT NULL) AS has_trial

        FROM bronze__accounts a
        LEFT JOIN silver__geography g
            ON UPPER(a.country_code) = g.country_code;
        """)

    con.execute(silver__accounts)
    print("Silver Accounts table successfully created.")
    logging.info("Silver accounts table successfully created.")




    # =================================================== #
    # creates silver__deals from bronze__deals
    # with transformations
    silver__deals = ("""
        CREATE OR REPLACE TABLE silver__deals AS
        SELECT
            deal_id,
            account_id,
            owner_user_id,
            pipeline_id,
            current_stage_id,

            LOWER(status) AS status,

            created_at,
            CAST(created_at AS DATE) AS created_date,

            closed_at,
            CAST(closed_at AS DATE) AS closed_date,

            last_stage_changed_at,
            CAST(last_stage_changed_at AS DATE) AS last_stage_changed_date,

            amount,
            UPPER(currency) AS currency,
            UPPER(country_code) AS country_code,

            source_system,

            (closed_at IS NOT NULL) AS is_closed,

            CASE
                WHEN LOWER(status) IN ('won', 'closed_won') THEN TRUE
                ELSE FALSE
            END AS is_won,

            CASE
                WHEN closed_at IS NOT NULL THEN DATE_DIFF('day', CAST(created_at AS DATE), CAST(closed_at AS DATE))
                ELSE NULL
            END AS deal_cycle_days,

            CASE
                WHEN CAST(created_at AS DATE) > CURRENT_DATE THEN 0
                ELSE DATE_DIFF('day', CAST(created_at AS DATE), CURRENT_DATE)
            END AS deal_age_days

        FROM bronze__deals;
        """) 

    con.execute(silver__deals)
    print("silver deals table successfully created.")
    logging.info("Silver deals table successfully created.")


    


    # =================================================== #
    # creates silver__product_events from bronze__product_events
    # with transformations
    silver__product_events = ("""
        CREATE OR REPLACE TABLE silver__product_events AS
        WITH base AS (
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
                UPPER(country_code) AS country_code,
                event_properties,
                is_test_event,
                source_system
            FROM bronze__product_events
            WHERE is_test_event = FALSE
        ),
        enriched AS (
            SELECT
                *,
                
                CAST(event_timestamp AS DATE) AS event_ts_date,
                DATE_TRUNC('month', event_timestamp) AS event_ts_month,

                CASE
                    WHEN event_name ILIKE '%login%' THEN 'AUTH'
                    WHEN event_name ILIKE '%pipeline%' OR event_name ILIKE '%deal%' THEN 'PIPELINE'
                    WHEN event_name ILIKE '%activity%' OR event_name ILIKE '%call%' OR event_name ILIKE '%email%' THEN 'ACTIVITY'
                    WHEN event_name ILIKE '%workflow%' OR event_name ILIKE '%automation%' THEN 'AUTOMATION'
                    ELSE 'OTHER'
                END AS event_category,

                CASE
                    WHEN deal_id IS NOT NULL THEN TRUE
                    ELSE FALSE
                END AS has_deal_context

            FROM base
        )
        SELECT
            event_id,
            event_name,
            event_category,
            user_id,
            account_id,
            deal_id,
            has_deal_context,
            event_timestamp,
            event_ts_date,
            event_ts_month,
            ingested_at,
            event_date,
            platform,
            device_type,
            app_version,
            country_code,
            event_properties,
            source_system

        FROM enriched;
        """)

    con.execute(silver__product_events)
    print("silver product events table successfully created.")
    logging.info("Silver product events table successfully created.")




    # =================================================== #
    # creates silver__users from bronze__users
    # with transformations
        
    silver__users =("""
        CREATE OR REPLACE TABLE silver__users AS
        SELECT
            user_id,
            account_id,

            -- Core descriptors
            full_name,
            LOWER(SPLIT_PART(email, '@', 2)) AS email_domain,
            job_role,
            user_status,

            -- Dates
            created_at,
            CAST(created_at AS DATE) AS created_date,
            last_seen_at,

            -- Tenure & recency
            CASE
                WHEN CAST(created_at AS DATE) > CURRENT_DATE THEN 0
                ELSE DATE_DIFF('day', CAST(created_at AS DATE), CURRENT_DATE)
            END AS user_tenure_days,

            CASE
                WHEN last_seen_at IS NULL THEN NULL
                WHEN CAST(last_seen_at AS DATE) > CURRENT_DATE THEN 0
                ELSE DATE_DIFF('day', CAST(last_seen_at AS DATE), CURRENT_DATE)
            END AS days_since_last_seen,

            CASE
                WHEN last_seen_at IS NULL THEN 'never seen'
                WHEN DATE_DIFF('day', CAST(last_seen_at AS DATE), CURRENT_DATE) <= 7 THEN '0-7 days'
                WHEN DATE_DIFF('day', CAST(last_seen_at AS DATE), CURRENT_DATE) <= 30 THEN '8-30 days'
                WHEN DATE_DIFF('day', CAST(last_seen_at AS DATE), CURRENT_DATE) <= 90 THEN '31-90 days'
                ELSE '90+ days'
            END AS recency_bucket,

            -- Flags
            (user_status = 'active') AS is_active_user,
            is_admin

        FROM bronze__users;
        """)

    con.execute(silver__users)
    print("silver users table successfully created.")
    logging.info("Silver users table successfully created.")


    #closing the connection 
    con.close()
    print("Connection Closed Successfully.")
    logging.info("Connection Closed Successfully.")



# =========================
#checking for errors
except Exception as e:
 logging.error(f"Failed to create silver layer: {e}")
raise
 
