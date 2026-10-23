#Lecturer dashboard: book resources, view and cancel bookings.
import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from booking_service import create_booking, cancel_booking, list_lecturer_bookings
from booking_rules import get_policy

FONT = ("Times New Roman", 12)

class LecturerDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title(f"Lecturer — {user.username}")
        self.geometry("900x600")
        self.campus_var = tk.StringVar(value=user.campus or "Johannesburg")
        self._build()
        self._load_resources()

    def _build(self):
        top = tk.Frame(self)
        top.pack(fill="x", pady=5)
        tk.Label(top, text="Active campus:", font=FONT).pack(side="left", padx=5)
        cb = ttk.Combobox(top, textvariable=self.campus_var,
                          values=["Johannesburg", "Cape Town", "Durban"],
                          state="readonly", width=20, font=FONT)
        cb.pack(side="left")
        cb.bind("<<ComboboxSelected>>", lambda e: self._load_resources())

        self.policy_lbl = tk.Label(top, text="", font=("Times New Roman", 10, "italic"),
                                   fg="blue")
        self.policy_lbl.pack(side="left", padx=15)
        self._update_policy()

        # Resources list
        tk.Label(self, text="Available Resources", font=("Times New Roman", 13, "bold")).pack(anchor="w", padx=10)
        cols = ("code", "name", "category")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=8)
        for c, w in zip(cols, (120, 250, 150)):
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=w)
        self.tree.pack(fill="x", padx=10)

        # Booking form
        form = tk.LabelFrame(self, text="Create Booking", font=FONT)
        form.pack(fill="x", padx=10, pady=10)
        tk.Label(form, text="Date (YYYY-MM-DD):", font=FONT).grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.date_var = tk.StringVar()
        tk.Entry(form, textvariable=self.date_var, font=FONT, width=15).grid(row=0, column=1)

        tk.Label(form, text="Start (HH:MM):", font=FONT).grid(row=0, column=2, padx=5, sticky="e")
        self.time_var = tk.StringVar()
        tk.Entry(form, textvariable=self.time_var, font=FONT, width=10).grid(row=0, column=3)

        tk.Label(form, text="Duration (min):", font=FONT).grid(row=0, column=4, padx=5, sticky="e")
        self.dur_var = tk.StringVar()
        tk.Entry(form, textvariable=self.dur_var, font=FONT, width=10).grid(row=0, column=5)

        tk.Button(form, text="Book Selected Resource", font=FONT,
                  command=self._book).grid(row=0, column=6, padx=10)

        # My bookings
        tk.Label(self, text="My Bookings", font=("Times New Roman", 13, "bold")).pack(anchor="w", padx=10)
        cols2 = ("id", "resource", "date", "start", "duration", "status")
        self.mine = ttk.Treeview(self, columns=cols2, show="headings", height=8)
        for c in cols2:
            self.mine.heading(c, text=c.title())
            self.mine.column(c, width=110)
        self.mine.pack(fill="both", expand=True, padx=10, pady=5)

        tk.Button(self, text="Cancel Selected Booking", font=FONT,
                  command=self._cancel).pack(pady=5)

    def _update_policy(self):
        p = get_policy(self.campus_var.get())
        if p:
            self.policy_lbl.config(text=f"Policy: {p['description']}")

    def _load_resources(self):
        self._update_policy()
        for r in self.tree.get_children():
            self.tree.delete(r)
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id,resource_code,name,category FROM resources WHERE campus=?",
                (self.campus_var.get(),),
            ).fetchall()
        for rid, code, name, cat in rows:
            self.tree.insert("", "end", iid=str(rid), values=(code, name, cat))
        self._load_mine()

    def _load_mine(self):
        for r in self.mine.get_children():
            self.mine.delete(r)
        for row in list_lecturer_bookings(self.user):
            self.mine.insert("", "end", values=row)

    def _book(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a resource first.")
            return
        try:
            dur = int(self.dur_var.get())
        except ValueError:
            messagebox.showerror("Invalid", "Duration must be a number.")
            return
        ok, msg = create_booking(
            self.user, int(sel[0]), self.campus_var.get(),
            self.date_var.get().strip(), self.time_var.get().strip(), dur,
        )
        if ok:
            messagebox.showinfo("Success", msg)
            self._load_mine()
        else:
            messagebox.showerror("Booking failed", msg)

    def _cancel(self):
        sel = self.mine.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a booking to cancel.")
            return
        bid = int(self.mine.item(sel[0])["values"][0])
        ok, msg = cancel_booking(bid, self.user)
        if ok:
            messagebox.showinfo("Cancelled", msg)
            self._load_mine()
        else:
            messagebox.showerror("Cancel failed", msg)