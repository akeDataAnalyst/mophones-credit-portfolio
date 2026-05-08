WITH latest_status AS (
    SELECT 
        l.loan_id,
        l.principal,
        l.disbursed_date,
        MAX(r.due_date) as latest_due_date,
        SUM(CASE WHEN r.days_late >= 30 THEN r.amount_due ELSE 0 END) as overdue_30,
        SUM(CASE WHEN r.days_late >= 60 THEN r.amount_due ELSE 0 END) as overdue_60,
        SUM(CASE WHEN r.days_late >= 90 THEN r.amount_due ELSE 0 END) as overdue_90
    FROM loans l
    JOIN repayments r ON l.loan_id = r.loan_id
    GROUP BY l.loan_id, l.principal, l.disbursed_date
)
SELECT 
    COUNT(loan_id) as total_loans_analyzed,
    ROUND(SUM(CASE WHEN overdue_30 > 0 THEN principal ELSE 0 END) * 100.0 / SUM(principal), 2) as par30_pct,
    ROUND(SUM(CASE WHEN overdue_60 > 0 THEN principal ELSE 0 END) * 100.0 / SUM(principal), 2) as par60_pct,
    ROUND(SUM(CASE WHEN overdue_90 > 0 THEN principal ELSE 0 END) * 100.0 / SUM(principal), 2) as par90_pct
FROM latest_status;