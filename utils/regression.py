from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from sklearn.pipeline import Pipeline


def get_regression_model(
    algorithm,
    preprocessor
):
    """
    Return selected regression model.
    """

    if algorithm == "Linear Regression":

        model = LinearRegression()

    elif algorithm == "Random Forest":

        model = RandomForestRegressor(
            n_estimators=50,
            max_depth=10,
            n_jobs=-1,
         random_state=42
        )

    elif algorithm == "Random Forest":

         model = RandomForestRegressor(
             n_estimators=30,
             max_depth=8,
             n_jobs=-1,
             random_state=42
         )

    else:

        raise ValueError(
            "Unsupported regression algorithm."
        )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    return pipeline