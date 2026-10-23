
#auth.py — User registration and login with SHA-256 password hashing.
import hashlib
from database import get_connection
from models import build_user


def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


def register(username, password, role, campus=None):
    if not username or not password:
        return False, "Username and password are required."
    if role not in ("lecturer", "admin", "operator"):
        return False, "Invalid role."
    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users(username,password,role,campus) VALUES(?,?,?,?)",
                (username, hash_password(password), role, campus),
            )
            conn.commit()
        return True, "Registered successfully."
    except Exception as e:
        return False, f"Registration failed: {e}"


def login(username, password):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id,username,password,role,campus FROM users WHERE username=?",
            (username,),
        ).fetchone()
    if not row:
        return None, "User not found."
    if row[2] != hash_password(password):
        return None, "Incorrect password."
    return build_user(row), "Login OK."