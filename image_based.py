import fitz  # PyMuPDF
import os
import pandas as pd
from paddleocr import PaddleOCR
from PIL import Image
import numpy as np

# ==========================================
# PDF PATH
# ==========================================
pdf_path = r"C:\Users\Hello\Downloads\sample.pdf"

# ==========================================
# OUTPUT FOLDER
# ==========================================
output_folder = os.path.join(
    os.path.dirname(pdf_path),
    "ocr_tables_output"
)

os.makedirs(output_folder, exist_ok=True)

# ==========================================
# INIT OCR ENGINE
# ==========================================
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# ==========================================
# OPEN PDF
# ==========================================
doc = fitz.open(pdf_path)

print(f"Total Pages: {len(doc)}")

table_count = 1

# ==========================================
# PROCESS EACH PAGE
# ==========================================
for page_num in range(len(doc)):

    page = doc[page_num]

    # Convert PDF page → image
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    img_path = os.path.join(output_folder, f"page_{page_num+1}.png")
    pix.save(img_path)

    print(f"\nProcessing Page {page_num+1}...")

    # Run OCR
    result = ocr.ocr(img_path)

    # Extract text lines
    rows = []

    if result and result[0]:

        for line in result[0]:
            text = line[1][0]   # detected text
            rows.append([text])

    # Convert OCR output to DataFrame
    df = pd.DataFrame(rows)

    # Save Excel
    excel_file = os.path.join(
        output_folder,
        f"page_{page_num+1}_table_{table_count}.xlsx"
    )

    df.to_excel(excel_file, index=False, header=False)

    print(f"Saved: {excel_file}")

    table_count += 1

print("\n===================================")
print(f"Total Pages Processed: {len(doc)}")
print(f"Files saved in: {output_folder}")
print("OCR Extraction Completed Successfully!")
print("===================================")