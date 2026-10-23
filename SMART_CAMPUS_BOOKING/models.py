
class User:
    def __init__(self, user_id, username, role, campus=None):
        self._user_id = user_id
        self._username = username
        self._role = role
        self._campus = campus

    @property
    def user_id(self): return self._user_id

    @property
    def username(self): return self._username

    @property
    def role(self): return self._role

    @property
    def campus(self): return self._campus

    def permissions(self):
        return []

    def __str__(self):
        return f"{self._role}:{self._username}"


class Lecturer(User):
    def __init__(self, user_id, username, campus):
        super().__init__(user_id, username, "lecturer", campus)

    def permissions(self):
        return ["create_booking", "view_own_bookings", "cancel_booking"]


class CampusAdmin(User):
    def __init__(self, user_id, username, campus):
        super().__init__(user_id, username, "admin", campus)

    def permissions(self):
        return ["manage_resources", "view_campus_bookings", "campus_reports"]


class SystemOperator(User):
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "operator", None)

    def permissions(self):
        return ["view_all", "cross_campus_reports"]


class Resource:
    def __init__(self, resource_code, name, category, campus):
        self.resource_code = resource_code
        self.name = name
        self.category = category
        self.campus = campus

    def __repr__(self):
        return f"<Resource {self.resource_code} {self.name} @ {self.campus}>"


def build_user(row):
    """Build the correct User subclass from a DB row
    (id, username, password_hash, role, campus)."""
    uid, uname, _pw, role, campus = row
    if role == "lecturer":
        return Lecturer(uid, uname, campus)
    if role == "admin":
        return CampusAdmin(uid, uname, campus)
    return SystemOperator(uid, uname)