import pandas as pd
import numpy as np


def generate_dataset_insights(df):
    """
    Generate automatic insights from a dataset.
    """

    insights = []

    rows, columns = df.shape

    # ---------------------------------------------
    # BASIC DATASET INFORMATION
    # ---------------------------------------------

    insights.append(
        f"The dataset contains {rows:,} rows "
        f"and {columns} columns."
    )

    # ---------------------------------------------
    # NUMERICAL / CATEGORICAL FEATURES
    # ---------------------------------------------

    numerical_columns = df.select_dtypes(
        include=np.number
    ).columns.tolist()

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    insights.append(
        f"There are {len(numerical_columns)} "
        f"numerical features and "
        f"{len(categorical_columns)} categorical features."
    )

    # ---------------------------------------------
    # MISSING VALUES
    # ---------------------------------------------

    missing = df.isnull().sum()

    missing = missing[
        missing > 0
    ].sort_values(
        ascending=False
    )

    if not missing.empty:

        column = missing.index[0]
        count = int(missing.iloc[0])

        percentage = (
            count / rows
        ) * 100

        insights.append(
            f"The column '{column}' has the "
            f"highest number of missing values: "
            f"{count:,} ({percentage:.2f}%)."
        )

    else:

        insights.append(
            "The dataset contains no missing values."
        )

    # ---------------------------------------------
    # DUPLICATES
    # ---------------------------------------------

    duplicate_count = int(
        df.duplicated().sum()
    )

    if duplicate_count > 0:

        insights.append(
            f"The dataset contains "
            f"{duplicate_count:,} duplicate rows."
        )

    else:

        insights.append(
            "No duplicate rows were detected."
        )

    # ---------------------------------------------
    # NUMERICAL INSIGHTS
    # ---------------------------------------------

    if numerical_columns:

        numeric_df = df[
            numerical_columns
        ]

        variances = numeric_df.var(
            numeric_only=True
        ).sort_values(
            ascending=False
        )

        if not variances.empty:

            highest_variance = (
                variances.index[0]
            )

            insights.append(
                f"'{highest_variance}' has the "
                f"highest variance among the "
                f"numerical features."
            )

        means = numeric_df.mean(
            numeric_only=True
        )

        if not means.empty:

            highest_mean_column = (
                means.idxmax()
            )

            insights.append(
                f"'{highest_mean_column}' has the "
                f"highest average numerical value."
            )

    # ---------------------------------------------
    # CATEGORICAL INSIGHTS
    # ---------------------------------------------

    if categorical_columns:

        for column in categorical_columns:

            unique_count = (
                df[column]
                .nunique(
                    dropna=True
                )
            )

            if unique_count <= 10:

                insights.append(
                    f"'{column}' contains "
                    f"{unique_count} unique categories."
                )

    # ---------------------------------------------
    # HIGH CARDINALITY
    # ---------------------------------------------

    for column in categorical_columns:

        unique_count = (
            df[column]
            .nunique(
                dropna=True
            )
        )

        if unique_count > 50:

            insights.append(
                f"'{column}' has high cardinality "
                f"with {unique_count:,} unique values. "
                f"It may require special preprocessing."
            )

    return insights


def generate_ml_insights(
    algorithm,
    problem_type,
    score,
    target
):
    """
    Generate simple ML insights.
    """

    insights = []

    insights.append(
        f"{algorithm} was trained for "
        f"{problem_type.lower()}."
    )

    insights.append(
        f"The target variable is '{target}'."
    )

    if problem_type == "Classification":

        insights.append(
            f"The model achieved an evaluation "
            f"score of {score:.2%}."
        )

        if score >= 0.90:

            insights.append(
                "The model shows very strong "
                "performance on the test data."
            )

        elif score >= 0.75:

            insights.append(
                "The model shows good performance "
                "on the test data."
            )

        else:

            insights.append(
                "The model may require further "
                "feature engineering or tuning."
            )

    elif problem_type == "Regression":

        insights.append(
            f"The model achieved an R² score "
            f"of {score:.4f}."
        )

    return insights