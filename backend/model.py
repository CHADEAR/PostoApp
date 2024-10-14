
import cv2
import numpy as np
import easyocr
import pandas as pd
import os
import re
from roboflow import Roboflow
from PIL import Image

# Initialize Roboflow client
rf = Roboflow(api_key="NNVM2evYZAe2wMrp9xGl")
project = rf.workspace("farafrang").project("parcel-receiver-name-detection-mdp3r")
model = project.version(2).model

# Create EasyOCR reader
reader = easyocr.Reader(['en', 'th'])  # Supports English and Thai

def read_name_from_image(image_path):
    result = model.predict(image_path).json()
    
    detected_names = []
    bounding_boxes = []
    
    if 'predictions' in result:
        for prediction in result['predictions']:
            name = prediction['class']
            x1 = int(prediction['x'] - prediction['width'] / 2)
            y1 = int(prediction['y'] - prediction['height'] / 2)
            x2 = int(prediction['x'] + prediction['width'] / 2)
            y2 = int(prediction['y'] + prediction['height'] / 2)
            
            detected_names.append(name)
            bounding_boxes.append((x1, y1, x2, y2))

    return detected_names, bounding_boxes

def crop_and_read_names(image_path, bounding_boxes):
    image = Image.open(image_path)
    cropped_names = []

    for box in bounding_boxes:
        x1, y1, x2, y2 = box
        cropped_image = np.array(image)[y1:y2, x1:x2]
        
        result = reader.readtext(cropped_image)
        for (_, text, _) in result:
            cleaned_text = re.sub(r'\s+', '', text)
            cropped_names.append(cleaned_text.strip())

    return cropped_names

def save_to_csv(cropped_names):
    csv_file_path = 'names.csv'

    try:
        if os.path.exists(csv_file_path):
            existing_df = pd.read_csv(csv_file_path)
        else:
            existing_df = pd.DataFrame(columns=['name', 'count'])

        for name in cropped_names:
            if pd.notna(name):  # ตรวจสอบค่า Null
                if name in existing_df['name'].values:
                    existing_df.loc[existing_df['name'] == name, 'count'] += 1
                else:
                    new_row = pd.DataFrame({'name': [name], 'count': [1]})
                    existing_df = pd.concat([existing_df, new_row], ignore_index=True)

        existing_df.to_csv(csv_file_path, index=False, encoding='utf-8')
    except Exception as e:
        print(f"เกิดข้อผิดพลาดในการบันทึกไฟล์ CSV: {e}")


def count_names_in_csv(csv_file_path='names.csv'):  # แก้ไขเป็นชื่อไฟล์ที่ถูกต้อง
    if os.path.isfile(csv_file_path):
        df = pd.read_csv(csv_file_path, encoding='utf-8')
        return df if not df.empty else pd.DataFrame(columns=['name', 'count'])
    else:
        return pd.DataFrame(columns=['name', 'count'])
