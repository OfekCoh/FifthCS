SELECT c.CustomerName
FROM Customers c      /* c is short for costumers */
JOIN Orders o ON c.CustomerID = o.CustomerID    /* o is short for orders */
/* join merges the rows together, on is the condition */ 
GROUP BY c.CustomerID, c.CustomerName
HAVING SUM(o.Quantity) > 0; 
