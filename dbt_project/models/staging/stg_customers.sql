{{ config(materialized='view') }}

SELECT 
    customer_id,
    full_name,
    phone_number,
    email,
    age,
    gender,
    location,
    income_band,
    credit_score,
    created_at
FROM {{ source('mophones_credit', 'customers') }}