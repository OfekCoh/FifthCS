SELECT DISTINCT p.ProductName
FROM products p
JOIN suppliers s ON p.SupplierID = s.SupplierID
WHERE s.SupplierName LIKE '%s%';
