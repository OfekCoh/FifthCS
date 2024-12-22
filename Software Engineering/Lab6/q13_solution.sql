SELECT c.*, sub.OrderCount
FROM customers c
JOIN (
    SELECT o.CustomerID, COUNT(o.OrderID) AS OrderCount
    FROM orders o
    GROUP BY o.CustomerID
    ORDER BY OrderCount DESC
    LIMIT 1
) sub ON c.CustomerID = sub.CustomerID;
