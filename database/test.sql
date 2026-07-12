SELECT
    merchant_name,
    failure_reason,
    status
FROM transactions
WHERE status = 'FAILED';