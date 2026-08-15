import streamlit as st
import pandas as pd

from sklearn.model_selection import train_test_split

from utils.preprocessing import prepare_features

from utils.regression import (
    get_regression_model
)

from utils.classification import (
    get_classification_model
)

from utils.clustering import (
    get_clustering_model
)

from utils.model_evaluation import (
    evaluate_regression,
    evaluate_classification
)

from utils.model_comparison import (
    compare_regression_models,
    compare_classification_models
)

from utils.model_manager import (
    save_model
)

from database.database import (
    save_experiment
)


# ==================================================
# PAGE TITLE
# ==================================================

st.title("🤖 Machine Learning Studio")


# ==================================================
# CHECK DATASET
# ==================================================

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset first."
    )

    st.stop()


df = st.session_state["df"].copy()


# ==================================================
# LIMIT DATASET SIZE
# ==================================================

MAX_ROWS = 50000

if len(df) > MAX_ROWS:

    st.warning(
        f"Dataset contains {len(df):,} rows. "
        f"Using the first {MAX_ROWS:,} rows "
        f"for faster development."
    )

    df = df.head(MAX_ROWS).copy()


# ==================================================
# DATASET PREVIEW
# ==================================================

st.subheader("📊 Dataset")

st.dataframe(
    df.head(10),
    use_container_width=True
)


# ==================================================
# PROBLEM TYPE
# ==================================================

st.markdown("---")

problem_type = st.selectbox(
    "Select Machine Learning Problem",
    [
        "Regression",
        "Classification",
        "Clustering"
    ]
)


# ==================================================
# REGRESSION
# ==================================================

if problem_type == "Regression":

    st.subheader(
        "📈 Regression"
    )


    algorithm = st.selectbox(
        "Select Algorithm",
        [
            "Linear Regression",
            "Random Forest"
        ],
        key="regression_algorithm"
    )


    target = st.selectbox(
        "Select Target Column",
        df.columns,
        key="regression_target"
    )


    st.info(
        f"Target column: {target}"
    )


    if st.button(
        "🚀 Train Regression Model"
    ):

        try:

            # ------------------------------------------
            # FEATURES AND TARGET
            # ------------------------------------------

            X = df.drop(
                columns=[target]
            )

            y = df[target]


            # ------------------------------------------
            # VALIDATE TARGET
            # ------------------------------------------

            if not pd.api.types.is_numeric_dtype(y):

                st.error(
                    "Regression target must be numerical."
                )

                st.stop()


            # ------------------------------------------
            # TRAIN TEST SPLIT
            # ------------------------------------------

            X_train, X_test, y_train, y_test = (
                train_test_split(
                    X,
                    y,
                    test_size=0.2,
                    random_state=42
                )
            )


            # ------------------------------------------
            # PREPROCESSOR
            # ------------------------------------------

            preprocessor = prepare_features(
                X_train
            )


            # ------------------------------------------
            # MODEL
            # ------------------------------------------

            model = get_regression_model(
                algorithm,
                preprocessor
            )


            # ------------------------------------------
            # TRAIN
            # ------------------------------------------

            with st.spinner(
                f"Training {algorithm} "
                f"on {len(X_train):,} records..."
            ):

                model.fit(
                    X_train,
                    y_train
                )


            # ------------------------------------------
            # PREDICTION
            # ------------------------------------------

            predictions = model.predict(
                X_test
            )


            # ------------------------------------------
            # EVALUATION
            # ------------------------------------------

            metrics = evaluate_regression(
                y_test,
                predictions
            )


            # ------------------------------------------
            # SAVE EXPERIMENT
            # ------------------------------------------

            save_experiment(
                st.session_state.get(
                    "filename",
                    "Unknown"
                ),
                "Regression",
                algorithm,
                target,
                metrics["R2 Score"]
            )


            # ------------------------------------------
            # SUCCESS
            # ------------------------------------------

            st.success(
                "Model trained successfully!"
            )


            # ------------------------------------------
            # METRICS
            # ------------------------------------------

            st.subheader(
                "📊 Model Performance"
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "MAE",
                    f"{metrics['MAE']:.4f}"
                )


            with col2:

                st.metric(
                    "RMSE",
                    f"{metrics['RMSE']:.4f}"
                )


            with col3:

                st.metric(
                    "R² Score",
                    f"{metrics['R2 Score']:.4f}"
                )


            # ------------------------------------------
            # SAVE MODEL
            # ------------------------------------------

            model_path = save_model(
                model,
                "latest_regression_model.pkl"
            )


            st.success(
                f"Model saved: {model_path}"
            )


            # ------------------------------------------
            # SESSION STATE
            # ------------------------------------------

            st.session_state[
                "trained_model"
            ] = model

            st.session_state[
                "problem_type"
            ] = "Regression"

            st.session_state[
                "target_column"
            ] = target


        except Exception as e:

            st.error(
                f"Training error: {e}"
            )


# ==================================================
# CLASSIFICATION
# ==================================================

elif problem_type == "Classification":

    st.subheader(
        "🟢 Classification"
    )


    # ----------------------------------------------
    # TARGET
    # ----------------------------------------------

    target = st.selectbox(
        "Select Target Column",
        df.columns,
        key="classification_target"
    )


    st.info(
        f"Target column: {target}"
    )


    # ----------------------------------------------
    # ALGORITHM
    # ----------------------------------------------

    algorithm = st.selectbox(
        "Select Algorithm",
        [
            "Logistic Regression",
            "Decision Tree",
            "Random Forest",
            "Naive Bayes"
        ],
        key="classification_algorithm"
    )


    # ----------------------------------------------
    # TRAIN MODEL
    # ----------------------------------------------

    if st.button(
        "🚀 Train Classification Model"
    ):

        try:

            # ------------------------------------------
            # FEATURES AND TARGET
            # ------------------------------------------

            X = df.drop(
                columns=[target]
            )

            y = df[target]


            # ------------------------------------------
            # VALIDATE TARGET
            # ------------------------------------------

            if y.isnull().any():

                st.error(
                    "Target column contains missing values. "
                    "Please clean the target column first."
                )

                st.stop()


            if y.nunique() < 2:

                st.error(
                    "Target must contain at least two classes."
                )

                st.stop()


            # ------------------------------------------
            # TRAIN TEST SPLIT
            # ------------------------------------------

            X_train, X_test, y_train, y_test = (
                train_test_split(
                    X,
                    y,
                    test_size=0.2,
                    random_state=42,
                    stratify=y
                )
            )


            # ------------------------------------------
            # PREPROCESSOR
            # ------------------------------------------

            preprocessor = prepare_features(
                X_train
            )


            # ------------------------------------------
            # MODEL
            # ------------------------------------------

            model = get_classification_model(
                algorithm,
                preprocessor
            )


            # ------------------------------------------
            # TRAIN
            # ------------------------------------------

            with st.spinner(
                f"Training {algorithm} "
                f"on {len(X_train):,} records..."
            ):

                model.fit(
                    X_train,
                    y_train
                )


            # ------------------------------------------
            # PREDICTION
            # ------------------------------------------

            predictions = model.predict(
                X_test
            )


            # ------------------------------------------
            # EVALUATION
            # ------------------------------------------

            metrics = evaluate_classification(
                y_test,
                predictions
            )


            # ------------------------------------------
            # SAVE EXPERIMENT
            # ------------------------------------------

            save_experiment(
                st.session_state.get(
                    "filename",
                    "Unknown"
                ),
                "Classification",
                algorithm,
                target,
                metrics["F1 Score"]
            )


            # ------------------------------------------
            # SUCCESS
            # ------------------------------------------

            st.success(
                "Model trained successfully!"
            )


            # ------------------------------------------
            # METRICS
            # ------------------------------------------

            st.subheader(
                "📊 Model Performance"
            )


            col1, col2, col3, col4 = (
                st.columns(4)
            )


            with col1:

                st.metric(
                    "Accuracy",
                    f"{metrics['Accuracy']:.4f}"
                )


            with col2:

                st.metric(
                    "Precision",
                    f"{metrics['Precision']:.4f}"
                )


            with col3:

                st.metric(
                    "Recall",
                    f"{metrics['Recall']:.4f}"
                )


            with col4:

                st.metric(
                    "F1 Score",
                    f"{metrics['F1 Score']:.4f}"
                )


            # ------------------------------------------
            # SAVE MODEL
            # ------------------------------------------

            model_path = save_model(
                model,
                "latest_classification_model.pkl"
            )


            st.success(
                f"Model saved: {model_path}"
            )


            # ------------------------------------------
            # SESSION STATE
            # ------------------------------------------

            st.session_state[
                "trained_model"
            ] = model

            st.session_state[
                "problem_type"
            ] = "Classification"

            st.session_state[
                "target_column"
            ] = target


        except Exception as e:

            st.error(
                f"Training error: {e}"
            )


# ==================================================
# CLUSTERING
# ==================================================

else:

    st.subheader(
        "🔵 K-Means Clustering"
    )


    numeric_columns = (
        df.select_dtypes(
            include=["number"]
        ).columns.tolist()
    )


    if len(numeric_columns) < 2:

        st.error(
            "At least two numerical columns "
            "are required for clustering."
        )

        st.stop()


    selected_columns = st.multiselect(
        "Select Features",
        numeric_columns,
        default=numeric_columns[:2],
        key="clustering_features"
    )


    n_clusters = st.slider(
        "Number of Clusters",
        min_value=2,
        max_value=10,
        value=3
    )


    if st.button(
        "🚀 Run K-Means"
    ):

        try:

            if len(selected_columns) < 2:

                st.error(
                    "Please select at least two features."
                )

                st.stop()


            X = df[selected_columns]


            preprocessor = prepare_features(
                X
            )


            model = get_clustering_model(
                preprocessor,
                n_clusters
            )


            with st.spinner(
                "Creating clusters..."
            ):

                model.fit(X)


            clusters = model.predict(
                X
            )


            result = df.copy()

            result["Cluster"] = clusters


            st.success(
                "Clustering completed!"
            )


            st.subheader(
                "📊 Cluster Results"
            )


            st.dataframe(
                result,
                use_container_width=True
            )


            st.subheader(
                "Cluster Distribution"
            )


            st.bar_chart(
                result[
                    "Cluster"
                ].value_counts()
            )


            model_path = save_model(
                model,
                "latest_clustering_model.pkl"
            )


            st.success(
                f"Model saved: {model_path}"
            )


        except Exception as e:

            st.error(
                f"Clustering error: {e}"
            )


# ==================================================
# MODEL COMPARISON
# ==================================================

st.markdown("---")

st.header(
    "🏆 Model Comparison"
)


# ==================================================
# REGRESSION COMPARISON
# ==================================================

if problem_type == "Regression":

    comparison_target = st.selectbox(
        "Select Target for Model Comparison",
        df.columns,
        key="comparison_regression_target"
    )


    if st.button(
        "🔍 Compare Regression Models"
    ):

        try:

            with st.spinner(
                "Comparing regression models..."
            ):

                results = (
                    compare_regression_models(
                        df,
                        comparison_target
                    )
                )


            display_results = []


            for result in results:

                display_results.append({

                    "Algorithm":
                        result["Algorithm"],

                    "MAE":
                        round(
                            result["MAE"],
                            4
                        ),

                    "RMSE":
                        round(
                            result["RMSE"],
                            4
                        ),

                    "R² Score":
                        round(
                            result["R2 Score"],
                            4
                        )
                })


            results_df = pd.DataFrame(
                display_results
            )


            st.dataframe(
                results_df,
                use_container_width=True
            )


            best_result = max(
                results,
                key=lambda x:
                    x["R2 Score"]
            )


            st.success(
                f"🏆 Best Model: "
                f"{best_result['Algorithm']}"
            )


            st.metric(
                "Best R² Score",
                f"{best_result['R2 Score']:.4f}"
            )


            save_model(
                best_result["Model"],
                "best_model.pkl"
            )


            st.session_state[
                "best_model"
            ] = best_result["Model"]


            st.session_state[
                "best_model_type"
            ] = "Regression"


            st.session_state[
                "best_target"
            ] = comparison_target


        except Exception as e:

            st.error(
                f"Comparison error: {e}"
            )


# ==================================================
# CLASSIFICATION COMPARISON
# ==================================================

elif problem_type == "Classification":

    comparison_target = st.selectbox(
        "Select Target for Model Comparison",
        df.columns,
        key="comparison_classification_target"
    )


    if st.button(
        "🔍 Compare Classification Models"
    ):

        try:

            # ------------------------------------------
            # SAFETY CHECK
            # ------------------------------------------

            if comparison_target not in df.columns:

                st.error(
                    "Selected target column "
                    "does not exist."
                )

                st.stop()


            # ------------------------------------------
            # SHOW SELECTED TARGET
            # ------------------------------------------

            st.info(
                f"Classification target: "
                f"{comparison_target}"
            )


            # ------------------------------------------
            # COMPARE MODELS
            # ------------------------------------------

            with st.spinner(
                "Comparing classification models..."
            ):

                results = (
                    compare_classification_models(
                        df,
                        comparison_target
                    )
                )


            # ------------------------------------------
            # DISPLAY RESULTS
            # ------------------------------------------

            display_results = []


            for result in results:

                display_results.append({

                    "Algorithm":
                        result["Algorithm"],

                    "Accuracy":
                        round(
                            result["Accuracy"],
                            4
                        ),

                    "Precision":
                        round(
                            result["Precision"],
                            4
                        ),

                    "Recall":
                        round(
                            result["Recall"],
                            4
                        ),

                    "F1 Score":
                        round(
                            result["F1 Score"],
                            4
                        )
                })


            results_df = pd.DataFrame(
                display_results
            )


            st.dataframe(
                results_df,
                use_container_width=True
            )


            # ------------------------------------------
            # BEST MODEL
            # ------------------------------------------

            best_result = max(
                results,
                key=lambda x:
                    x["F1 Score"]
            )


            st.success(
                f"🏆 Best Model: "
                f"{best_result['Algorithm']}"
            )


            st.metric(
                "Best F1 Score",
                f"{best_result['F1 Score']:.4f}"
            )


            # ------------------------------------------
            # SAVE BEST MODEL
            # ------------------------------------------

            model_path = save_model(
                best_result["Model"],
                "best_model.pkl"
            )


            st.success(
                f"Best model saved: {model_path}"
            )


            # ------------------------------------------
            # SESSION STATE
            # ------------------------------------------

            st.session_state[
                "best_model"
            ] = best_result["Model"]


            st.session_state[
                "best_model_type"
            ] = "Classification"


            st.session_state[
                "best_target"
            ] = comparison_target


        except Exception as e:

            st.error(
                f"Comparison error: {e}"
            )


# ==================================================
# END
# ==================================================

else:

    st.info(
        "Model comparison is currently "
        "available for Regression "
        "and Classification."
    )