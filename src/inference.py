from ultralytics import YOLO
import cv2

def run_invoice_inference(model_path, image_path, conf_threshold=0.5):
    # Load weights
    model = YOLO(model_path)
    
    # Run inference (save=True bakal ngebikin folder runs/detect/predict dengan gambar hasil bbox)
    results = model.predict(source=image_path, conf=conf_threshold, save=True)
    
    extracted_data = []
    
    # Looping hasil prediksi (untuk 1 gambar, results biasanya list dengan 1 elemen)
    for result in results:
        for box in result.boxes:
            # Koordinat BBox (x_min, y_min, x_max, y_max)
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            
            # Confidence score & Class ID
            conf = box.conf[0].item()
            cls_id = int(box.cls[0].item())
            cls_name = model.names[cls_id]
            
            extracted_data.append({
                "class": cls_name,
                "confidence": round(conf, 3),
                "bbox": [round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)]
            })
            
            print(f"Terdeteksi: {cls_name} | Conf: {conf:.2f} | BBox: [{x1:.1f}, {y1:.1f}, {x2:.1f}, {y2:.1f}]")
            
    return extracted_data

# Cara eksekusi
if __name__ == "__main__":
    best_weights = "../models/best.pt"
    test_image = "../data/input/test_invoice.jpg"
    
    hasil_deteksi = run_invoice_inference(best_weights, test_image)