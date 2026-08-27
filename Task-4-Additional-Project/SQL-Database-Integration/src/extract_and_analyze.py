from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "travel_bookings.db"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

BOOKING_LEVEL_QUERY = """
SELECT
    b.booking_id,
    date(b.booking_date) AS booking_date,
    u.user_id,
    u.full_name,
    u.city AS customer_city,
    u.segment,
    p.property_name,
    p.destination,
    p.property_type,
    b.nights,
    b.status,
    b.total_amount
FROM bookings b
JOIN users u ON b.user_id = u.user_id
JOIN properties p ON b.property_id = p.property_id
WHERE b.status != 'Cancelled';
"""

DESTINATION_QUERY = """
SELECT
    p.destination,
    COUNT(*) AS booking_count,
    SUM(b.total_amount) AS revenue,
    ROUND(AVG(b.total_amount), 2) AS avg_booking_value
FROM bookings b
JOIN properties p ON b.property_id = p.property_id
WHERE b.status != 'Cancelled'
GROUP BY p.destination
ORDER BY revenue DESC;
"""


def main():
    if not DB_PATH.exists():
        raise FileNotFoundError("Database not found. Run: python src/setup_database.py")

    with sqlite3.connect(DB_PATH) as conn:
        bookings = pd.read_sql_query(BOOKING_LEVEL_QUERY, conn, parse_dates=["booking_date"])
        destination = pd.read_sql_query(DESTINATION_QUERY, conn)

    bookings["revenue_per_night"] = bookings["total_amount"] / bookings["nights"]
    bookings["booking_month"] = bookings["booking_date"].dt.to_period("M").astype(str)

    bookings.to_csv(OUTPUT_DIR / "booking_level_dataset.csv", index=False)
    destination.to_csv(OUTPUT_DIR / "destination_performance.csv", index=False)

    print("Booking-level dataset shape:", bookings.shape)
    print("\nDestination performance:\n", destination.to_string(index=False))
    print("\nPandas validation — revenue by destination:")
    print(bookings.groupby("destination")["total_amount"].sum().sort_values(ascending=False))


if __name__ == "__main__":
    main()
