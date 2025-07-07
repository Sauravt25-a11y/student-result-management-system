
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os

CSV_FILE = "student_results_sem2_extracted.csv"

class ResultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Result Management System")
        self.geometry("950x600")
        self.resizable(False, False)

        # Load data
        if os.path.exists(CSV_FILE):
            self.df = pd.read_csv(CSV_FILE)
        else:
            self.df = pd.DataFrame(columns=["roll_no", "name", "father_name", "sgpa", "result"])

        # --- UI ---
        self.create_widgets()
        self.populate_tree()

    # ---------------- Widgets ---------------- #
    def create_widgets(self):
        # Search bar
        search_frame = tk.Frame(self)
        search_frame.pack(pady=5, fill="x")

        tk.Label(search_frame, text="Search Roll No:").pack(side="left", padx=(10,5))
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var, width=15).pack(side="left")
        tk.Button(search_frame, text="Search", command=self.search_record).pack(side="left", padx=5)
        tk.Button(search_frame, text="Show All", command=self.populate_tree).pack(side="left", padx=5)

        # Treeview (table)
        columns = ("roll_no", "name", "father_name", "sgpa", "result")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=150 if col != "name" else 180, anchor="center")
        self.tree.pack(padx=10, pady=5, fill="both", expand=False)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Entry form
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        labels = ["Roll No", "Name", "Father Name", "SGPA", "Result"]
        self.entries = {}
        for i, label in enumerate(labels):
            tk.Label(form_frame, text=label).grid(row=0, column=i, padx=5, sticky="w")
            entry = tk.Entry(form_frame, width=18)
            entry.grid(row=1, column=i, padx=5, pady=2)
            self.entries[label.lower().replace(" ", "_")] = entry

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=8)
        tk.Button(btn_frame, text="Add", width=12, command=self.add_record).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", width=12, command=self.update_record).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", width=12, command=self.delete_record).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Save to CSV", width=12, command=self.save_data).grid(row=0, column=3, padx=5)

    # ---------------- Functions ---------------- #
    def populate_tree(self):
        # Clear
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Insert
        for _, row in self.df.iterrows():
            self.tree.insert("", "end", values=row.tolist())

    def search_record(self):
        roll = self.search_var.get().strip()
        if not roll:
            messagebox.showinfo("Search", "Please enter a roll number.")
            return
        rec = self.df[self.df["roll_no"].astype(str) == roll]
        if rec.empty:
            messagebox.showinfo("Search", f"No record found for roll {roll}.")
        else:
            self.tree.selection_remove(*self.tree.get_children())  # clear selection
            self.populate_tree()
            # highlight the row
            for item in self.tree.get_children():
                if self.tree.item(item, "values")[0] == roll:
                    self.tree.selection_add(item)
                    self.tree.see(item)
                    break

    def on_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        vals = self.tree.item(selected[0], "values")
        keys = ["roll_no", "name", "father_name", "sgpa", "result"]
        for k, v in zip(keys, vals):
            self.entries[k].delete(0, tk.END)
            self.entries[k].insert(0, v)

    def add_record(self):
        data = {k: e.get().strip() for k, e in self.entries.items()}
        if "" in data.values():
            messagebox.showwarning("Add", "Please fill in all fields.")
            return
        if not data["sgpa"].replace(".", "", 1).isdigit():
            messagebox.showwarning("Add", "SGPA must be numeric.")
            return
        if not self.df[self.df["roll_no"].astype(str) == data["roll_no"]].empty:
            messagebox.showwarning("Add", "Roll number already exists.")
            return
        data["sgpa"] = float(data["sgpa"])
        self.df = pd.concat([self.df, pd.DataFrame([data])], ignore_index=True)
        self.populate_tree()
        messagebox.showinfo("Add", "Record added successfully.")

    def update_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Update", "Select a record to update.")
            return
        roll = self.tree.item(selected[0], "values")[0]
        idx = self.df.index[self.df["roll_no"].astype(str) == roll]
        if idx.empty:
            messagebox.showerror("Update", "Record not found in DataFrame.")
            return
        data = {k: e.get().strip() for k, e in self.entries.items()}
        if "" in data.values():
            messagebox.showwarning("Update", "Please fill in all fields.")
            return
        if not data["sgpa"].replace(".", "", 1).isdigit():
            messagebox.showwarning("Update", "SGPA must be numeric.")
            return
        for k, v in data.items():
            self.df.loc[idx, k] = float(v) if k == "sgpa" else v
        self.populate_tree()
        messagebox.showinfo("Update", "Record updated successfully.")

    def delete_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Delete", "Select a record to delete.")
            return
        roll = self.tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Delete", f"Delete record for roll {roll}?")
        if confirm:
            self.df = self.df[self.df["roll_no"].astype(str) != roll]
            self.populate_tree()
            messagebox.showinfo("Delete", "Record deleted.")

    def save_data(self):
        self.df.to_csv(CSV_FILE, index=False)
        messagebox.showinfo("Save", f"Data saved to {CSV_FILE}")

if __name__ == "__main__":
    app = ResultApp()
    app.mainloop()
