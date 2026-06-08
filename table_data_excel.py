import pdfplumber
import pandas as pd
import os
from openpyxl.utils import get_column_letter

# ==========================================
# PDF FILE PATH
# ==========================================
pdf_location = r"C:\Users\Hello\Downloads\sample-tables.pdf"

# ==========================================
# OUTPUT FOLDER
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

                excel_filename = f"page_{page_num}_table_{table_count}.xlsx"
                excel_path = os.path.join(output_folder, excel_filename)

                # Save to Excel
                with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
                    df.to_excel(
                        writer,
                        sheet_name="Table",
                        index=False
                    )

                    worksheet = writer.sheets["Table"]

                    # Auto-fit column widths
                    for column in worksheet.columns:

                        max_length = 0
                        column_letter = get_column_letter(
                            column[0].column
                        )

                        for cell in column:
                            try:
                                if cell.value is not None:
                                    max_length = max(
                                        max_length,
                                        len(str(cell.value))
                                    )
                            except Exception:
                                pass

                        adjusted_width = min(max_length + 2, 50)
                        worksheet.column_dimensions[
                            column_letter
                        ].width = adjusted_width

                print(f"Saved: {excel_filename}")

                table_count += 1

            except Exception as e:
                print(f"Error processing table: {e}")

print("\n===================================")
print(f"Total Tables Extracted: {table_count - 1}")
print(f"Excel Files Saved In: {output_folder}")
print("Extraction Completed Successfully!")
print("===================================")