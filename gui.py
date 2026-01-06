import tkinter as tk
from tkinter import filedialog, messagebox
from excel_handler.excel_reader import read_excel
import re

from app import print_one_job, print_from_csv, print_from_excel


# ================= UTIL =================

def build_lsn_list(base_lsn: str, counter: int):
    """
    Bangun list LSN hasil increment (untuk info ke user)
    """
    match = re.match(r"^(.*?)(\d+)$", base_lsn.strip())
    if not match:
        return []

    prefix = match.group(1)
    start_number = int(match.group(2))

    return [
        f"{prefix}{start_number + i}"
        for i in range(counter)
    ]


def build_excel_summary(excel_file):
    rows = read_excel(excel_file)

    total_jobs = len(rows)
    total_labels = 0
    job_details = []

    for row in rows:
        job_no = row.get("job_no", "-")

        try:
            counter = int(row.get("counter")) if str(row.get("counter")).strip() else 1
            if counter < 1:
                counter = 1
        except ValueError:
            counter = 1

        total_labels += counter
        job_details.append(f"- Job {job_no} → {counter} label")

    return total_jobs, total_labels, job_details


def clear_form():
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


# ================= ACTIONS =================

def print_from_form():
    data = {
        "job_no": entry_job_no.get(),
        "box_no": entry_box_no.get(),
        "first": entry_first.get(),
        "last": entry_last.get(),
        "date_received": entry_date.get(),
        "lsn": entry_lsn.get(),
        "sid": entry_sid.get(),
        "counter": entry_counter.get(),
    }

    # ---- VALIDASI (SAMA DENGAN EXCEL) ----
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

    # ---- NORMALISASI COUNTER UNTUK INFO ----
    try:
        counter = int(data["counter"]) if data["counter"].strip() else 1
        if counter < 1:
            counter = 1
    except ValueError:
        counter = 1  # error bisnis akan ditangani app.py

    try:
        # ---- PROSES PRINT ----
        print_one_job(data)

        # ---- BUILD INFO MESSAGE ----
        lsn_list = build_lsn_list(data["lsn"], counter)

        message = (
            "Print berhasil\n\n"
            f"Job No : {data['job_no']}\n"
            f"Total label belakang : {len(lsn_list)}\n\n"
            "LSN:\n" + "\n".join(f"- {lsn}" for lsn in lsn_list)
        )

        messagebox.showinfo("Sukses", message)

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
        # ---- PROSES PRINT ----
        print_from_excel(file_path)

        # ---- BUILD SUMMARY ----
        total_jobs, total_labels, job_details = build_excel_summary(file_path)

        message = (
            "Print Excel berhasil\n\n"
            f"Total Job   : {total_jobs}\n"
            f"Total Label : {total_labels}\n\n"
            "Detail:\n" + "\n".join(job_details)
        )

        messagebox.showinfo("Sukses", message)

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= UI =================

root = tk.Tk()
root.title("Label Printer - Zebra ZD230")
root.geometry("450x560")

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
