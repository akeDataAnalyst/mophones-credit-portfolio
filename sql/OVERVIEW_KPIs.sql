SELECT 
    COUNT(DISTINCT customer_id) as total_customers,
    COUNT(loan_id) as total_loans,
    ROUND(SUM(principal), 0) as total_disbursed,
    ROUND(AVG(principal), 0) as avg_loan_size,
    ROUND(AVG(term_months), 1) as avg_term_months,
    COUNT(CASE WHEN promo_applied = 1 THEN 1 END) as promo_loans,
    ROUND(COUNT(CASE WHEN promo_applied = 1 THEN 1 END) * 100.0 / COUNT(*), 1) as promo_pct
FROM loans;