import streamlit as st
import pandas as pd

from database.database import (
    get_datasets,
    get_experiments,
    get_predictions
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="IntelliData AI Dashboard",
    page_icon="📊",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("📊 IntelliData AI Dashboard")

st.caption(
    "Unified overview of your data, machine learning experiments and predictions."
)


# ==================================================
# LOAD DATABASE DATA
# ==================================================

datasets = get_datasets()
experiments = get_experiments()
predictions = get_predictions()


# ==================================================
# CONVERT TO DATAFRAMES
# ==================================================

datasets_df = pd.DataFrame(
    datasets,
    columns=[
        "ID",
        "Filename",
        "Rows",
        "Columns",
        "Uploaded At"
    ]
)


experiments_df = pd.DataFrame(
    experiments,
    columns=[
        "ID",
        "Dataset",
        "Problem Type",
        "Algorithm",
        "Target",
        "Score",
        "Created At"
    ]
)


predictions_df = pd.DataFrame(
    predictions,
    columns=[
        "ID",
        "Model Type",
        "Target",
        "Prediction",
        "Confidence",
        "Created At"
    ]
)


# ==================================================
# KPI CALCULATIONS
# ==================================================

total_datasets = len(
    datasets_df
)

total_experiments = len(
    experiments_df
)

total_predictions = len(
    predictions_df
)


if not experiments_df.empty:

    best_score = experiments_df[
        "Score"
    ].max()

else:

    best_score = 0


# ==================================================
# KPI CARDS
# ==================================================

st.subheader(
    "📌 Key Performance Indicators"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "📁 Total Datasets",
        total_datasets
    )


with col2:

    st.metric(
        "🤖 ML Experiments",
        total_experiments
    )


with col3:

    st.metric(
        "🔮 Predictions",
        total_predictions
    )


with col4:

    if best_score <= 1:

        score_display = (
            f"{best_score:.2%}"
        )

    else:

        score_display = (
            f"{best_score:.2f}%"
        )

    st.metric(
        "🏆 Best Score",
        score_display
    )


# ==================================================
# MODEL PERFORMANCE
# ==================================================

st.markdown("---")

st.subheader(
    "🤖 Model Performance"
)


if not experiments_df.empty:

    performance_df = (
        experiments_df
        .groupby("Algorithm")["Score"]
        .mean()
        .sort_values(
            ascending=False
        )
    )

    st.bar_chart(
        performance_df
    )


    # ----------------------------------------------
    # BEST ALGORITHM
    # ----------------------------------------------

    best_algorithm = (
        performance_df.idxmax()
    )

    best_algorithm_score = (
        performance_df.max()
    )


    col1, col2 = st.columns(2)


    with col1:

        st.metric(
            "🥇 Best Algorithm",
            best_algorithm
        )


    with col2:

        if best_algorithm_score <= 1:

            display_score = (
                f"{best_algorithm_score:.2%}"
            )

        else:

            display_score = (
                f"{best_algorithm_score:.2f}%"
            )

        st.metric(
            "📈 Average Score",
            display_score
        )


else:

    st.info(
        "No ML experiments available yet."
    )


# ==================================================
# LATEST PREDICTION
# ==================================================

st.markdown("---")

st.subheader(
    "🔮 Latest Prediction"
)


if not predictions_df.empty:

    latest_prediction = (
        predictions_df.iloc[0]
    )


    prediction_value = (
        latest_prediction["Prediction"]
    )


    confidence = (
        latest_prediction["Confidence"]
    )


    # ----------------------------------------------
    # PREDICTION LABEL
    # ----------------------------------------------

    if str(prediction_value) == "1":

        prediction_label = (
            "Survived"
        )

    elif str(prediction_value) == "0":

        prediction_label = (
            "Not Survived"
        )

    else:

        prediction_label = str(
            prediction_value
        )


    # ----------------------------------------------
    # CONFIDENCE
    # ----------------------------------------------

    try:

        confidence_value = float(
            confidence
        )

        if confidence_value <= 1:

            confidence_value *= 100

        confidence_display = (
            f"{confidence_value:.2f}%"
        )

    except Exception:

        confidence_display = (
            "Not Available"
        )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🎯 Prediction",
            prediction_label
        )


    with col2:

        st.metric(
            "📊 Confidence",
            confidence_display
        )


    with col3:

        st.metric(
            "🎯 Target",
            str(
                latest_prediction["Target"]
            )
        )


    with col4:

        st.metric(
            "🧠 Model Type",
            str(
                latest_prediction["Model Type"]
            )
        )


    st.caption(
        f"Generated: {latest_prediction['Created At']}"
    )


else:

    st.info(
        "No predictions available yet. "
        "Go to the Prediction page and generate a prediction."
    )


# ==================================================
# DATASET QUALITY
# ==================================================

st.markdown("---")

st.subheader(
    "🧹 Dataset Overview"
)


if not datasets_df.empty:

    total_rows = int(
        datasets_df["Rows"].sum()
    )

    total_columns = int(
        datasets_df["Columns"].sum()
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "📁 Uploaded Datasets",
            len(datasets_df)
        )


    with col2:

        st.metric(
            "📊 Total Rows",
            f"{total_rows:,}"
        )


    with col3:

        st.metric(
            "📋 Total Columns",
            f"{total_columns:,}"
        )


else:

    st.info(
        "No datasets uploaded yet."
    )


# ==================================================
# EXPERIMENT HISTORY
# ==================================================

st.markdown("---")

st.subheader(
    "📈 Experiment History"
)


if not experiments_df.empty:

    history_df = experiments_df[
        [
            "Dataset",
            "Problem Type",
            "Algorithm",
            "Target",
            "Score",
            "Created At"
        ]
    ].copy()


    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No experiment history available."
    )


# ==================================================
# PREDICTION HISTORY
# ==================================================

st.markdown("---")

st.subheader(
    "🔮 Recent Predictions"
)


if not predictions_df.empty:

    recent_predictions = (
        predictions_df.head(10)
    )


    prediction_history = (
        recent_predictions[
            [
                "Model Type",
                "Target",
                "Prediction",
                "Confidence",
                "Created At"
            ]
        ]
    )


    st.dataframe(
        prediction_history,
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No predictions available yet."
    )


# ==================================================
# DATASET HISTORY
# ==================================================

st.markdown("---")

st.subheader(
    "📁 Uploaded Dataset History"
)


if not datasets_df.empty:

    st.dataframe(
        datasets_df[
            [
                "Filename",
                "Rows",
                "Columns",
                "Uploaded At"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No datasets uploaded yet."
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "IntelliData AI • Intelligent Data Analytics & Machine Learning Platform"
)