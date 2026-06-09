import pdfplumber
import pandas as pd

pdf_path = r"C:\Users\Hello\Downloads\table.pdf"
output_csv = "table.csv"

all_rows = []
header = None

with pdfplumber.open(pdf_path) as pdf:

    for page in pdf.pages:

        tables = page.extract_tables()

        for table in tables:

            if not table or len(table) < 2:
                continue

            # Set header only once
            if header is None:
                header = table[0]

            rows = table[1:]

            for row in rows:

                if not any(row):
                    continue

                # fix row length mismatch
                while len(row) < len(header):
                    row.append("")

                all_rows.append(row[:len(header)])

if all_rows and header:

    df = pd.DataFrame(all_rows, columns=header)
    df.to_csv(output_csv, index=False)

    print(f"CSV created successfully: {output_csv}")

else:
    print("No table found in PDF")