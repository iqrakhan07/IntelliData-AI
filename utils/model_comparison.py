from sklearn.model_selection import train_test_split

from utils.preprocessing import prepare_features

from utils.regression import get_regression_model
from utils.classification import get_classification_model

from utils.model_evaluation import (
    evaluate_regression,
    evaluate_classification
)


def compare_regression_models(df, target):

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    algorithms = [
        "Linear Regression",
        "Random Forest"
    ]

    results = []

    for algorithm in algorithms:

        preprocessor = prepare_features(X_train)

        model = get_regression_model(
            algorithm,
            preprocessor
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        metrics = evaluate_regression(
            y_test,
            predictions
        )

        results.append({
            "Algorithm": algorithm,
            "MAE": metrics["MAE"],
            "RMSE": metrics["RMSE"],
            "R2 Score": metrics["R2 Score"],
            "Model": model
        })

    return results


def compare_classification_models(df, target):

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    algorithms = [
        "Logistic Regression",
        "Decision Tree",
        "Random Forest",
        "Naive Bayes"
    ]

    results = []

    for algorithm in algorithms:

        preprocessor = prepare_features(X_train)

        model = get_classification_model(
            algorithm,
            preprocessor
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(
            X_test
        )

        metrics = evaluate_classification(
            y_test,
            predictions
        )

        results.append({
            "Algorithm": algorithm,
            "Accuracy": metrics["Accuracy"],
            "Precision": metrics["Precision"],
            "Recall": metrics["Recall"],
            "F1 Score": metrics["F1 Score"],
            "Model": model
        })

    return results