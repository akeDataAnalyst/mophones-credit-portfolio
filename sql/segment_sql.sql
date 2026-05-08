SELECT 
    location,
    income_band,
    COUNT(DISTINCT l.loan_id) as loans,
    ROUND(AVG(CASE WHEN r.days_late >= 30 THEN 1 ELSE 0 END)*100, 2) as par30_rate,
    ROUND(SUM(l.principal), 0) as disbursed
FROM loans l
JOIN customers c ON l.customer_id = c.customer_id
JOIN repayments r ON l.loan_id = r.loan_id
GROUP BY location, income_band
ORDER BY par30_rate DESC;