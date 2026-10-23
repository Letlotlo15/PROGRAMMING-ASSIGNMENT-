
import tkinter as tk
from tkinter import messagebox, simpledialog
from auth import login, register

# Define a global font variable to ensure consistency (Times New Roman, size 12 as required)
FONT = ("Times New Roman", 12)


class LoginWindow(tk.Tk):

    #The Login Window is the first screen the user sees.
    #It inherits from tk.Tk, which means this class IS the main application window.

    def __init__(self, on_success):
        # Initialize the main Tkinter window
        super().__init__()
        self.on_success = on_success
        self.title("Smart Campus — Login")
        self.geometry("450x400")
        self._build()

    def _build(self):

        tk.Label(self, text="Smart Campus Resource Booking System",
                 font=("Times New Roman", 15, "bold")).pack(pady=15)
        frm = tk.Frame(self)
        frm.pack(pady=10)
        tk.Label(frm, text="Username:", font=FONT).grid(row=0, column=0, sticky="e", pady=5)
        self.user_var = tk.StringVar()
        tk.Entry(frm, textvariable=self.user_var, font=FONT, width=22).grid(row=0, column=1)

        tk.Label(frm, text="Password:", font=FONT).grid(row=1, column=0, sticky="e", pady=5)
        self.pw_var = tk.StringVar()
        tk.Entry(frm, textvariable=self.pw_var, show="*", font=FONT, width=22).grid(row=1, column=1)

        # Action Buttons
        tk.Button(self, text="Login", width=22, font=FONT,
                  command=self._do_login).pack(pady=8)
        tk.Button(self, text="Register as Lecturer", width=22, font=FONT,
                  command=self._reg_lecturer).pack(pady=2)
        tk.Button(self, text="Register as Admin", width=22, font=FONT,
                  command=self._reg_admin).pack(pady=2)
        tk.Label(self, text="Default: admin_jhb/admin123, operator/op123",
                 font=("Times New Roman", 9, "italic")).pack(pady=15)

    def _do_login(self):
        username = self.user_var.get().strip()
        password = self.pw_var.get()
        user, msg = login(username, password)
        if not user:
            messagebox.showerror("Login failed", msg)
            return
        self.destroy()
        self.on_success(user)

    def _reg_lecturer(self):
#Wrapper function to trigger registration specifically for lecturers
        self._process_registration("lecturer")

    def _reg_admin(self):
#Wrapper function to trigger registration specifically for admins.
        self._process_registration("admin")

    def _process_registration(self, role):
#Handles the shared registration logic for both Admins and Lecturers.
        username = self.user_var.get().strip()
        password = self.pw_var.get()
        if not username or not password:
            messagebox.showerror("Error", "Please type a Username and Password in the boxes before clicking Register.")
            return
        campus = simpledialog.askstring("Campus", "Enter your campus (e.g., Johannesburg):")
        if not campus:
            return
        ok, msg = register(username, password, role, campus.strip())
        if ok:
            messagebox.showinfo("Success", f"Registered successfully as {role.capitalize()}! You can now log in.")
        else:
            messagebox.showerror("Registration Failed", msg)