import pandas as pd
from fuzzywuzzy import process

def reconcile_data(ocr_results):
    print("\n--- Mulai Proses Rekonsiliasi ---")
    
    # 1. Mock Database Master ERP (Anggap aja ini ditarik dari sistem internal klien)
    erp_db = pd.DataFrame({
        'customer_id': ['C001', 'C002', 'C003'],
        'customer_name': ['PT Formaocean Indonesia', 'CV Maju Jaya Abadi', 'Toko Berkah Mandiri'],
        'qty_kirim': [150, 50, 200]
    })
    print("Data ERP Internal:")
    print(erp_db[['customer_name', 'qty_kirim']])
    print("-" * 30)

    # 2. Konversi hasil OCR ke DataFrame
    df_ocr = pd.DataFrame(ocr_results)
    
    rekonsiliasi_final = []

    # 3. Logika Fuzzy Matching & Komparasi
    for index, row in df_ocr.iterrows():
        scanned_name = row['scanned_name']
        scanned_qty = row['scanned_qty']
        
        # Cari nama paling mirip di database ERP
        # Limit 1 hasil teratas, balikin tuple (nama_match, skor_kemiripan)
        match_result = process.extractOne(scanned_name, erp_db['customer_name'].tolist())
        best_match_name = match_result[0]
        match_score = match_result[1]
        
        # Ambil data asli dari ERP berdasarkan nama yang match
        erp_row = erp_db[erp_db['customer_name'] == best_match_name].iloc[0]
        
        # Cek apakah ada retur/diskrepansi
        is_discrepancy = scanned_qty != erp_row['qty_kirim']
        
        rekonsiliasi_final.append({
            'customer_id': erp_row['customer_id'],
            'nama_erp': best_match_name,
            'nama_scan': scanned_name,
            'skor_fuzzy': match_score,
            'qty_erp': erp_row['qty_kirim'],
            'qty_aktual': scanned_qty,
            'status': 'WARNING_RETUR' if is_discrepancy else 'MATCH'
        })

    df_final = pd.DataFrame(rekonsiliasi_final)
    print("\nData Setelah Direkonsiliasi:")
    print(df_final[['nama_erp', 'nama_scan', 'skor_fuzzy', 'qty_aktual', 'status']])
    
    return df_final

if __name__ == "__main__":
    # Mock data hasil OCR dari lapangan (sengaja dibikin typo dan ada retur)
    mock_ocr_data = [
        {'scanned_name': 'PT Formaocean Indo', 'scanned_qty': 150}, # Typo, qty pas
        {'scanned_name': 'CV Maju Jaya', 'scanned_qty': 45},        # Typo, ada retur 5 barang
        {'scanned_name': 'Toko Berkah Mandir1', 'scanned_qty': 200} # Typo angka 1, qty pas
    ]
    
    hasil_df = reconcile_data(mock_ocr_data)