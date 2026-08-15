import pandas as pd


def get_basic_statistics(df):
    """
    Generate descriptive statistics.
    """
    return df.describe(include="all").transpose()


def get_numeric_columns(df):
    """
    Return numerical columns.
    """
    return df.select_dtypes(
        include=["number"]
    ).columns.tolist()


def get_categorical_columns(df):
    """
    Return categorical columns.
    """
    return df.select_dtypes(
        include=["object", "category"]
    ).columns.tolist()


def get_correlation(df):
    """
    Calculate correlation between numerical columns.
    """

    numeric_df = df.select_dtypes(
        include=["number"]
    )

    return numeric_df.corr()