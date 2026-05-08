{{ config(materialized='view') }}

WITH loan_repayment_summary AS (
    SELECT 
        l.loan_id,
        l.customer_id,
        l.disbursed_date,
        l.principal,
        l.term_months,
        l.device_model,
        l.promo_applied,
        MAX(r.due_date) as latest_due_date,
        SUM(r.amount_due) as total_due,
        SUM(r.amount_paid) as total_paid,
        MAX(r.days_late) as max_days_late,
        COUNT(CASE WHEN r.days_late >= 30 THEN 1 END) as times_30plus_dpd
    FROM {{ ref('stg_loans') }} l
    LEFT JOIN {{ ref('stg_repayments') }} r ON l.loan_id = r.loan_id
    GROUP BY l.loan_id, l.customer_id, l.disbursed_date, l.principal, 
             l.term_months, l.device_model, l.promo_applied
)
SELECT *,
       CASE 
           WHEN max_days_late >= 90 THEN '90+'
           WHEN max_days_late >= 60 THEN '60-89'
           WHEN max_days_late >= 30 THEN '30-59'
           ELSE 'Performing'
       END as current_status
FROM loan_repayment_summary