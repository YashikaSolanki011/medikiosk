import re
from datetime import datetime
from typing import Dict, List, Any
from PIL import Image
import pytesseract

LAB_REFERENCE_RANGES = {
    "Hemoglobin": {"min": 12.0, "max": 17.0, "unit": "g/dL", "patterns": [r"hemoglobin|haemoglobin|hb"]},
    "TLC (WBC Count)": {"min": 4000, "max": 11000, "unit": "/mcL", "patterns": [r"tlc|total leukocyte count|wbc count|wbc"]},
    "Platelets": {"min": 150000, "max": 450000, "unit": "/mcL", "patterns": [r"platelet|platelet count|plt"]},
    "Fasting Blood Sugar": {"min": 70.0, "max": 100.0, "unit": "mg/dL", "patterns": [r"fasting blood sugar|fbs|glucose fasting"]},
    "Postprandial Blood Sugar": {"min": 70.0, "max": 140.0, "unit": "mg/dL", "patterns": [r"post prandial|ppbs|glucose post prandial"]},
    "HbA1c": {"min": 4.0, "max": 5.7, "unit": "%", "patterns": [r"hba1c|glycated hemoglobin"]},
    "Serum Creatinine": {"min": 0.6, "max": 1.3, "unit": "mg/dL", "patterns": [r"serum creatinine|creatinine|s\.?\s*creat"]},
    "Blood Urea": {"min": 15.0, "max": 45.0, "unit": "mg/dL", "patterns": [r"blood urea|urea"]},
    "Total Bilirubin": {"min": 0.2, "max": 1.2, "unit": "mg/dL", "patterns": [r"total bilirubin|s\.?\s*bilirubin"]},
    "SGPT (ALT)": {"min": 7.0, "max": 56.0, "unit": "U/L", "patterns": [r"sgpt|alt|alanine transaminase"]},
    "SGOT (AST)": {"min": 10.0, "max": 40.0, "unit": "U/L", "patterns": [r"sgot|ast|aspartate aminotransferase"]}
}

COMMON_CONDITIONS = [
    "Hypertension", "HTN", "Type 2 Diabetes", "T2DM", "Diabetes Mellitus", "Hypothyroidism",
    "Asthma", "COPD", "Coronary Artery Disease", "CAD", "Tuberculosis", "TB",
    "GERD", "Chronic Kidney Disease", "CKD", "Osteoarthritis"
]

FREQUENCY_PATTERNS = ["1-0-1", "1-1-1", "1-0-0", "0-0-1", "0-1-0", "od", "bd", "tds", "sos", "hs"]

def extract_text_from_image(image_path: str) -> str:
    try:
        img = Image.open(image_path)
        return pytesseract.image_to_string(img)
    except Exception as e:
        return f"[OCR Error: {str(e)}]"

def parse_clinical_entities(text: str, doc_name: str = "Document") -> Dict[str, Any]:
    lines = text.split("\n")
    dates = re.findall(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)
    primary_date = dates[0] if dates else datetime.today().strftime("%d/%m/%Y")

    labs = []
    for lab_name, info in LAB_REFERENCE_RANGES.items():
        for line in lines:
            for pat in info["patterns"]:
                match = re.search(pat, line, re.IGNORECASE)
                if match:
                    num_match = re.search(r"(\d+(?:\.\d+)?)", line[match.end():])
                    if num_match:
                        try:
                            val = float(num_match.group(1))
                            is_abnormal = (val < info["min"]) or (val > info["max"])
                            status = "HIGH" if val > info["max"] else ("LOW" if val < info["min"] else "NORMAL")
                            labs.append({
                                "parameter": lab_name,
                                "value": val,
                                "unit": info["unit"],
                                "reference_range": f"{info['min']} - {info['max']} {info['unit']}",
                                "status": status,
                                "is_abnormal": is_abnormal
                            })
                            break
                        except ValueError:
                            continue
            if any(l["parameter"] == lab_name for l in labs):
                break

    meds = []
    for line in lines:
        clean = line.strip()
        if re.search(r"\b(?:tab|tablet|cap|capsule|syr|inj)\b", clean, re.IGNORECASE) or re.search(r"\b\d+\s*mg\b", clean, re.IGNORECASE):
            freq = "As directed"
            for f in FREQUENCY_PATTERNS:
                if re.search(rf"\b{re.escape(f)}\b", clean, re.IGNORECASE):
                    freq = f.upper()
                    break
            meds.append({"prescription_line": clean, "frequency": freq})

    diagnoses = [c for c in COMMON_CONDITIONS if re.search(rf"\b{re.escape(c)}\b", text, re.IGNORECASE)]

    return {
        "document_name": doc_name,
        "date": primary_date,
        "investigations": labs,
        "medications": meds,
        "documented_diagnoses": list(set(diagnoses)),
        "abnormal_count": sum(1 for l in labs if l["is_abnormal"])
    }

def process_medical_document(image_path: str = None, raw_text: str = None, doc_name: str = "Document") -> Dict[str, Any]:
    if image_path:
        text = extract_text_from_image(image_path)
    elif raw_text:
        text = raw_text
    else:
        text = ""
    return parse_clinical_entities(text, doc_name=doc_name)
