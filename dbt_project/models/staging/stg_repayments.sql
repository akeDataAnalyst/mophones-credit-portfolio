{{ config(materialized='view') }}

SELECT 
    repayment_id,
    loan_id,
    due_date,
    paid_date,
    amount_due,
    amount_paid,
    days_late,
    CASE 
        WHEN days_late >= 90 THEN '90+'
        WHEN days_late >= 60 THEN '60-89'
        WHEN days_late >= 30 THEN '30-59'
        ELSE 'Current'
    END as delinquency_bucket
FROM {{ source('mophones_credit', 'repayments') }}