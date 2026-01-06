import csv
import os

CSV_FILE = "data/printed_labels.csv"

HEADERS = [
    "job_no",
    "box_no",
    "first",
    "last",
    "date_received",
    "lsn",
    "sid"
]


def save_printed_data(data):
    os.makedirs("data", exist_ok=True)

    file_exists = os.path.isfile(CSV_FILE)

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)

        if not file_exists:
            writer.writeheader()

        writer.writerow(data)
