import tkinter as tk
from tkinter import ttk, messagebox
from database import get_connection
from booking_service import list_campus_bookings
from reports import campus_report

FONT = ("Times New Roman", 12)


class AdminDashboard(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.title(f"Admin — {user.campus}")
        self.geometry("1050x620")
        self.campus = user.campus
        self._build()
        self._load_resources()
        self._load_bookings()

    def _build(self):
        tk.Label(self, text=f"Campus: {self.campus}",
                 font=("Times New Roman", 14, "bold")).pack(pady=8)

        # Resource management
        frame = tk.LabelFrame(self, text="Resources", font=FONT)
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        cols = ("id", "code", "name", "category")
        self.tree = ttk.Treeview(frame, columns=cols, show="headings", height=7)
        for c in cols:
            self.tree.heading(c, text=c.title())
            self.tree.column(c, width=140)
        self.tree.pack(fill="x", side="top")

        form = tk.Frame(frame)
        form.pack(fill="x", pady=5)

        tk.Label(form, text="Code:", font=FONT).grid(row=0, column=0)
        self.code_var = tk.StringVar()
        tk.Entry(form, textvariable=self.code_var, font=FONT, width=15).grid(row=0, column=1)

        tk.Label(form, text="Name:", font=FONT).grid(row=0, column=2)
        self.name_var = tk.StringVar()
        tk.Entry(form, textvariable=self.name_var, font=FONT, width=20).grid(row=0, column=3)

        tk.Label(form, text="Category:", font=FONT).grid(row=0, column=4)
        self.cat_var = tk.StringVar()
        tk.Entry(form, textvariable=self.cat_var, font=FONT, width=15).grid(row=0, column=5)

        # Buttons: Add, Delete, Update
        tk.Button(form, text="Add", font=FONT, command=self._add).grid(row=0, column=6, padx=5)
        tk.Button(form, text="Delete Selected", font=FONT, command=self._delete).grid(row=0, column=7, padx=5)
        tk.Button(form, text="Update Selected", font=FONT, command=self._update).grid(row=0, column=8, padx=5)

        # Bookings
        tk.Label(self, text="Campus Bookings", font=("Times New Roman", 13, "bold")).pack(anchor="w", padx=10)
        cols2 = ("id", "resource", "lecturer", "date", "start", "duration", "status")
        self.bk = ttk.Treeview(self, columns=cols2, show="headings", height=7)
        for c in cols2:
            self.bk.heading(c, text=c.title())
            self.bk.column(c, width=105)
        self.bk.pack(fill="x", padx=10)

        tk.Button(self, text="Generate Campus Report", font=FONT,
                  command=self._report).pack(pady=8)

    def _load_resources(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id,resource_code,name,category FROM resources WHERE campus=?",
                (self.campus,),
            ).fetchall()
        for row in rows:
            self.tree.insert("", "end", values=row)

    def _load_bookings(self):
        for r in self.bk.get_children():
            self.bk.delete(r)
        for row in list_campus_bookings(self.campus):
            self.bk.insert("", "end", values=row)

    def _add(self):
        code = self.code_var.get().strip()
        name = self.name_var.get().strip()
        cat = self.cat_var.get().strip()
        if not (code and name and cat):
            messagebox.showerror("Invalid", "All fields required.")
            return
        try:
            with get_connection() as conn:
                conn.execute(
                    "INSERT INTO resources(resource_code,name,category,campus) "
                    "VALUES(?,?,?,?)", (code, name, cat, self.campus),
                )
                conn.commit()
            messagebox.showinfo("Added", f"Resource {code} added.")
            self._load_resources()
        except Exception as e:
            messagebox.showerror("Duplicate or error", str(e))

    def _delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Please select a resource to delete.")
            return
        rid = self.tree.item(sel[0])["values"][0]
        with get_connection() as conn:
            conn.execute("DELETE FROM resources WHERE id=?", (rid,))
            conn.commit()
        self._load_resources()

    def _update(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("No selection", "Select a resource to update.")
            return

        rid = self.tree.item(sel[0])["values"][0]
        new_code = self.code_var.get().strip()
        new_name = self.name_var.get().strip()
        new_cat = self.cat_var.get().strip()

        if not (new_code and new_name and new_cat):
            messagebox.showerror("Invalid", "All fields must be filled to update.")
            return

        try:
            with get_connection() as conn:
                conn.execute(
                    "UPDATE resources SET resource_code=?, name=?, category=? WHERE id=?",
                    (new_code, new_name, new_cat, rid)
                )
                conn.commit()
            messagebox.showinfo("Updated", "Resource updated successfully.")
            self._load_resources()
        except Exception as e:
            messagebox.showerror("Error", f"Update failed. Code might already exist.\n{e}")

    def _report(self):
        r = campus_report(self.campus)
        msg = f"Campus: {r['campus']}\nTotal bookings: {r['total_bookings']}\n"
        msg += f"Average duration: {r['average_duration']} min\n\nTop resources:\n"
        for name, uses in r["top_resources"]:
            msg += f"  {name}: {uses}\n"
        messagebox.showinfo("Campus Report", msg)