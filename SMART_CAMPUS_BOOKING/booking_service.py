from datetime import datetime, timedelta
from database import get_connection
from booking_rules import validate_booking


def check_overlap(resource_id, booking_date, start_time, duration_minutes):
    new_start = datetime.strptime(f"{booking_date} {start_time}", "%Y-%m-%d %H:%M")
    new_end = new_start + timedelta(minutes=duration_minutes)

    with get_connection() as conn:
        rows = conn.execute(
            "SELECT start_time, duration_minutes FROM bookings "
            "WHERE resource_id=? AND booking_date=? AND status='active'",
            (resource_id, booking_date),
        ).fetchall()

    for s, d in rows:
        ex_start = datetime.strptime(f"{booking_date} {s}", "%Y-%m-%d %H:%M")
        ex_end = ex_start + timedelta(minutes=d)
        if new_start < ex_end and ex_start < new_end:
            return True
    return False


def create_booking(user, resource_id, campus, booking_date, start_time, duration):
    ok, msg = validate_booking(campus, start_time, duration)
    if not ok:
        return False, msg
    if check_overlap(resource_id, booking_date, start_time, duration):
        return False, "Resource is already booked for that time slot."
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO bookings(resource_id,lecturer_id,campus,"
                "booking_date,start_time,duration_minutes) VALUES(?,?,?,?,?,?)",
                (resource_id, user.user_id, campus, booking_date, start_time, duration),
            )
            conn.commit()
        return True, "Booking created successfully."
    except Exception as e:
        return False, f"Booking failed: {e}"


def cancel_booking(booking_id, user):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT lecturer_id, booking_date, start_time FROM bookings WHERE id=?",
            (booking_id,),
        ).fetchone()
        if not row:
            return False, "Booking not found."
        if user.role == "lecturer" and row[0] != user.user_id:
            return False, "You can only cancel your own bookings."
        b_dt = datetime.strptime(f"{row[1]} {row[2]}", "%Y-%m-%d %H:%M")
        if b_dt <= datetime.now():
            return False, "Past bookings cannot be cancelled."
        conn.execute("UPDATE bookings SET status='cancelled' WHERE id=?", (booking_id,))
        conn.commit()
    return True, "Booking cancelled."


def list_lecturer_bookings(user):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT b.id, r.name, b.booking_date, b.start_time, b.duration_minutes, b.status
            FROM bookings b JOIN resources r ON r.id = b.resource_id
            WHERE b.lecturer_id = ? ORDER BY b.booking_date DESC, b.start_time DESC
        """, (user.user_id,)).fetchall()
    return rows


def list_campus_bookings(campus):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT b.id, r.name, u.username, b.booking_date,
                   b.start_time, b.duration_minutes, b.status
            FROM bookings b
            JOIN resources r ON r.id = b.resource_id
            JOIN users u ON u.id = b.lecturer_id
            WHERE b.campus = ?
            ORDER BY b.booking_date DESC, b.start_time DESC
        """, (campus,)).fetchall()
    return rows


def list_all_bookings():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT b.id, b.campus, r.name, u.username, b.booking_date,
                   b.start_time, b.duration_minutes, b.status
            FROM bookings b
            JOIN resources r ON r.id = b.resource_id
            JOIN users u ON u.id = b.lecturer_id
            ORDER BY b.booking_date DESC
        """).fetchall()
    return rows