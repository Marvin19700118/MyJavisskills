# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "face_recognition",
#     "opencv-python-headless",
#     "numpy",
#     "pandas",
#     "openpyxl"
# ]
# ///

import face_recognition
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

FACES_DB = "social_faces_db.pkl"

def load_db():
    if os.path.exists(FACES_DB):
        with open(FACES_DB, 'rb') as f:
            return pickle.load(f)
    return {"names": [], "encodings": []}

def save_db(db):
    with open(FACES_DB, 'wb') as f:
        pickle.dump(db, f)

def register_face(image_path, name_id):
    # Load the image
    image = face_recognition.load_image_file(image_path)
    
    # Find all face encodings in the image
    face_encodings = face_recognition.face_encodings(image)
    
    if len(face_encodings) == 0:
        return json.dumps({"status": "error", "message": "照片中找不到人臉，請換一張更清晰的照片。"}, ensure_ascii=False)
    elif len(face_encodings) > 1:
        return json.dumps({"status": "error", "message": "照片中有多個人臉，註冊時請使用單人清晰照。"}, ensure_ascii=False)
        
    # Get the single encoding
    encoding = face_encodings[0]
    
    db = load_db()
    
    # Check if name_id already exists and update, or append
    if name_id in db["names"]:
        idx = db["names"].index(name_id)
        db["encodings"][idx] = encoding
        msg = f"成功更新 {name_id} 的臉部特徵。"
    else:
        db["names"].append(name_id)
        db["encodings"].append(encoding)
        msg = f"成功註冊 {name_id} 的新臉部特徵。"
        
    save_db(db)
    return json.dumps({"status": "success", "message": msg}, ensure_ascii=False)

def recognize_face(image_path):
    db = load_db()
    if not db["names"]:
        return json.dumps({"status": "error", "message": "資料庫中目前沒有任何人臉特徵，請先註冊。"}, ensure_ascii=False)
        
    # Load the image to check
    unknown_image = face_recognition.load_image_file(image_path)
    
    # Find all faces in the unknown image
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
    
    if len(face_encodings) == 0:
        return json.dumps({"status": "error", "message": "無法從照片中辨識出人臉。"}, ensure_ascii=False)
        
    results = []
    
    # Check each face found in the image against our database
    for face_encoding in face_encodings:
        # Compare faces (lower tolerance = stricter match, 0.6 is default)
        matches = face_recognition.compare_faces(db["encodings"], face_encoding, tolerance=0.5)
        face_distances = face_recognition.face_distance(db["encodings"], face_encoding)
        
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = db["names"][best_match_index]
            confidence = round((1 - face_distances[best_match_index]) * 100, 2)
            results.append({"name_id": name, "confidence": confidence})
            
    if not results:
        return json.dumps({"status": "not_found", "message": "抱歉，資料庫中沒有找到匹配的人。"}, ensure_ascii=False)
        
    return json.dumps({"status": "success", "matches": results}, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "參數不足。用法: python face_engine.py <register|recognize> <image_path> [name_id]"}, ensure_ascii=False))
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
