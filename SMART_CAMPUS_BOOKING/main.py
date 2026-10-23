
from database import initialise_db, seed_data
from gui.login_window import LoginWindow
from gui.lecturer_dashboard import LecturerDashboard
from gui.admin_dashboard import AdminDashboard
from gui.operator_dashboard import OperatorDashboard


def route_user(user):
    if user.role == "lecturer":
        LecturerDashboard(user).mainloop()
    elif user.role == "admin":
        AdminDashboard(user).mainloop()
    else:
        OperatorDashboard(user).mainloop()
if __name__ == "__main__":
    initialise_db()
    seed_data()
    LoginWindow(on_success=route_user).mainloop()