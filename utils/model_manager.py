import os
import joblib


MODEL_DIRECTORY = "models"


def save_model(
    model,
    filename
):
    """
    Save trained model.
    """

    os.makedirs(
        MODEL_DIRECTORY,
        exist_ok=True
    )

    path = os.path.join(
        MODEL_DIRECTORY,
        filename
    )

    joblib.dump(
        model,
        path
    )

    return path


def load_model(filename):
    """
    Load saved model.
    """

    path = os.path.join(
        MODEL_DIRECTORY,
        filename
    )

    if not os.path.exists(path):

        raise FileNotFoundError(
            f"Model not found: {path}"
        )

    return joblib.load(path)