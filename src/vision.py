import cv2
import numpy as np
import fitz  
from config import PROCESSING_DIR
from ultralytics import YOLO
import os
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

def preprocess_pdf(pdf_path):
    print(f"Mulai bedah visual massal: {pdf_path.name}")
    doc = fitz.open(pdf_path)
    
    output_paths = []
    
    # Looping semua halaman di dalam PDF
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=300) 
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
        
        if pix.n == 4:  
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
            
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        thresh = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
        
        # Save dengan format nama file + nomor halaman
        output_path = pdf_path.parent / f"{pdf_path.stem}_page_{i+1}.jpg"
        cv2.imwrite(str(output_path), thresh)
        output_paths.append(output_path)
        
        print(f"[+] Halaman {i+1} diekstrak -> {output_path.name}")
        
    print(f"Total {len(doc)} halaman selesai diproses!")
    return output_paths

def extract_roi(image_path):
    print(f"\nMulai deteksi ROI YOLO di: {image_path.name}")
    
    # 1. Load Model YOLOv8 (Pake versi nano/n biar enteng buat CPU)
    # Nanti di real-world, file 'yolov8n.pt' ini diganti sama model hasil training Roboflow lo
    model = YOLO('yolov8n.pt') 
    
    # 2. Hajar gambarnya (kita paksa pake CPU biar ga crash)
    results = model(str(image_path), device='cpu')
    
    # 3. Bikin folder khusus buat hasil potongan gambar (crops)
    crop_dir = image_path.parent / f"{image_path.stem}_crops"
    crop_dir.mkdir(exist_ok=True)
    
    roi_paths = []
    
    # 4. Looping hasil bounding box
    for result in results:
        boxes = result.boxes
        for i, box in enumerate(boxes):
            # Ambil koordinat bounding box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            # (Optional) Ambil nama class, misalnya: 0 = Tabel, 1 = Tanda Tangan
            # cls = int(box.cls[0]) 
            
            # Potong gambarnya berdasarkan koordinat itu
            img = cv2.imread(str(image_path))
            roi_crop = img[y1:y2, x1:x2]
            
            # Save hasil potongannya
            roi_path = crop_dir / f"crop_{i}.jpg"
            cv2.imwrite(str(roi_path), roi_crop)
            roi_paths.append(roi_path)
            
            print(f"[+] Dipotong: {roi_path.name}")
            
    return roi_paths

def extract_text_trocr(image_path):
    print(f"\nMulai baca teks pakai TrOCR di: {image_path.name}")
    
    # Load model (kita pakai versi base dari Microsoft dulu buat testing)
    # Nanti bisa diganti ke model fine-tune lokal kayak NusaAksara
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
    model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")
    
    # Buka gambar crop-nya
    image = Image.open(image_path).convert("RGB")
    
    # Proses gambarnya
    pixel_values = processor(image, return_tensors="pt").pixel_values
    
    # Generate teks
    generated_ids = model.generate(pixel_values, max_new_tokens=50)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    
    print(f"[>] Hasil ekstraksi teks: {generated_text}")
    return generated_text

if __name__ == "__main__":
    dummy_files = list(PROCESSING_DIR.glob('*.pdf'))
    if dummy_files:
        jpg_paths = preprocess_pdf(dummy_files[0])
        
        if jpg_paths:
             # Ambil hasil crop dari halaman pertama
             roi_paths = extract_roi(jpg_paths[0])
             
             # Ekstrak teks dari salah satu hasil crop (misal crop yang pertama)
             if roi_paths:
                 hasil_teks = extract_text_trocr(roi_paths[0])
                 print(f"\n--- TEKS FINAL: {hasil_teks} ---")
    else:
        print("Kosong nih, belum ada file masuk dari folder raw.")