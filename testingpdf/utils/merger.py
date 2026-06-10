import pandas as pd

def merge_tables(tables):

    if not tables:
        return None

    return pd.concat(
        tables,
        ignore_index=True
    )