
#reports.py — Campus-level and cross-campus reporting.
from database import get_connection


def campus_report(campus):
    with get_connection() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM bookings WHERE campus=? AND status='active'",
            (campus,),
        ).fetchone()[0]

        top = conn.execute("""
            SELECT r.name, COUNT(*) AS uses
            FROM bookings b JOIN resources r ON r.id=b.resource_id
            WHERE b.campus=? AND b.status='active'
            GROUP BY r.id ORDER BY uses DESC LIMIT 5
        """, (campus,)).fetchall()

        avg = conn.execute(
            "SELECT AVG(duration_minutes) FROM bookings "
            "WHERE campus=? AND status='active'", (campus,),
        ).fetchone()[0] or 0

    return {
        "campus": campus,
        "total_bookings": total,
        "top_resources": top,
        "average_duration": round(avg, 1),
    }


def cross_campus_comparison():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT campus, COUNT(*) AS bookings, AVG(duration_minutes) AS avg_dur
            FROM bookings WHERE status='active'
            GROUP BY campus ORDER BY bookings DESC
        """).fetchall()
    return [
        {"campus": r[0], "bookings": r[1], "avg_duration": round(r[2] or 0, 1)}
        for r in rows
    ]