SELECT p.ProductName
FROM Products p      /* p is short for Products */
JOIN Orders o ON p.ProductID = o.ProductID    /* o is short for orders */
/* join merges the rows together, on is the condition */ 
GROUP BY p.ProductID, p.ProductName
HAVING SUM(o.Quantity) > 4; 
