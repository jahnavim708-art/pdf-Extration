import fitz
import requests
import pandas as pd
import tempfile
import os

API_KEY = "YOUR_API_KEY"

def extract(pdf_path):

    results = []

    doc = fitz.open(pdf_path)

    for page in doc:

        with tempfile.NamedTemporaryFile(
            suffix=".png",
            delete=False
        ) as tmp:

            pix = page.get_pixmap(matrix=fitz.Matrix(2,2))
            pix.save(tmp.name)

            with open(tmp.name, "rb") as f:

                response = requests.post(
                    "https://api.ocr.space/parse/image",
                    files={"filename": f},
                    data={
                        "apikey": API_KEY,
                        "language": "eng"
                    }
                )

            os.remove(tmp.name)

        data = response.json()

        if "ParsedResults" not in data:
            continue

        text = data["ParsedResults"][0]["ParsedText"]

        rows = []

        for line in text.split("\n"):
            line = line.strip()

            if line:
                rows.append([line])

        if rows:
            results.append(
                pd.DataFrame(rows)
            )

    return results