from sklearn.cluster import KMeans

from sklearn.pipeline import Pipeline


def get_clustering_model(
    preprocessor,
    n_clusters=3
):
    """
    Return K-Means clustering pipeline.
    """

    model = KMeans(
        n_clusters=n_clusters,
        random_state=42,
        n_init=10
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model)
        ]
    )

    return pipeline