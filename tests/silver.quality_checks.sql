
-- ============================================================
-- DATA QUALITY CHECKS - SILVER LAYER
-- ============================================================
use product_analytics_light;

-- 1. Duplicate accounts
SELECT
    account_id,
    COUNT(*) AS duplicate_count
FROM silver__accounts
GROUP BY account_id
HAVING COUNT(*) > 1;


-- 2. Duplicate users
SELECT
    user_id,
    COUNT(*) AS duplicate_count
FROM silver__users
GROUP BY user_id
HAVING COUNT(*) > 1;


-- 3. Duplicate deals
SELECT
    deal_id,
    COUNT(*) AS duplicate_count
FROM silver__deals
GROUP BY deal_id
HAVING COUNT(*) > 1;


-- 4. Users without a valid account
SELECT
    u.user_id,
    u.account_id
FROM silver__users u
LEFT JOIN silver__accounts a
    ON u.account_id = a.account_id
WHERE a.account_id IS NULL;


-- 5. Deals without a valid account
SELECT
    d.deal_id,
    d.account_id
FROM silver__deals d
LEFT JOIN silver__accounts a
    ON d.account_id = a.account_id
WHERE d.account_id IS NOT NULL
  AND a.account_id IS NULL;


-- 6. Product events without a valid user
SELECT
    e.event_id,
    e.user_id
FROM silver__product_events e
LEFT JOIN silver__users u
    ON e.user_id = u.user_id
WHERE e.user_id IS NOT NULL
  AND u.user_id IS NULL;


-- 7. Invalid account dates
SELECT
    account_id,
    created_date,
    trial_start_date,
    trial_end_date
FROM silver__accounts
WHERE trial_start_date < created_date
   OR trial_end_date < trial_start_date;


-- 8. Invalid deal dates / negative deal cycle
SELECT
    deal_id,
    created_date,
    closed_date,
    deal_cycle_days
FROM silver__deals
WHERE closed_date < created_date
   OR deal_cycle_days < 0;


-- 9. Negative deal amounts
SELECT
    deal_id,
    account_id,
    amount,
    currency
FROM silver__deals
WHERE amount < 0;


-- 10. Won deals that are not closed
SELECT
    deal_id,
    status,
    is_closed,
    is_won
FROM silver__deals
WHERE is_won = TRUE
  AND is_closed = FALSE;
