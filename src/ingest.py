import os
import shutil
from config import RAW_PDF_DIR, PROCESSING_DIR, ERROR_DIR

def check_and_ingest():
    print("Agent Ingest aktif: mantau Surat Jalan baru...")
    
    # Cuma nangkep file PDF
    files = [f for f in os.listdir(RAW_PDF_DIR) if f.lower().endswith('.pdf')]
    
    if not files:
        print("Folder kosong. Admin logistik belum upload.")
        return

    for file in files:
        raw_path = RAW_PDF_DIR / file
        processing_path = PROCESSING_DIR / file
        error_path = ERROR_DIR / file
        
        try:
            # Pindah ke arena eksekusi
            shutil.move(str(raw_path), str(processing_path))
            print(f"[+] Ditarik ke processing: {file}")
            
            # TODO: Panggil fungsi OpenCV (deskewing & binarization) di sini nanti
            
        except Exception as e:
            print(f"[!] Crash pas narik {file}. Buang ke karantina. Error: {e}")
            shutil.move(str(raw_path), str(error_path))

if __name__ == "__main__":
    check_and_ingest()