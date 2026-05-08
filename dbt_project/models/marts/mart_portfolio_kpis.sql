{{ config(materialized='table') }}

SELECT 
    COUNT(DISTINCT customer_id) as total_customers,
    COUNT(loan_id) as total_loans,
    ROUND(SUM(principal), 0) as total_disbursed,
    ROUND(AVG(principal), 0) as avg_loan_size,
    ROUND(SUM(CASE WHEN promo_applied = TRUE THEN principal ELSE 0 END) * 100.0 / SUM(principal), 2) as promo_disbursed_pct,

    -- Delinquency KPIs
    ROUND(100.0 * SUM(CASE WHEN max_days_late >= 30 THEN principal ELSE 0 END) / SUM(principal), 2) as PAR30,
    ROUND(100.0 * SUM(CASE WHEN max_days_late >= 60 THEN principal ELSE 0 END) / SUM(principal), 2) as PAR60,
    ROUND(100.0 * SUM(CASE WHEN max_days_late >= 90 THEN principal ELSE 0 END) / SUM(principal), 2) as PAR90
FROM {{ ref('int_loans_repayments') }}