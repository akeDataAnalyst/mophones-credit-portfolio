SELECT 
    DATE_FORMAT(disburse_month, '%%Y-%%m') as vintage_month,
    COUNT(loan_id) as loans,
    ROUND(SUM(principal), 0) as disbursed,
    ROUND(AVG(CASE WHEN days_late >= 30 THEN 1 ELSE 0 END) * 100, 2) as cum_par30,
    ROUND(AVG(CASE WHEN days_late >= 60 THEN 1 ELSE 0 END) * 100, 2) as cum_par60
FROM (
    SELECT 
        l.loan_id,
        l.principal,                                   -- Added this
        DATE_FORMAT(l.disbursed_date, '%%Y-%%m-01') as disburse_month,
        MAX(r.days_late) as days_late
    FROM loans l
    JOIN repayments r ON l.loan_id = r.loan_id
    GROUP BY l.loan_id, l.principal, disburse_month
) v
GROUP BY vintage_month
ORDER BY vintage_month;