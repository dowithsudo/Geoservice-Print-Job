import tkinter as tk
from tkinter import filedialog, messagebox

from app import print_one_job, print_from_csv, print_from_excel
from csv_handler.csv_reader import read_csv
from excel_handler.excel_reader import read_excel


# ================= LOGIC =================

def print_from_form():
    data = {
        "job_no": entry_job_no.get(),
        "box_no": entry_box_no.get(),
        "first": entry_first.get(),
        "last": entry_last.get(),
        "date_received": entry_date.get(),
        "lsn": entry_lsn.get(),
        "sid": entry_sid.get(),
    }

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
        rows = read_csv(file_path)
        total_jobs = len(rows)

        if total_jobs == 0:
            messagebox.showinfo("Info", "Tidak ada data untuk dicetak")
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Cetak",
            f"Jumlah data: {total_jobs}\n"
            f"Total label tercetak: {total_jobs * 2}\n\n"
            "Lanjutkan cetak?"
        )

        if not confirm:
            return

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
        rows = read_excel(file_path)
        total_jobs = len(rows)

        if total_jobs == 0:
            messagebox.showinfo("Info", "Tidak ada data untuk dicetak")
            return

        confirm = messagebox.askyesno(
            "Konfirmasi Cetak",
            f"Jumlah data: {total_jobs}\n"
            f"Total label tercetak: {total_jobs * 2}\n\n"
            "Lanjutkan cetak?"
        )

        if not confirm:
            return

        print_from_excel(file_path)
        messagebox.showinfo("Sukses", "Excel berhasil dicetak")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= UI =================

root = tk.Tk()
root.title("PT. Geoservices - Label Printer")
root.geometry("480x500")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(expand=True)

# ===== Title =====
tk.Label(
    main_frame,
    text="PT. Geoservices",
    font=("Arial", 16, "bold")
).pack(pady=(0, 10))

tk.Label(
    main_frame,
    text="Zebra ZD230 Label Printer",
    font=("Arial", 10)
).pack(pady=(0, 20))


form_frame = tk.Frame(main_frame)
form_frame.pack()


def add_field(label):
    row = tk.Frame(form_frame)
    row.pack(fill="x", pady=4)

    tk.Label(row, text=label, width=14, anchor="w").pack(side="left")
    entry = tk.Entry(row, width=35)
    entry.pack(side="right", expand=True, fill="x")
    return entry


entry_job_no = add_field("Job No")
entry_box_no = add_field("Box No")
entry_first = add_field("First")
entry_last = add_field("Last")
entry_date = add_field("Date Rec'd")
entry_lsn = add_field("LSN")
entry_sid = add_field("SID")


# ===== Buttons =====
btn_frame = tk.Frame(main_frame)
btn_frame.pack(pady=25)

tk.Button(
    btn_frame,
    text="PRINT LABEL",
    width=22,
    height=2,
    command=print_from_form
).pack(pady=5)

tk.Button(
    btn_frame,
    text="IMPORT CSV",
    width=22,
    command=import_csv
).pack(pady=5)

tk.Button(
    btn_frame,
    text="IMPORT EXCEL",
    width=22,
    command=import_excel
).pack(pady=5)

root.mainloop()
# ================= END UI =================