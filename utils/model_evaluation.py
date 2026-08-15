from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

import numpy as np


def evaluate_classification(
    y_true,
    y_pred
):
    """
    Calculate classification metrics.
    """

    return {
        "Accuracy": accuracy_score(
            y_true,
            y_pred
        ),

        "Precision": precision_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ),

        "Recall": recall_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        ),

        "F1 Score": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0
        )
    }


def evaluate_regression(
    y_true,
    y_pred
):
    """
    Calculate regression metrics.
    """

    mse = mean_squared_error(
        y_true,
        y_pred
    )

    rmse = np.sqrt(mse)

    return {
        "MAE": mean_absolute_error(
            y_true,
            y_pred
        ),

        "MSE": mse,

        "RMSE": rmse,

        "R2 Score": r2_score(
            y_true,
            y_pred
        )
    }