-- Q1. Booking-level analytical dataset using a 3-table JOIN
SELECT
    b.booking_id,
    b.booking_date,
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
JOIN properties p ON b.property_id = p.property_id;

-- Q2. Destination performance
SELECT
    p.destination,
    COUNT(*) AS booking_count,
    SUM(CASE WHEN b.status != 'Cancelled' THEN 1 ELSE 0 END) AS active_bookings,
    ROUND(AVG(CASE WHEN b.status != 'Cancelled' THEN b.total_amount END), 2) AS avg_booking_value,
    SUM(b.total_amount) AS revenue
FROM bookings b
JOIN properties p ON b.property_id = p.property_id
GROUP BY p.destination
ORDER BY revenue DESC;

-- Q3. High-value customers using HAVING
SELECT
    u.user_id,
    u.full_name,
    u.segment,
    COUNT(b.booking_id) AS total_bookings,
    SUM(b.total_amount) AS lifetime_value
FROM users u
JOIN bookings b ON u.user_id = b.user_id
GROUP BY u.user_id, u.full_name, u.segment
HAVING SUM(b.total_amount) >= 100000
ORDER BY lifetime_value DESC;

-- Q4. Users with no bookings using LEFT JOIN
SELECT
    u.user_id,
    u.full_name,
    u.city
FROM users u
LEFT JOIN bookings b ON u.user_id = b.user_id
WHERE b.booking_id IS NULL
ORDER BY u.user_id;

-- Q5. Destination revenue ranking with a window function
WITH destination_revenue AS (
    SELECT
        p.destination,
        SUM(b.total_amount) AS revenue
    FROM bookings b
    JOIN properties p ON b.property_id = p.property_id
    GROUP BY p.destination
)
SELECT
    destination,
    revenue,
    DENSE_RANK() OVER (ORDER BY revenue DESC) AS revenue_rank
FROM destination_revenue
ORDER BY revenue_rank;

-- Q6. Monthly booking trend
SELECT
    substr(b.booking_date, 1, 7) AS month,
    COUNT(*) AS bookings,
    SUM(b.total_amount) AS revenue
FROM bookings b
GROUP BY substr(b.booking_date, 1, 7)
ORDER BY month;
