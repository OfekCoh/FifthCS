SELECT 
    cu.City, 
    COUNT(DISTINCT cu.CustomerID) AS CustomerCount, 
    COUNT(DISTINCT s.SupplierID) AS SupplierCount
FROM 
    customers cu
LEFT JOIN 
    suppliers s ON cu.City = s.City
GROUP BY 
    cu.City
ORDER BY 
    cu.City;
