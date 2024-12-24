-- Create a temporary table to hold cleaned data
CREATE TABLE Temp_CustomerReviews2 (
    Name NVARCHAR(50),
    VerifiedReview BIT,
    Datetime DATETIME,
    OverallRating INT,
    SeatComfort INT,
    CabinStaffService INT,
    GroundService INT,
    ValueForMoney INT,
    Recommended BIT,
    TypeOfTraveller NVARCHAR(50),
    SeatType NVARCHAR(50),
    Route NVARCHAR(50)
);

-- Insert valid data into the temporary table, correcting or filtering invalid dates
INSERT INTO Temp_CustomerReviews2
SELECT 
    Name,
    VerifiedReview,
    CASE 
        WHEN ISDATE(Datetime) = 1 THEN Datetime 
        ELSE NULL  -- You can set to a default date if needed, like '1900-01-01'
    END AS Datetime,
    OverallRating,
    SeatComfort,
    CabinStaffService,
    GroundService,
    ValueForMoney,
    Recommended,
    TypeOfTraveller,
    SeatType,
    Route
FROM CustomerReviews2.dbo.CustomerReviews2;

-- Now proceed with your inserts, ensuring you use the temporary table

-- Insert into Dim_Customer
INSERT INTO Dim_Customer (Name, VerifiedReview)
SELECT DISTINCT Name, VerifiedReview
FROM Temp_CustomerReviews2
WHERE VerifiedReview IS NOT NULL;

-- Insert into Dim_TravellerType
INSERT INTO Dim_TravellerType (TypeOfTraveller)
SELECT DISTINCT TypeOfTraveller
FROM Temp_CustomerReviews2
WHERE TypeOfTraveller IS NOT NULL;

-- Insert into Dim_SeatType
INSERT INTO Dim_SeatType (SeatType)
SELECT DISTINCT SeatType
FROM Temp_CustomerReviews2
WHERE SeatType IS NOT NULL;

-- Insert into Dim_Route
INSERT INTO Dim_Route (Route)
SELECT DISTINCT Route
FROM Temp_CustomerReviews2
WHERE Route IS NOT NULL;

-- Insert into Dim_Time with distinct dates to avoid duplicates
INSERT INTO Dim_Time (DateKey, Date, Year, Month, DayOfWeek, DayOfMonth, Quarter)
SELECT DISTINCT 
    CAST(CONVERT(VARCHAR(8), Datetime, 112) AS INT) AS DateKey,  -- Format as YYYYMMDD
    Datetime,
    YEAR(Datetime) AS Year,
    MONTH(Datetime) AS Month,
    DATENAME(WEEKDAY, Datetime) AS DayOfWeek,
    DAY(Datetime) AS DayOfMonth,
    DATEPART(QUARTER, Datetime) AS Quarter
FROM Temp_CustomerReviews2
WHERE Datetime IS NOT NULL  -- Avoid inserting nulls
AND NOT EXISTS (
    SELECT 1 
    FROM Dim_Time t 
    WHERE t.DateKey = CAST(CONVERT(VARCHAR(8), Datetime, 112) AS INT)
);

-- Insert into Fact_Review
INSERT INTO Fact_Review (Datetime, OverallRating, SeatComfort, CabinStaffService, GroundService, ValueForMoney, Recommended, CustomerID, TravellerTypeID, SeatTypeID, RouteID, DateKey)
SELECT 
    cs.Datetime,
    cs.OverallRating,
    cs.SeatComfort,
    cs.CabinStaffService,
    cs.GroundService,
    cs.ValueForMoney,
    cs.Recommended,
    c.CustomerID,
    tt.TravellerTypeID,
    st.SeatTypeID,
    r.RouteID,
    CAST(CONVERT(VARCHAR(8), cs.Datetime, 112) AS INT) AS DateKey  -- Format as YYYYMMDD
FROM Temp_CustomerReviews2 cs
JOIN Dim_Customer c ON cs.Name = c.Name AND cs.VerifiedReview = c.VerifiedReview
JOIN Dim_TravellerType tt ON cs.TypeOfTraveller = tt.TypeOfTraveller
JOIN Dim_SeatType st ON cs.SeatType = st.SeatType
JOIN Dim_Route r ON cs.Route = r.Route
JOIN Dim_Time t ON CAST(CONVERT(VARCHAR(8), cs.Datetime, 112) AS INT) = t.DateKey  -- Format as YYYYMMDD
WHERE cs.Datetime IS NOT NULL;  -- Ensure Datetime is not null

-- Drop the temporary table after use
DROP TABLE Temp_CustomerReviews2;
