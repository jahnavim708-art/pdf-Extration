def clean_tables(tables):

    cleaned = []

    for df in tables:

        if df is None:
            continue

        if df.empty:
            continue

        df = df.dropna(how="all")
        df = df.reset_index(drop=True)

        cleaned.append(df)

    return cleaned