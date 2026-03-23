# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "opencv-python",
#     "numpy",
#     "pandas",
#     "openpyxl"
# ]
# ///

import cv2
import numpy as np
import pandas as pd
import os
import pickle
import json
import sys

# Windows print encoding fix
if sys.platform.startswith('win'):
    sys.stdout.reconfigure(encoding='utf-8')

FACES_DB = "social_faces_db_cv2.pkl"

def load_db():
    if os.path.exists(FACES_DB):
        with open(FACES_DB, 'rb') as f:
            return pickle.load(f)
    return {"names": [], "histograms": []}

def save_db(db):
    with open(FACES_DB, 'wb') as f:
        pickle.dump(db, f)

# We use an alternative lightweight method for demonstration since dlib/CMake is not installed.
# We will use OpenCV's built-in Haar Cascades for face detection and simple Histogram comparison (or EigenFaces if available).
# For production, deep learning models like MediaPipe or DeepFace are preferred over dlib on Windows.

def extract_face(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(image_path)
    if img is None:
        return None
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return None
        
    # Return the largest face region
    x, y, w, h = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
    face_roi = gray[y:y+h, x:x+w]
    face_roi = cv2.resize(face_roi, (100, 100)) # Normalize size
    return face_roi

def register_face(image_path, name_id):
    face = extract_face(image_path)
    if face is None:
        return json.dumps({"status": "error", "message": "照片中找不到人臉，或請換一張正面清晰的照片。"}, ensure_ascii=False)
        
    # Create a simple representation (Histogram or flattened array)
    # Using LBP or simply saving the normalized face for a simple recognizer
    db = load_db()
    
    if name_id in db["names"]:
        idx = db["names"].index(name_id)
        db["histograms"][idx] = face
        msg = f"成功更新 {name_id} 的臉部特徵 (CV2)。"
    else:
        db["names"].append(name_id)
        db["histograms"].append(face)
        msg = f"成功註冊 {name_id} 的新臉部特徵 (CV2)。"
        
    save_db(db)
    return json.dumps({"status": "success", "message": msg}, ensure_ascii=False)

def recognize_face(image_path):
    db = load_db()
    if not db["names"]:
        return json.dumps({"status": "error", "message": "資料庫中目前沒有任何人臉特徵，請先註冊。"}, ensure_ascii=False)
        
    face = extract_face(image_path)
    if face is None:
        return json.dumps({"status": "error", "message": "無法從照片中辨識出人臉。"}, ensure_ascii=False)
        
    # Simple EigenFace or Template Matching (using MSE for basic demo)
    best_match = None
    min_diff = float('inf')
    
    for idx, stored_face in enumerate(db["histograms"]):
        # Mean Squared Error between the 100x100 grayscale face matrices
        diff = np.mean((face - stored_face) ** 2)
        if diff < min_diff:
            min_diff = diff
            best_match = db["names"][idx]
            
    # Threshold for MSE (needs tuning based on lighting, 3000 is arbitrary)
    if min_diff < 5000:
        confidence = round(max(0, 100 - (min_diff / 100)), 2)
        return json.dumps({"status": "success", "matches": [{"name_id": best_match, "confidence": confidence}]}, ensure_ascii=False)
    else:
        return json.dumps({"status": "not_found", "message": "抱歉，資料庫中沒有找到足夠相似的人。"}, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "參數不足。用法: python face_engine_cv2.py <register|recognize> <image_path> [name_id]"}, ensure_ascii=False))
        sys.exit(1)
        
    action = sys.argv[1]
    image_path = sys.argv[2]
    
    if not os.path.exists(image_path):
        print(json.dumps({"error": f"找不到圖片檔案: {image_path}"}, ensure_ascii=False))
        sys.exit(1)
        
    if action == "register":
        if len(sys.argv) < 4:
            print(json.dumps({"error": "註冊人臉需要提供姓名識別碼 (name_id)。"}, ensure_ascii=False))
            sys.exit(1)
        name_id = sys.argv[3]
        print(register_face(image_path, name_id))
        
    elif action == "recognize":
        print(recognize_face(image_path))
    else:
        print(json.dumps({"error": "未知的指令，僅支援 register 或 recognize。"}, ensure_ascii=False))
