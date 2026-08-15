import pandas as pd


def load_data(uploaded_file):
    """
    Load CSV or Excel file into a Pandas DataFrame.
    """

    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)

    else:
        raise ValueError(
            "Unsupported file format. Please upload CSV or Excel."
        )

    return df