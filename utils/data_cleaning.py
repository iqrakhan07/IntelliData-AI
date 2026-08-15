import pandas as pd


def get_missing_values(df):
    """
    Return missing value count for each column.
    """
    return df.isnull().sum()


def get_duplicate_count(df):
    """
    Return number of duplicate rows.
    """
    return df.duplicated().sum()


def remove_duplicates(df):
    """
    Remove duplicate rows.
    """
    return df.drop_duplicates()


def fill_missing_numeric(df):
    """
    Fill missing numerical values with median.
    """

    df = df.copy()

    numeric_columns = df.select_dtypes(
        include=["number"]
    ).columns

    for column in numeric_columns:
        df[column] = df[column].fillna(
            df[column].median()
        )

    return df


def fill_missing_categorical(df):
    """
    Fill missing categorical values with mode.
    """

    df = df.copy()

    categorical_columns = df.select_dtypes(
        include=["object", "category"]
    ).columns

    for column in categorical_columns:

        if not df[column].mode().empty:
            df[column] = df[column].fillna(
                df[column].mode()[0]
            )

    return df