# Project 4 — SQL Database Extraction & Integration

## Business problem
Customer profiles, properties and booking transactions live in separate relational tables. Build SQL extracts that combine them into analysis-ready datasets and then continue the analysis in Pandas.

## Data model
- `users(user_id, full_name, city, signup_date, segment)`
- `properties(property_id, property_name, destination, property_type, nightly_rate)`
- `bookings(booking_id, user_id, property_id, booking_date, nights, status, total_amount)`

Relationships:
`users 1 ── * bookings * ── 1 properties`

## Step-by-step
1. Run `setup_database.py` to create a reproducible SQLite database.
2. Inspect the three table schemas.
3. Start with simple SELECT/WHERE queries.
4. Join bookings to users on `user_id`.
5. Join bookings to properties on `property_id`.
6. Aggregate destination performance with `GROUP BY`.
7. Use conditional aggregation for active/cancelled bookings.
8. Use `HAVING` to find high-value customers.
9. Use a `LEFT JOIN` to identify users with no bookings.
10. Use a CTE and `DENSE_RANK()` window function for destination rankings.
11. Load SQL results directly into Pandas with `pd.read_sql_query`.
12. Engineer `revenue_per_night` and `booking_month` in Python.
13. Export analysis-ready CSV files and validate SQL aggregates with Pandas.

## Run
```bash
python src/setup_database.py
python src/extract_and_analyze.py
```

Open `sql/analysis_queries.sql` in SQLite/VS Code to practice the queries manually.

## Interview explanation
“I modeled the business as users, properties and bookings, then used foreign-key-style joins to create a booking-level analytical dataset. SQL handled relational filtering and aggregation close to the data; Pandas handled downstream feature engineering and validation. I also practiced LEFT JOIN anti-matching, HAVING, CTEs and window functions.”

## Improvements
Actual primary/foreign-key constraints, parameterized queries, SQLAlchemy, PostgreSQL, incremental loads, dbt models, data-quality tests and orchestration.
