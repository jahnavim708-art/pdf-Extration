import fitz

def is_scanned_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    for page in doc:
        text = page.get_text().strip()

        if text:
            return False

    return True