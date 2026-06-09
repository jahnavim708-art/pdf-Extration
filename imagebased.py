import fitz
import requests
import os
import pandas as pd

pdf_path = r"C:\Users\Hello\Downloads\sample.pdf"

output_folder = os.path.join(os.path.dirname(pdf_path), "cloud_tables")
os.makedirs(output_folder, exist_ok=True)

API_KEY = "helloworld"  # free demo key

doc = fitz.open(pdf_path)

table_count = 1

for i, page in enumerate(doc):

    print(f"Processing page {i+1}")

    pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
    img_path = os.path.join(output_folder, f"page_{i+1}.png")
    pix.save(img_path)

    # OCR API call
    with open(img_path, "rb") as f:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"filename": f},
            data={"apikey": API_KEY, "language": "eng"}
        )

    result = response.json()

    text = result["ParsedResults"][0]["ParsedText"]

    #rows = [line.split() for line in text.split("\n") if line.strip()]
    rows = []

    for line in text.split("\n"):
        line = line.strip()
        if line:
            rows.append([line])

    df = pd.DataFrame(rows)

    df = pd.DataFrame(rows)

    file_path = os.path.join(output_folder, f"page_{i+1}_table_{table_count}.xlsx")

    df.to_excel(file_path, index=False, header=False)

    print("Saved:", file_path)

    table_count += 1

print("DONE")