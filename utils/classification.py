from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.pipeline import Pipeline


def get_classification_model(
    algorithm,
    preprocessor
):
    """
    Return selected classification model.
    """

    if algorithm == "Logistic Regression":

        model = LogisticRegression(
            max_iter=1000
        )

    elif algorithm == "Decision Tree":

        model = DecisionTreeClassifier(
            random_state=42
        )

    elif algorithm == "Random Forest":

        model = RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            n_jobs=-1,
            random_state=42
        )

    elif algorithm == "Naive Bayes":

        model = GaussianNB()

    else:

        raise ValueError(
            "Unsupported classification algorithm."
        )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    return pipeline