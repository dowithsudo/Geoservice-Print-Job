# Dokumentasi Aplikasi - Label Printer Zebra

## 📋 Ringkasan Aplikasi

Aplikasi **Label Printer Zebra** adalah sistem pencetakan label untuk **PT. Geoservices (Mineral)** yang dibangun menggunakan Python. Aplikasi ini memungkinkan pencetakan label barok dan belakang dari printer Zebra dengan kemampuan:

- ✅ Pencetakan manual melalui GUI
- ✅ Import dan pencetakan batch dari CSV
- ✅ Import dan pencetakan batch dari Excel
- ✅ Auto-increment nomor LSN untuk label belakang
- ✅ Penyimpanan data tercetak ke database CSV
- ✅ Validasi data input otomatis

---

## 📁 Struktur Direktori

```
label_print_app/
├── app.py                      # Core logic aplikasi
├── gui.py                      # Interface GUI (Tkinter)
├── LabelPrinterZebra.spec      # Spec file untuk PyInstaller
│
├── printer/                    # Module printer
│   ├── zebra_print.py         # Komunikasi dengan printer
│   ├── zebra_templates.py     # Template ZPL untuk label
│   └── zebra_config.py        # Konfigurasi printer
│
├── csv_handler/               # Module CSV
│   ├── csv_reader.py          # Membaca file CSV
│   └── csv_writer.py          # Menulis data tercetak ke CSV
│
├── excel_handler/             # Module Excel
│   └── excel_reader.py        # Membaca file Excel
│
└── data/                       # Folder data
    ├── import_labels.csv       # Data label untuk import
    └── printed_labels.csv      # Hasil data yang tercetak
```

---

## 🔧 Daftar Fungsi Aplikasi

### **1. MODULE: app.py** (Core Logic)

#### **Fungsi: `parse_lsn(lsn: str)`**
- **Tujuan:** Memecah string LSN menjadi prefix dan nomor
- **Input:** String LSN (contoh: "CIK 25-1579582")
- **Output:** Tuple (prefix, number) - (str, int)
- **Contoh:**
  ```python
  parse_lsn("CIK 25-1579582")  → ("CIK 25-", 1579582)
  ```
- **Validasi:** 
  - LSN tidak boleh kosong
  - LSN harus mengandung angka di akhir
  - Menggunakan regex: `^(.*?)(\d+)$`

#### **Fungsi: `normalize_counter(value)`**
- **Tujuan:** Normalisasi nilai counter (jumlah label belakang)
- **Input:** Nilai counter (int, str, None)
- **Output:** Integer counter (minimum 1)
- **Logika:**
  - None atau kosong → return 1
  - Kurang dari 1 → return 1
  - Bukan angka → raise ValueError

#### **Fungsi: `print_one_job(data)`**
- **Tujuan:** Cetak satu job lengkap (label depan + belakang)
- **Input:** Dictionary dengan keys:
  - `job_no` (str): Nomor job
  - `box_no` (str): Nomor box
  - `first` (str): Nama depan
  - `last` (str): Nama belakang
  - `date_received` (str): Tanggal  terima (dd/mm/yy)
  - `lsn` (str): Labor Sample Number (format: "PREFIX NUMBER")
  - `sid` (str): Sample ID
  - `counter` (int/str): Jumlah label belakang
  
- **Proses:**
  1. Normalisasi counter
  2. Parse LSN menjadi prefix + start_number
  3. Print label depan (1x dengan LSN base)
  4. Loop print label belakang dengan LSN auto-increment
  5. Simpan data tercetak ke CSV

- **Output:** Tidak ada (side-effect: print + save)

#### **Fungsi: `print_from_csv(csv_file)`**
- **Tujuan:** Cetak batch dari file CSV
- **Input:** Path file CSV
- **Proses:** 
  1. Baca CSV dengan `read_csv()`
  2. Loop setiap baris → panggil `print_one_job()`

#### **Fungsi: `print_from_excel(excel_file)`**
- **Tujuan:** Cetak batch dari file Excel
- **Input:** Path file Excel (.xlsx)
- **Proses:** 
  1. Baca Excel dengan `read_excel()`
  2. Loop setiap baris → panggil `print_one_job()`

---

### **2. MODULE: gui.py** (Interface GUI - Tkinter)

#### **Fungsi: `build_lsn_list(base_lsn: str, counter: int)`**
- **Tujuan:** Bangun list LSN hasil increment untuk info ke user
- **Input:** LSN base (str), counter (int)
- **Output:** List berisi LSN yang sudah di-increment
- **Contoh:**
  ```python
  build_lsn_list("CIK 25-1579582", 3)
  → ["CIK 25-1579582", "CIK 25-1579583", "CIK 25-1579584"]
  ```

#### **Fungsi: `build_excel_summary(excel_file)`**
- **Tujuan:** Buat ringkasan Excel untuk ditampilkan ke user
- **Input:** Path file Excel
- **Output:** Tuple (total_jobs, total_labels, job_details_list)
- **Job Details:** List berisi string seperti "- Job XYZ → 5 label"

#### **Fungsi: `clear_form()`**
- **Tujuan:** Kosongkan semua field input di form
- **Proses:** Delete semua text dari entry widgets

#### **Fungsi: `print_from_form()`**
- **Tujuan:** Cetak label dari data di form
- **Validasi:**
  - Field wajib: job_no, first, last, date_received, lsn, sid
  - Kolom opsional: box_no, counter
- **Proses:**
  1. Kumpulkan data dari form
  2. Validasi field wajib
  3. Panggil `print_one_job(data)`
  4. Build LSN list untuk info
  5. Tampilkan dialog sukses dengan detail LSN
- **Error Handling:** Tangkap exception dan tampilkan error dialog

#### **Fungsi: `import_csv()`**
- **Tujuan:** Import dan cetak batch dari file CSV
- **Proses:**
  1. Buka dialog file picker (filter: .csv)
  2. Panggil `print_from_csv()`
  3. Tampilkan sukses dialog
- **Error Handling:** Tangkap exception dan tampilkan error dialog

#### **Fungsi: `import_excel()`**
- **Tujuan:** Import dan cetak batch dari file Excel
- **Proses:**
  1. Buka dialog file picker (filter: .xlsx)
  2. Panggil `print_from_excel()`
  3. Build summary dengan `build_excel_summary()`
  4. Tampilkan sukses dialog dengan detail summary
- **Error Handling:** 
  - PermissionError: File masih dibuka di aplikasi lain
  - Exception: Error umum

#### **Fungsi: `add_field(label, row)`**
- **Tujuan:** Utility membuat field Entry
- **Input:** Label text (str), row number (int)
- **Output:** tk.Entry widget

#### **Fungsi: `add_date_field(label, row)`**
- **Tujuan:** Utility membuat field DateEntry (dari tkcalendar)
- **Input:** Label text (str), row number (int)
- **Output:** DateEntry widget dengan format dd/mm/yy
- **Format:** DateEntry dengan date_pattern "dd/mm/yy"

#### **GUI Layout:**
- **Rows:**
  - 0: Job No
  - 1: Box No (optional)
  - 2: First
  - 3: Last
  - 4: Date Rec'd (DateEntry)
  - 5: LSN
  - 6: SID
  - 7: Counter (jumlah label belakang)
  - 8: Button PRINT LABEL
  - 9: Button CLEAR FORM
  - 10: Button IMPORT CSV
  - 11: Button IMPORT EXCEL

---

### **3. MODULE: printer/zebra_print.py** (Komunikasi Printer)

#### **Fungsi: `send_to_printer(zpl)`**
- **Tujuan:** Kirim ZPL command ke printer Zebra
- **Input:** String ZPL (Zebra Programming Language)
- **Proses:**
  1. Buka koneksi ke printer (nama dari config)
  2. Start document job dengan type "RAW"
  3. Start page
  4. Write ZPL data (encode UTF-8)
  5. End page
  6. End document
  7. Close koneksi
- **Library:** Menggunakan `win32print` (Windows printer API)
- **Error Handling:** Try-finally untuk memastikan printer always closed

---

### **4. MODULE: printer/zebra_templates.py** (Template Label)

#### **Fungsi: `label_depan(data)`**
- **Tujuan:** Generate ZPL untuk label depan
- **Input:** Dictionary dengan keys: job_no, box_no, first, last, date_received
- **Output:** String ZPL command
- **Content:**
  - Title: "GeoAssay Laboratory - CIKARANG"
  - Job No, Box No, First, Last, Date Rec'd
  - Ukuran: 640x400 (80mm x 50mm)
  - Font: A0N ukuran 28-34pt

#### **Fungsi: `label_belakang(data)`**
- **Tujuan:** Generate ZPL untuk label belakang
- **Input:** Dictionary dengan keys: job_no, lsn, sid, date_received, box_no
- **Output:** String ZPL command
- **Content:**
  - Title: "GEOASSAY LABORATORY"
  - Job No
  - LSN (teks + barcode 1D Code128)
  - SID
  - Date Rec'd
  - Box No
  - Ukuran: 640x400 (80mm x 50mm)
  - Barcode: BCN format, height 60

---

### **5. MODULE: printer/zebra_config.py** (Konfigurasi)

#### **Konstanta:**
- **`PRINTER_NAME`** (str): "ZDesigner ZD230-203dpi ZPL"
  - Nama printer yang akan digunakan
  - Harus sesuai dengan nama printer di Windows
- **`LABEL_WIDTH`** (int): 640 pixel (80mm)
- **`LABEL_HEIGHT`** (int): 400 pixel (50mm)

---

### **6. MODULE: csv_handler/csv_reader.py** (Baca CSV)

#### **Fungsi: `read_csv(file_path)`**
- **Tujuan:** Baca file CSV dan return list of dictionaries
- **Input:** Path file CSV
- **Output:** List[Dict] berisi data dari CSV
- **Encoding:** UTF-8
- **Format:** CSV dengan header (uses csv.DictReader)
- **Contoh:**
  ```python
  read_csv("data.csv")
  → [
      {"job_no": "001", "first": "John", ...},
      {"job_no": "002", "first": "Jane", ...}
    ]
  ```

---

### **7. MODULE: csv_handler/csv_writer.py** (Simpan CSV)

#### **Fungsi: `save_printed_data(data)`**
- **Tujuan:** Simpan data hasil cetak ke CSV
- **Input:** Dictionary data hasil cetak
- **Output:** None (side-effect: append ke file CSV)
- **File Target:** `data/printed_labels.csv`
- **Headers:**
  - job_no, box_no, first, last, date_received, lsn, sid
- **Logika:**
  1. Buat folder `data/` jika belum ada
  2. Check apakah file sudah ada
  3. Jika belum ada: tulis header
  4. Append row data
- **Encoding:** UTF-8
- **Mode:** Append (mode='a')

---

### **8. MODULE: excel_handler/excel_reader.py** (Baca Excel)

#### **Fungsi: `read_excel(file_path)`**
- **Tujuan:** Baca file Excel dan return list of dictionaries
- **Input:** Path file Excel (.xlsx)
- **Output:** List[Dict] berisi data dari Excel
- **Library:** `openpyxl` dengan data_only=True

#### **Required Headers (WAJIB):**
```
job_no, box_no, first, last, date_received, lsn, sid, counter
```

#### **Validasi:**
- File tidak boleh kosong
- Header harus match EXACTLY (urutan dan nama)
- Exception jika tidak sesuai

#### **Normalisasi Data:**
- **date_received:**
  - Jika datetime object → format ke dd/mm/yy
  - Jika string → parse dari YYYY-MM-DD → dd/mm/yy
  - Fallback: gunakan string as-is
- **Semua field lain:** Convert ke string
- **Skip baris kosong:** Baris yang semua kolomnya None/kosong di-skip

#### **Contoh Output:**
```python
[
  {
    "job_no": "001",
    "box_no": "A1",
    "first": "John",
    "last": "Doe",
    "date_received": "11/02/26",
    "lsn": "CIK 25-1579582",
    "sid": "SID001",
    "counter": "3"
  },
  ...
]
```

---

## 🔄 Alur Kerja Aplikasi

### **Scenario 1: Print dari Form GUI**
```
User input form → print_from_form()
  ↓
Validasi field wajib
  ↓
print_one_job(data)
  ├─ parse_lsn() → (prefix, start_number)
  ├─ normalize_counter() → counter (int)
  ├─ send_to_printer(label_depan)  [1x]
  ├─ Loop counter kali:
  │  ├─ Hitung LSN baru (prefix + start_number + i)
  │  ├─ send_to_printer(label_belakang)
  │  └─ save_printed_data() [simpan ke CSV]
  └─ Return sukses
  ↓
Show info dialog dengan LSN list
```

### **Scenario 2: Import Batch dari CSV**
```
User klik "IMPORT CSV" → File picker
  ↓
import_csv()
  ↓
print_from_csv(file_path)
  ├─ read_csv() → List[Dict]
  └─ For setiap row:
      └─ print_one_job(row)  [sama seperti scenario 1]
  ↓
Show sukses dialog
```

### **Scenario 3: Import Batch dari Excel**
```
User klik "IMPORT EXCEL" → File picker
  ↓
import_excel()
  ├─ print_from_excel(file_path)
  │  ├─ read_excel() → List[Dict]
  │  │  └─ Validasi headers
  │  └─ For setiap row:
  │      └─ print_one_job(row)  [sama seperti scenario 1]
  │
  ├─ build_excel_summary() → (total_jobs, total_labels, details)
  │
  └─ Show sukses dialog dengan summary
```

---

## 📊 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                        (gui.py - Tkinter)                       │
│                                                                 │
│  Form Input  │  Import CSV  │  Import Excel  │  View History  │
└──────┬───────┴──────┬────────┴──────┬────────┴────────┬───────┘
       │              │               │                │
       ↓              ↓               ↓                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CORE LOGIC (app.py)                          │
│                                                                 │
│  ┌──────────┐  ┌──────────────┐  ┌──────────────┐             │
│  │parse_lsn │  │normalize_cnt │  │print_one_job │             │
│  └──────────┘  └──────────────┘  └──────┬───────┘             │
│                                          │                     │
│             ┌────────────────────────────┼──────────────────┐  │
│             ↓                            ↓                  ↓  │
│      ┌────────────────┐  ┌──────────────────────────────────┐ │
│      │CSV Handler     │  │     PRINTER PROCESSING           │ │
│      │(csv_reader.py) │  │  (zebra_print.py)                │ │
│      └────────────────┘  │  (zebra_templates.py)            │ │
│             ↓            │  (zebra_config.py)               │ │
│      ┌────────────────┐  │                                  │ │
│      │Excel Handler   │  └──────────────┬───────────────────┘ │
│      │(excel_reader)  │                 │                     │
│      └────────────────┘                 ↓                     │
│                              ┌─────────────────────┐          │
│                              │ ZPL Commands       │          │
│                              │ (label_depan,      │          │
│                              │  label_belakang)   │          │
│                              └─────────────────────┘          │
└──────────────────────────────────────────┬────────────────────┘
                                           │
        ┌──────────────────────────────────┼──────┐
        ↓                                  ↓      ↓
   ┌─────────────┐              ┌──────────────┐
   │ CSV Writer  │              │ ZEBRA PRINTER│
   │ (save CSV)  │              │ (Windows API)│
   └─────────────┘              └──────────────┘
        │
        ↓
   ┌─────────────────────┐
   │ printed_labels.csv  │
   │ (History/Record)    │
   └─────────────────────┘
```

---

## 📝 Format Data

### **Input Format - Form/CSV/Excel:**
```json
{
  "job_no": "JOB001",
  "box_no": "BOX-A1",
  "first": "JOHN",
  "last": "DOE",
  "date_received": "11/02/26",
  "lsn": "CIK 25-1579582",
  "sid": "SID-001",
  "counter": "3"
}
```

### **Output Format - Saved CSV:**
```csv
job_no,box_no,first,last,date_received,lsn,sid
JOB001,BOX-A1,JOHN,DOE,11/02/26,CIK 25-1579582,SID-001
JOB001,BOX-A1,JOHN,DOE,11/02/26,CIK 25-1579583,SID-001
JOB001,BOX-A1,JOHN,DOE,11/02/26,CIK 25-1579584,SID-001
```

Note: `counter` field di-remove sebelum save CSV (hanya untuk cetak)

---

## 🛡️ Validasi dan Error Handling

### **Validasi Level Input (GUI):**
- Field wajib diisi: job_no, first, last, date_received, lsn, sid
- Error message jika field kosong

### **Validasi Level Bisnis (app.py):**
- LSN harus ada angka di akhir
- Counter harus angka atau kosong (default 1)
- Semua nilai harus bisa di-convert ke string

### **Validasi Level Excel (excel_handler):**
- Header harus match EXACTLY
- File tidak boleh kosong
- Date format normalisasi

### **Error Handling:**
- ValueError: Logika bisnis error (LSN, counter, header)
- PermissionError: File Excel sedang dibuka (special message)
- Exception umum: Tampilkan error message ke user

---

## ⚙️ Dependencies

```
tkinter          # Built-in Python GUI
tkcalendar      # DateEntry widget
openpyxl        # Baca/write Excel
win32print      # Windows printer API
python-dateutil # (Implicit via openpyxl)
csv             # Built-in CSV module
re              # Built-in regex
os              # Built-in OS operations
datetime        # Built-in datetime
```

---

## 🚀 Cara Menjalankan Aplikasi

### **Development Mode:**
```bash
# Pastikan dependencies terinstall
pip install openpyxl tkcalendar pywin32

# Jalankan GUI
python gui.py
```

### **Build Executable:**
```bash
# Menggunakan PyInstaller (sudah ada di spec)
pyinstaller LabelPrinterZebra.spec
```

---

## 📌 Catatan Penting

1. **Nama Printer:** Harus sesuai dengan nama printer di Windows
   - Check: Settings > Devices > Printers & Scanners
   - Atau update di `printer/zebra_config.py`

2. **Format LSN:** Harus memiliki prefix dan trailing number
   - ✅ Benar: "CIK 25-1579582", "SAMPLE-001"
   - ❌ Salah: "SAMPLE", "CIK25"

3. **Counter:** Jumlah label belakang (base label depan selalu 1)
   - Counter kosong/0 → default 1
   - Counter 3 → cetak 1 label depan + 3 label belakang

4. **CSV Import Format:**
   - Header harus match persis dengan kolom yang dipersyaratkan
   - Encoding: UTF-8

5. **Excel Import Format:**
   - Header harus match PERSIS (urutan & nama)
   - Format date: Bisa Excel date object atau string YYYY-MM-DD
   - Akan otomatis dikonversi ke dd/mm/yy

6. **Date Format:**
   - Input: dd/mm/yy (dari GUI) atau berbagai format (dari Excel)
   - Storage: Tetap dalam format input
   - Output: Dicetak apa adanya ke label

---

## 🎯 Ringkasan Fungsi Utama

| Fungsi | Module | Input | Output | Tujuan |
|--------|--------|-------|--------|--------|
| `parse_lsn()` | app.py | str LSN | (prefix, number) | Parse LSN |
| `normalize_counter()` | app.py | any | int | Validasi counter |
| `print_one_job()` | app.py | dict | None | Cetak 1 job |
| `print_from_csv()` | app.py | str path | None | Cetak batch CSV |
| `print_from_excel()` | app.py | str path | None | Cetak batch Excel |
| `send_to_printer()` | zebra_print.py | str ZPL | None | Kirim ke printer |
| `label_depan()` | zebra_temp.py | dict | str ZPL | Generate label depan |
| `label_belakang()` | zebra_temp.py | dict | str ZPL | Generate label belakang |
| `read_csv()` | csv_reader.py | str path | List[Dict] | Baca CSV |
| `save_printed_data()` | csv_writer.py | dict | None | Simpan CSV |
| `read_excel()` | excel_reader.py | str path | List[Dict] | Baca Excel |

---

**Dokumentasi dibuat pada:** 11 Februari 2026

