{{ config(materialized='view') }}

SELECT 
    loan_id,
    customer_id,
    disbursed_date,
    principal,
    term_months,
    interest_rate,
    device_model,
    promo_applied
FROM {{ source('mophones_credit', 'loans') }}