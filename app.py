from printer.zebra_templates import label_depan, label_belakang
from printer.zebra_print import send_to_printer
from csv_handler.csv_writer import save_printed_data
from csv_handler.csv_reader import read_csv
from excel_handler.excel_reader import read_excel



def print_one_job(data):
    send_to_printer(label_depan(data))
    send_to_printer(label_belakang(data))
    save_printed_data(data)


def print_from_csv(csv_file):
    rows = read_csv(csv_file)
    for data in rows:
        print_one_job(data)

def print_from_excel(excel_file):
    rows = read_excel(excel_file)
    for data in rows:
        print_one_job(data)



# TEST MANUAL (boleh dihapus nanti)
if __name__ == "__main__":
    data = {
        "job_no": "MLG.01163",
        "box_no": "1 of 1",
        "first": "GLAB/PC-MCS/2025/12/475-1",
        "last": "GLAB/PC-MCS/2025/12/475-4",
        "date_received": "30/12/2025",
        "lsn": "CIK 25-1579582",
        "sid": "GLAB/PC-MCS/2025/12/475-1"
    }

    print_one_job(data)
