from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "data" / "travel_bookings.db"
rng = np.random.default_rng(42)


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(DB_PATH)

    users = pd.DataFrame({
        "user_id": range(1, 401),
        "full_name": [f"Customer {i:03d}" for i in range(1, 401)],
        "city": rng.choice(["Delhi","Mumbai","Bengaluru","Kolkata","Hyderabad","Pune","Jaipur"], 400),
        "signup_date": pd.Timestamp("2025-01-01") + pd.to_timedelta(rng.integers(0, 500, 400), unit="D"),
        "segment": rng.choice(["Budget","Standard","Premium"], 400, p=[.35,.48,.17]),
    })

    destinations = ["Jaipur","Goa","Manali","Kerala","Varanasi","Udaipur","Ladakh"]
    properties = []
    property_id = 1
    for dest in destinations:
        for j in range(8):
            properties.append({
                "property_id": property_id,
                "property_name": f"{dest} Stay {j+1}",
                "destination": dest,
                "property_type": rng.choice(["Hotel","Resort","Homestay","Hostel"], p=[.48,.22,.20,.10]),
                "nightly_rate": int(rng.integers(1800, 12000)),
            })
            property_id += 1
    properties = pd.DataFrame(properties)

    bookings = []
    for booking_id in range(1, 1201):
        user_id = int(rng.integers(1, 401))
        property_id = int(rng.integers(1, len(properties)+1))
        booking_date = pd.Timestamp("2025-06-01") + pd.to_timedelta(int(rng.integers(0, 430)), unit="D")
        nights = int(rng.integers(1, 8))
        rate = int(properties.loc[properties.property_id.eq(property_id), "nightly_rate"].iloc[0])
        status = rng.choice(["Completed","Confirmed","Cancelled"], p=[.61,.25,.14])
        total_amount = rate * nights if status != "Cancelled" else 0
        bookings.append({
            "booking_id": booking_id,
            "user_id": user_id,
            "property_id": property_id,
            "booking_date": booking_date,
            "nights": nights,
            "status": status,
            "total_amount": total_amount,
        })
    bookings = pd.DataFrame(bookings)

    users.to_sql("users", conn, index=False)
    properties.to_sql("properties", conn, index=False)
    bookings.to_sql("bookings", conn, index=False)

    conn.executescript("""
        CREATE INDEX idx_bookings_user ON bookings(user_id);
        CREATE INDEX idx_bookings_property ON bookings(property_id);
        CREATE INDEX idx_bookings_date ON bookings(booking_date);
    """)
    conn.commit()
    conn.close()
    print(f"Created database: {DB_PATH}")
    print("Tables: users=400, properties=56, bookings=1200")


if __name__ == "__main__":
    main()
