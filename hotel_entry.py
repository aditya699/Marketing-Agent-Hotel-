import streamlit as st
import pyodbc
from datetime import date

# Database connection function
def create_connection():
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                          'Server=DESKTOP-KLL45AE\SQLEXPRESS;'
                          'Database=ADITYADB;'
                          'Trusted_Connection=yes;')
    return conn

# Streamlit app
def main():
    st.title("Hotel Reservation Data Entry")

    # Form inputs
    guest_name = st.text_input("Guest Name")
    room_number = st.number_input("Room Number", min_value=1, max_value=1000, step=1)
    check_in_date = st.date_input("Check-in Date", min_value=date.today())
    check_out_date = st.date_input("Check-out Date", min_value=check_in_date)
    number_of_guests = st.number_input("Number of Guests", min_value=1, max_value=10, step=1)
    reservation_status = st.selectbox("Reservation Status", ["Confirmed", "Pending"])
    total_amount = st.number_input("Total Amount", min_value=0.0, step=0.01)
    phone_number = st.text_input("Phone Number")
    email = st.text_input("Email")
    special_requests = st.text_area("Special Requests")

    if st.button("Submit Reservation"):
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO HotelReservation (GuestName, RoomNumber, CheckInDate, CheckOutDate, NumberOfGuests,
                                      ReservationStatus, TotalAmount, PhoneNumber, Email, SpecialRequests)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (guest_name, room_number, check_in_date, check_out_date, number_of_guests,
              reservation_status, total_amount, phone_number, email, special_requests))
        conn.commit()
        conn.close()
        st.success("Reservation added successfully!")

if __name__ == "__main__":
    main()