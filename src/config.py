import os
from pathlib import Path

# Set root directory
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Mapping landing zone
RAW_PDF_DIR = DATA_DIR / "1_raw_pdf"
PROCESSING_DIR = DATA_DIR / "2_processing"
XML_DIR = DATA_DIR / "3_output_xml"
ERROR_DIR = DATA_DIR / "4_error"
ARCHIVE_DIR = DATA_DIR / "5_archive"

# Otomatis create folder kalau belum ada (anti-crash pas run pertama kali)
for d in [RAW_PDF_DIR, PROCESSING_DIR, XML_DIR, ERROR_DIR, ARCHIVE_DIR]:
    d.mkdir(parents=True, exist_ok=True)
    
print("Config loaded. Direktori aman.")