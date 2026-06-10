import pdfplumber
import pandas as pd

def extract(pdf_path):

    results = []

    try:
        with pdfplumber.open(pdf_path) as pdf:

            for page in pdf.pages:

                table = page.extract_table()

                if table:
                    results.append(
                        pd.DataFrame(table)
                    )

    except Exception as e:
        print("pdfplumber Error:", e)

    return results