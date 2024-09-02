DECLARE @i INT = 1;
WHILE @i <= 100
BEGIN
    INSERT INTO HotelReservation (
        GuestName, RoomNumber, CheckInDate, CheckOutDate, NumberOfGuests,
        ReservationStatus, TotalAmount, PhoneNumber, Email, SpecialRequests
    )
    VALUES (
        'Guest ' + CAST(@i AS NVARCHAR(10)),
        FLOOR(RAND()*(500-100+1))+100,
        DATEADD(DAY, ABS(CHECKSUM(NEWID()) % 365), GETDATE()),
        DATEADD(DAY, ABS(CHECKSUM(NEWID()) % 7) + 1, DATEADD(DAY, ABS(CHECKSUM(NEWID()) % 365), GETDATE())),
        FLOOR(RAND()*(5-1+1))+1,
        CASE WHEN RAND() > 0.5 THEN 'Confirmed' ELSE 'Pending' END,
        ROUND(RAND() * (1000 - 100) + 100, 2),
        '555-' + CAST(FLOOR(RAND()*(999-100+1))+100 AS NVARCHAR(3)) + '-' + CAST(FLOOR(RAND()*(9999-1000+1))+1000 AS NVARCHAR(4)),
        'guest' + CAST(@i AS NVARCHAR(10)) + '@example.com',
        CASE WHEN RAND() > 0.7 THEN 'No special requests' ELSE 'Special request ' + CAST(@i AS NVARCHAR(10)) END
    );
    SET @i = @i + 1;
END