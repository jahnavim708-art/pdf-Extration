import camelot

def extract(pdf_path):
    try:
        tables = camelot.read_pdf(
            pdf_path,
            pages="all",
            flavor="stream",
            edge_tol=500,
            row_tol=10
        )

        return [t.df for t in tables]

    except Exception as e:
        print("Camelot Stream Error:", e)
        return []