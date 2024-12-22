SELECT c.CustomerName, p.ProductName, o.OrderDate
FROM orders o
JOIN customers c ON o.CustomerID = c.CustomerID
JOIN products p ON o.ProductID = p.ProductID
WHERE YEAR(o.OrderDate) = 2024;
