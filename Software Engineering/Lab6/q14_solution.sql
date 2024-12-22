SELECT DISTINCT s.SupplierName
FROM suppliers s
JOIN products p ON s.SupplierID = p.SupplierID
WHERE p.Price > 1000;
