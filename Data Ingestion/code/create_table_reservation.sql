CREATE TABLE HotelReservation (
    ReservationID INT PRIMARY KEY IDENTITY(1,1),
    GuestName NVARCHAR(100) NOT NULL,
    RoomNumber INT NOT NULL,
    CheckInDate DATE NOT NULL,
    CheckOutDate DATE NOT NULL,
    NumberOfGuests INT NOT NULL,
    ReservationStatus NVARCHAR(20) NOT NULL,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    PhoneNumber NVARCHAR(20),
    Email NVARCHAR(100),
    SpecialRequests NVARCHAR(MAX),
    CreatedAt DATETIME DEFAULT GETDATE(),
    UpdatedAt DATETIME DEFAULT GETDATE()
);