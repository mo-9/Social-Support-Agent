import os
import pandas as pd
from pypdf import PdfReader
from PIL import Image
import pytesseract

# --- إعداد مسار Tesseract ---
default_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
if os.path.exists(default_path):
    pytesseract.pytesseract.tesseract_cmd = default_path
    os.environ['TESSDATA_PREFIX'] = r'C:\Program Files\Tesseract-OCR\tessdata'

# --- الدالة الرئيسية ---
def extract_text_from_file(file_path: str) -> str:
    try:
        if not os.path.exists(file_path):
            return "File not found."

        ext = file_path.split(".")[-1].lower()
        
        # 1. التعامل مع PDF
        if ext == "pdf":
            return _read_pdf(file_path)
        
        # 2. التعامل مع الصور
        elif ext in ["jpg", "jpeg", "png", "bmp"]:
            return _read_image(file_path)
        
        # 3. التعامل مع الإكسل والـ CSV (الجديد)
        elif ext in ["csv", "xlsx", "xls"]:
            return _read_tabular_data(file_path, ext)
            
        else:
            return f"Unsupported file format: {ext}"
            
    except Exception as e:
        print(f"❌ Error processing file {file_path}: {e}")
        return ""

# --- الدوال الفرعية ---
def _read_pdf(path):
    try:
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content: text += content + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

def _read_image(path):
    try:
        image = Image.open(path)
        text = pytesseract.image_to_string(image, config='--psm 3')
        return text.strip()
    except Exception as e:
        return f"Error reading Image: {e}"

def _read_tabular_data(path, ext):
    print(f"📊 Processing Tabular Data: {path}...")
    try:
        if ext == 'csv':
            df = pd.read_csv(path)
        else:
            df = pd.read_excel(path)
        
        # تحويل الجدول لنص منسق (Markdown Table) عشان الـ LLM يفهمه بسهولة
        return df.to_markdown(index=False)
    except Exception as e:
        return f"Error reading Excel/CSV: {e}"