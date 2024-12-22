SELECT Suppliers.SupplierName, Products.ProductName FROM Suppliers
JOIN Products ON Suppliers.SupplierID = Products.SupplierID
ORDER BY Suppliers.SupplierName ASC, Products.ProductName ASC;
