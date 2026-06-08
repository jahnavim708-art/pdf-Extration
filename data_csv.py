import pdfplumber
import pandas as pd
import os

# ==========================================
# PDF FILE PATH
# ==========================================
pdf_location = r"C:\Users\Hello\Downloads\sample-tables.pdf"

# ==========================================
# OUTPUT FOLDER FOR CSV FILES
# ==========================================
output_folder = os.path.join(
    os.path.dirname(pdf_location),
    "pdf_tables"
)

os.makedirs(output_folder, exist_ok=True)

# ==========================================
# EXTRACT TABLES
# ==========================================
table_count = 1

with pdfplumber.open(pdf_location) as pdf:

    print(f"Total Pages: {len(pdf.pages)}")

    for page_num, page in enumerate(pdf.pages, start=1):

        print(f"\nProcessing Page {page_num}...")

        tables = page.extract_tables()

        if not tables:
            print("No tables found on this page.")
            continue

        for table in tables:

            if not table or len(table) < 2:
                continue

            try:
                # First row as header
                header = table[0]
                data = table[1:]

                df = pd.DataFrame(data, columns=header)

                csv_filename = f"page_{page_num}_table_{table_count}.csv"
                csv_path = os.path.join(output_folder, csv_filename)

                df.to_csv(csv_path, index=False, encoding="utf-8-sig")

                print(f"Saved: {csv_filename}")

                table_count += 1

            except Exception as e:
                print(f"Error processing table: {e}")

print("\n===================================")
print(f"Total Tables Extracted: {table_count - 1}")
print(f"CSV Files Saved In: {output_folder}")
print("Extraction Completed Successfully!")
print("===================================")