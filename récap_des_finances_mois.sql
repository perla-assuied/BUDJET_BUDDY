USE banque;
SELECT 
    YEAR(date_transaction) AS annee,
    MONTH(date_transaction) AS mois,
    SUM(CASE WHEN type_transaction = 'depot' THEN montant ELSE 0 END) AS total_revenus,
    SUM(CASE WHEN type_transaction = 'retrait' THEN montant ELSE 0 END) AS total_depenses
FROM transactions
WHERE utilisateur_id = 1
GROUP BY YEAR(date_transaction), MONTH(date_transaction)
ORDER BY annee DESC, mois DESC;
