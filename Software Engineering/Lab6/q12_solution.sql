SELECT c.CustomerName, SUM(o.Quantity) AS TotalQuantity
FROM orders o
JOIN customers c ON o.CustomerID = c.CustomerID
GROUP BY c.CustomerName
ORDER BY TotalQuantity DESC;
