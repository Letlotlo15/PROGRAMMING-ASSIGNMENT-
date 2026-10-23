#System operator dashboard: cross-campus comparison.
import tkinter as tk
from tkinter import ttk, messagebox
from booking_service import list_all_bookings
from reports import cross_campus_comparison

FONT = ("Times New Roman", 12)


class OperatorDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title("System Operator — All Campuses")
        self.geometry("950x600")
        self._build()
        self._load()

    def _build(self):
        tk.Label(self, text="Cross-Campus Comparison",
                 font=("Times New Roman", 14, "bold")).pack(pady=8)

        cols = ("campus", "bookings", "avg_duration")
        self.cmp = ttk.Treeview(self, columns=cols, show="headings", height=5)
        for c in cols:
            self.cmp.heading(c, text=c.replace("_", " ").title())
            self.cmp.column(c, width=200)
        self.cmp.pack(fill="x", padx=10)

        tk.Label(self, text="All Bookings",
                 font=("Times New Roman", 13, "bold")).pack(anchor="w", padx=10, pady=10)

        cols2 = ("id", "campus", "resource", "lecturer", "date", "start", "duration", "status")
        self.tree = ttk.Treeview(self, columns=cols2, show="headings", height=12)
        for c in cols2:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=100)
        self.tree.pack(fill="both", expand=True, padx=10)

        tk.Button(self, text="Refresh", font=FONT, command=self._load).pack(pady=8)

    def _load(self):
        for r in self.cmp.get_children():
            self.cmp.delete(r)
        for row in cross_campus_comparison():
            self.cmp.insert("", "end",
                            values=(row["campus"], row["bookings"], row["avg_duration"]))

        for r in self.tree.get_children():
            self.tree.delete(r)
        for row in list_all_bookings():
            self.tree.insert("", "end", values=row)