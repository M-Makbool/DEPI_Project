USE CustomerFeedbackDW;
 
-- Normalized Customer Dimension
CREATE TABLE Dim_Customer (
    CustomerID INT PRIMARY KEY IDENTITY(1,1),
    Name NVARCHAR(50),
    VerifiedReview BIT
);
 
-- Separate Traveler Type Dimension
CREATE TABLE Dim_TravellerType (
    TravellerTypeID INT PRIMARY KEY IDENTITY(1,1),
    TypeOfTraveller NVARCHAR(50)
);
 
-- Separate Seat Type Dimension
CREATE TABLE Dim_SeatType (
    SeatTypeID INT PRIMARY KEY IDENTITY(1,1),
    SeatType NVARCHAR(50)
);
 
-- Route Dimension
CREATE TABLE Dim_Route (
    RouteID INT PRIMARY KEY IDENTITY(1,1),
    Route NVARCHAR(50),
);
 
-- Time Dimension
CREATE TABLE Dim_Time (
    DateKey INT PRIMARY KEY,
    Date DATE,
    Year INT,
    Month INT,
    DayOfWeek NVARCHAR(50),
	DayOfMonth INT,
    Quarter INT
);
 
-- Fact Review Table with indexes on foreign keys
CREATE TABLE Fact_Review (
    ReviewID INT PRIMARY KEY IDENTITY(1,1),
    Datetime DATETIME,
    OverallRating INT,
    SeatComfort INT,
    CabinStaffService INT,
    GroundService INT,
    ValueForMoney INT,
    Recommended BIT,
    CustomerID INT,
    TravellerTypeID INT,
    SeatTypeID INT,
    RouteID INT,
    DateKey INT,
    FOREIGN KEY (CustomerID) REFERENCES Dim_Customer(CustomerID),
    FOREIGN KEY (TravellerTypeID) REFERENCES Dim_TravellerType(TravellerTypeID),
    FOREIGN KEY (SeatTypeID) REFERENCES Dim_SeatType(SeatTypeID),
    FOREIGN KEY (RouteID) REFERENCES Dim_Route(RouteID),
    FOREIGN KEY (DateKey) REFERENCES Dim_Time(DateKey)
);
 
 
-- Adding indexes to foreign key columns for faster querying
CREATE INDEX idx_FactReview_CustomerID ON Fact_Review(CustomerID);
CREATE INDEX idx_FactReview_TravellerTypeID ON Fact_Review(TravellerTypeID);
CREATE INDEX idx_FactReview_SeatTypeID ON Fact_Review(SeatTypeID);
CREATE INDEX idx_FactReview_RouteID ON Fact_Review(RouteID);
CREATE INDEX idx_FactReview_DateKey ON Fact_Review(DateKey);
