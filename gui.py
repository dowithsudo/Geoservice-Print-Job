import tkinter as tk
from tkinter import filedialog, messagebox

from app import print_one_job, print_from_csv, print_from_excel


def clear_form():
    """Hapus semua input field di form GUI"""
    entries = [
        entry_job_no,
        entry_box_no,
        entry_first,
        entry_last,
        entry_date,
        entry_lsn,
        entry_sid,
        entry_counter,
    ]

    for entry in entries:
        entry.delete(0, tk.END)


def print_from_form():
    data = {
        "job_no": entry_job_no.get(),
        "box_no": entry_box_no.get(),          # optional
        "first": entry_first.get(),
        "last": entry_last.get(),
        "date_received": entry_date.get(),
        "lsn": entry_lsn.get(),
        "sid": entry_sid.get(),
        "counter": entry_counter.get(),        # optional
    }

    # ===== VALIDASI (KONSISTEN DENGAN EXCEL) =====
    required_fields = [
        "job_no",
        "first",
        "last",
        "date_received",
        "lsn",
        "sid",
    ]

    for key in required_fields:
        if not data[key].strip():
            messagebox.showerror("Error", f"Field '{key}' wajib diisi")
            return

    try:
        print_one_job(data)
        messagebox.showinfo("Sukses", "Label berhasil dicetak")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def import_csv():
    file_path = filedialog.askopenfilename(
        filetypes=[("CSV files", "*.csv")]
    )
    if not file_path:
        return

    try:
        print_from_csv(file_path)
        messagebox.showinfo("Sukses", "CSV berhasil dicetak")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def import_excel():
    file_path = filedialog.askopenfilename(
        filetypes=[("Excel files", "*.xlsx")]
    )
    if not file_path:
        return

    try:
        print_from_excel(file_path)
        messagebox.showinfo("Sukses", "Excel berhasil dicetak")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= UI =================

root = tk.Tk()
root.title("Label Printer - Zebra ZD230")
root.geometry("450x520")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)


def add_field(label, row):
    tk.Label(frame, text=label).grid(row=row, column=0, sticky="w")
    entry = tk.Entry(frame, width=40)
    entry.grid(row=row, column=1, pady=4)
    return entry


entry_job_no = add_field("Job No", 0)
entry_box_no = add_field("Box No (optional)", 1)
entry_first = add_field("First", 2)
entry_last = add_field("Last", 3)
entry_date = add_field("Date Rec'd (dd/mm/yy)", 4)
entry_lsn = add_field("LSN", 5)
entry_sid = add_field("SID", 6)
entry_counter = add_field("Counter (jumlah label belakang)", 7)

# ===== BUTTONS =====

tk.Button(
    frame,
    text="PRINT LABEL",
    height=2,
    command=print_from_form
).grid(row=8, column=0, columnspan=2, pady=(10, 4), sticky="we")

tk.Button(
    frame,
    text="CLEAR FORM",
    command=clear_form
).grid(row=9, column=0, columnspan=2, pady=(0, 10), sticky="we")

tk.Button(
    frame,
    text="IMPORT CSV",
    command=import_csv
).grid(row=10, column=0, columnspan=2, sticky="we")

tk.Button(
    frame,
    text="IMPORT EXCEL",
    command=import_excel
).grid(row=11, column=0, columnspan=2, pady=5, sticky="we")

root.mainloop()
