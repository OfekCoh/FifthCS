SELECT o.CustomerID, c.CustomerName, o.ProductID, p.ProductName, COUNT(o.OrderID) AS OrderCount
FROM orders o
JOIN customers c ON o.CustomerID = c.CustomerID
JOIN products p ON o.ProductID = p.ProductID
GROUP BY o.CustomerID, o.ProductID
HAVING COUNT(o.OrderID) >= 2;
