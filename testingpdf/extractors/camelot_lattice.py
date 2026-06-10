import camelot

def extract(pdf_path):
    try:
        tables = camelot.read_pdf(
            pdf_path,
            pages="all",
            flavor="lattice"
        )

        return [t.df for t in tables]

    except Exception as e:
        print("Camelot Lattice Error:", e)
        return []