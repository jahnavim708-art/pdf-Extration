import fitz
import requests
import os
import pandas as pd
import re

# ==========================================
# PDF PATH
# ==========================================
pdf_path = r"C:\Users\Hello\Downloads\sample.pdf"

# ==========================================
# OUTPUT FOLDER
# ==========================================
output_folder = os.path.join(
    os.path.dirname(pdf_path),
    "bank_statement_output"
)

os.makedirs(output_folder, exist_ok=True)

# ==========================================
# OCR API KEY
# ==========================================
API_KEY = "helloworld"

# ==========================================
# OPEN PDF
# ==========================================
doc = fitz.open(pdf_path)

all_transactions = []

# Match dates like:
# 01/05/2025
# 01-05-2025
date_pattern = r"\d{2}[/-]\d{2}[/-]\d{4}"

for page_no, page in enumerate(doc, start=1):

    print(f"Processing Page {page_no}")

    img_path = os.path.join(output_folder, f"page_{page_no}.png")

    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    pix.save(img_path)

    # OCR call
    with open(img_path, "rb") as f:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"filename": f},
            data={
                "apikey": API_KEY,
                "language": "eng"
            }
        )

    result = response.json()

    if "ParsedResults" not in result:
        print("OCR failed on page", page_no)
        continue

    text = result["ParsedResults"][0]["ParsedText"]

    # Uncomment for debugging
    # print(text)

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        # Keep rows starting with a date
        if not re.match(date_pattern, line):
            continue

        parts = line.split()

        # Need at least:
        # TxnDate ValueDate Description Amount Balance
        if len(parts) < 5:
            continue

        txn_date = parts[0]
        value_date = parts[1]

        # Last value = balance
        balance = parts[-1]

        # Second-last value = amount
        amount = parts[-2]

        description = " ".join(parts[2:-2])

        debit = ""
        credit = ""

        # Generic assumption:
        # negative amount => debit
        # positive amount => credit
        try:
            amt = float(amount.replace(",", ""))

            if amt < 0:
                debit = abs(amt)
            else:
                credit = amt

        except:
            credit = amount

        all_transactions.append([
            txn_date,
            value_date,
            description,
            debit,
            credit,
            balance
        ])

# ==========================================
# SAVE EXCEL
# ==========================================
columns = [
    "Txn Date",
    "Value Date",
    "Description / Ref No",
    "Debit",
    "Credit",
    "Balance"
]

df = pd.DataFrame(all_transactions, columns=columns)

excel_file = os.path.join(
    output_folder,
    "bank_statement.xlsx"
)

df.to_excel(excel_file, index=False)

print("\n===================================")
print("Excel Saved:")
print(excel_file)
print("===================================")