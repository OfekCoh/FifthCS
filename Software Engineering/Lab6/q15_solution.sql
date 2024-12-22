SELECT 
    cu.City, 
    COUNT(DISTINCT cu.CustomerID) AS NumberOfCustomers, 
    COUNT(DISTINCT s.SupplierID) AS NumberOfSuppliers
FROM 
    customers cu
LEFT JOIN 
    suppliers s ON cu.City = s.City
GROUP BY 
    cu.City
ORDER BY 
    cu.City;
