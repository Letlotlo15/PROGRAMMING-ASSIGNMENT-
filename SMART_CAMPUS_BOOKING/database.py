import sqlite3

DB_PATH = "campus.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialise_db():
    with get_connection() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('lecturer','admin','operator')),
            campus TEXT
        );

        CREATE TABLE IF NOT EXISTS campuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_code TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            campus TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_id INTEGER NOT NULL,
            lecturer_id INTEGER NOT NULL,
            campus TEXT NOT NULL,
            booking_date TEXT NOT NULL,
            start_time TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'active',
            FOREIGN KEY(resource_id) REFERENCES resources(id),
            FOREIGN KEY(lecturer_id) REFERENCES users(id)
        );
        """)
        conn.commit()


def seed_data():
    from auth import hash_password
    with get_connection() as conn:
        for c in ["Johannesburg", "Cape Town", "Durban"]:
            conn.execute("INSERT OR IGNORE INTO campuses(name) VALUES(?)", (c,))

        conn.execute(
            "INSERT OR IGNORE INTO users(username,password,role,campus) VALUES(?,?,?,?)",
            ("admin_jhb", hash_password("admin123"), "admin", "Johannesburg"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO users(username,password,role,campus) VALUES(?,?,?,?)",
            ("admin_cpt", hash_password("admin123"), "admin", "Cape Town"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO users(username,password,role,campus) VALUES(?,?,?,?)",
            ("admin_dbn", hash_password("admin123"), "admin", "Durban"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO users(username,password,role,campus) VALUES(?,?,?,?)",
            ("operator", hash_password("op123"), "operator", None),
        )

        samples = [
            ("LAB-JHB-01", "Computer Lab A", "Lab", "Johannesburg"),
            ("LAB-JHB-02", "Computer Lab B", "Lab", "Johannesburg"),
            ("PROJ-JHB-01", "Multimedia Projector", "Equipment", "Johannesburg"),
            ("LAB-CPT-01", "Computer Lab C", "Lab", "Cape Town"),
            ("SEM-CPT-01", "Seminar Room", "Room", "Cape Town"),
            ("PROJ-CPT-01", "Portable Projector", "Equipment", "Cape Town"),
            ("LAB-DBN-01", "Computer Lab D", "Lab", "Durban"),
            ("SEM-DBN-01", "Seminar Room", "Room", "Durban"),
        ]
        for code, name, cat, camp in samples:
            conn.execute(
                "INSERT OR IGNORE INTO resources(resource_code,name,category,campus) "
                "VALUES(?,?,?,?)", (code, name, cat, camp),
            )
        conn.commit()


if __name__ == "__main__":
    initialise_db()
    seed_data()
    print("Database initialised and seeded.")