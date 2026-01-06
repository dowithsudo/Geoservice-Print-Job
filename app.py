from printer.zebra_templates import label_depan, label_belakang
from printer.zebra_print import send_to_printer
from csv_handler.csv_writer import save_printed_data
from csv_handler.csv_reader import read_csv
from excel_handler.excel_reader import read_excel

import re


def parse_lsn(lsn: str):
    """
    Memecah LSN menjadi (prefix, number)
    Contoh:
      CIK 25-1579582
      -> ("CIK 25-", 1579582)
    """
    if not lsn:
        raise ValueError("LSN kosong")

    match = re.match(r"^(.*?)(\d+)$", lsn.strip())
    if not match:
        raise ValueError(f"LSN tidak valid (tidak ada angka di akhir): {lsn}")

    prefix = match.group(1)
    number = int(match.group(2))
    return prefix, number


def normalize_counter(value):
    """
    Normalisasi counter:
    - None / kosong -> 1
    - < 1 -> 1
    - bukan angka -> error
    """
    if value is None or str(value).strip() == "":
        return 1

    try:
        counter = int(value)
    except ValueError:
        raise ValueError(f"Counter bukan angka: {value}")

    return max(counter, 1)


def print_one_job(data):
    """
    Cetak 1 job:
    - Label depan: 1x (base LSN)
    - Label belakang: Nx (LSN auto-increment)
    - CSV: simpan per LSN hasil
    """

    # --- Normalisasi counter ---
    counter = normalize_counter(data.get("counter"))

    # --- Parsing LSN ---
    base_lsn = data.get("lsn")
    prefix, start_number = parse_lsn(base_lsn)

    # --- 1) PRINT LABEL DEPAN (SELALU PERTAMA) ---
    data_depan = data.copy()   # defensive copy
    send_to_printer(label_depan(data_depan))

    # --- 2) PRINT LABEL BELAKANG (LOOP) ---
    for i in range(counter):
        computed_lsn = f"{prefix}{start_number + i}"

        data_iter = data.copy()
        data_iter["lsn"] = computed_lsn

        # HAPUS counter sebelum simpan CSV
        data_iter.pop("counter", None)
        
        send_to_printer(label_belakang(data_iter))
        save_printed_data(data_iter)


def print_from_csv(csv_file):
    rows = read_csv(csv_file)
    for data in rows:
        print_one_job(data)


def print_from_excel(excel_file):
    rows = read_excel(excel_file)
    for data in rows:
        print_one_job(data)


# =========================
# TEST MANUAL (DEV ONLY)
# =========================
if __name__ == "__main__":
    # Test helper
    print(parse_lsn("CIK 25-1579582"))     # ('CIK 25-', 1579582)
    print(normalize_counter(""))           # 1
    print(normalize_counter("4"))          # 4
    print(normalize_counter(0))            # 1

    # Test print logic (counter > 1)
    test_data = {
        "job_no": "MLG.01163",
        "box_no": "1 of 1",
        "first": "GLAB/PC-MCS/2025/12/475-1",
        "last": "GLAB/PC-MCS/2025/12/475-4",
        "date_received": "30/12/25",
        "lsn": "CIK 25-1579582",
        "sid": "GLAB/PC-MCS/2025/12/475-1",
        "counter": 4
    }

    print_one_job(test_data)
