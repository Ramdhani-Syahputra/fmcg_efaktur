from ultralytics import YOLO

# Load model custom buatan lo
model = YOLO('fmcg_yolo_poc.pt') 

# Tembak ke satu gambar surat jalan/nota palsu lo buat test drive
results = model.predict(source='dataset/gambar-testing1.jpg', save=True)