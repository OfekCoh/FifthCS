SELECT Suppliers.SupplierName, COUNT(Products.ProductID) AS ProductCount
FROM Suppliers
JOIN Products ON Suppliers.SupplierID = Products.SupplierID
GROUP BY Suppliers.SupplierName;
