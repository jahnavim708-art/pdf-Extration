import pandas as pd

from utils.pdf_detector import is_scanned_pdf
from utils.table_cleaner import clean_tables
from utils.merger import merge_tables

from extractors.camelot_lattice import extract as lattice_extract
from extractors.camelot_stream import extract as stream_extract
from extractors.pdfplumber_extractor import extract as plumber_extract
from extractors.ocr_extractor import extract as ocr_extract


PDF_PATH = r"C:\Users\Hello\Downloads\table.pdf"


def run_pipeline(pdf_path):

    all_tables = []

    scanned = is_scanned_pdf(pdf_path)

    if scanned:

        print("Scanned PDF detected")
        all_tables.extend(
            ocr_extract(pdf_path)
        )

    else:

        print("Digital PDF detected")

        all_tables.extend(
            lattice_extract(pdf_path)
        )

        if not all_tables:
            all_tables.extend(
                stream_extract(pdf_path)
            )

        if not all_tables:
            all_tables.extend(
                plumber_extract(pdf_path)
            )

    all_tables = clean_tables(
        all_tables
    )

    final_df = merge_tables(
        all_tables
    )

    return final_df


if __name__ == "__main__":

    df = run_pipeline(PDF_PATH)

    if df is not None:

        df.to_excel(
            "final_output.xlsx",
            index=False
        )

        df.to_csv(
            "final_output.csv",
            index=False
        )

        print("Output saved")

    else:

        print("No tables found")