import xml.etree.ElementTree as ET
from xml.dom import minidom
import pandas as pd
from config import XML_DIR

def generate_efaktur_xml(df_reconciled):
    print("\n--- Mulai Generate XML e-Faktur ---")
    
    # Bikin Root (Akar) XML-nya
    root = ET.Element("ImportFakturPajakKeluaran")
    
    # Looping data Pandas lo jadi struktur XML
    for index, row in df_reconciled.iterrows():
        faktur = ET.SubElement(root, "FakturPajak")
        
        # Detail Pelanggan dari Database ERP
        ET.SubElement(faktur, "NamaPelanggan").text = str(row['nama_erp'])
        ET.SubElement(faktur, "CustomerID").text = str(row['customer_id'])
        
        # Detail Barang (Pakai kuantitas aktual hasil scan lapangan!)
        detail = ET.SubElement(faktur, "DetailBarang")
        ET.SubElement(detail, "Kuantitas").text = str(row['qty_aktual'])
        
        # Catatan khusus kalau ada retur biar admin pajak tau
        catatan = "Sesuai Surat Jalan" if row['status'] == 'MATCH' else "Ada Retur di Lapangan"
        ET.SubElement(faktur, "Referensi").text = catatan

    # Bikin XML-nya rapi biar gampang dibaca manusia (pretty print)
    xml_string = ET.tostring(root, 'utf-8')
    parsed_xml = minidom.parseString(xml_string)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")
    
    # Save file-nya ke Landing Zone Output
    output_file = XML_DIR / "import_efaktur_batch_1.xml"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(pretty_xml)
        
    print(f"[+] BOOM! File XML siap di-import DJP: {output_file}")
    return output_file

if __name__ == "__main__":
    # Kita panggil file reconcile.py tadi buat ngambil df_final
    from reconcile import reconcile_data
    
    # Mock data dari tahap sebelumnya
    mock_ocr_data = [
        {'scanned_name': 'PT Formaocean Indo', 'scanned_qty': 150},
        {'scanned_name': 'CV Maju Jaya', 'scanned_qty': 45},        
        {'scanned_name': 'Toko Berkah Mandir1', 'scanned_qty': 200} 
    ]
    
    df_reconciled = reconcile_data(mock_ocr_data)
    generate_efaktur_xml(df_reconciled)