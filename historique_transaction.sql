USE banque;
SELECT * FROM transactions
WHERE utilisateur_id = 1
AND date_transaction BETWEEN '2025-03-01' AND '2025-03-18'
ORDER BY montant DESC;
