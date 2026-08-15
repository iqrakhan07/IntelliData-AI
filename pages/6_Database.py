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
    page_title="Database - IntelliData AI",
    page_icon="🗄️",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("🗄️ IntelliData AI Database")

st.caption(
    "View datasets, machine learning experiments and prediction history."
)


# ==================================================
# REFRESH
# ==================================================

if st.button("🔄 Refresh Database"):

    st.rerun()


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
# DATABASE SUMMARY
# ==================================================

st.subheader(
    "📊 Database Summary"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "📁 Datasets",
        len(datasets_df)
    )


with col2:

    st.metric(
        "🤖 Experiments",
        len(experiments_df)
    )


with col3:

    st.metric(
        "🔮 Predictions",
        len(predictions_df)
    )


# ==================================================
# DATASETS
# ==================================================

st.markdown("---")

st.header(
    "📁 Uploaded Datasets"
)


if not datasets_df.empty:

    st.dataframe(
        datasets_df[
            [
                "ID",
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
        "No datasets have been uploaded yet."
    )


# ==================================================
# EXPERIMENTS
# ==================================================

st.markdown("---")

st.header(
    "🤖 Machine Learning Experiments"
)


if not experiments_df.empty:

    # ----------------------------------------------
    # BEST EXPERIMENT
    # ----------------------------------------------

    best_index = (
        experiments_df["Score"].idxmax()
    )

    best_experiment = (
        experiments_df.loc[
            best_index
        ]
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🏆 Best Algorithm",
            str(
                best_experiment["Algorithm"]
            )
        )


    with col2:

        best_score = float(
            best_experiment["Score"]
        )

        if best_score <= 1:

            score_display = (
                f"{best_score:.2%}"
            )

        else:

            score_display = (
                f"{best_score:.2f}%"
            )

        st.metric(
            "📈 Best Score",
            score_display
        )


    with col3:

        st.metric(
            "🎯 Target",
            str(
                best_experiment["Target"]
            )
        )


    st.markdown("### 📋 Experiment Records")


    st.dataframe(
        experiments_df[
            [
                "ID",
                "Dataset",
                "Problem Type",
                "Algorithm",
                "Target",
                "Score",
                "Created At"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No ML experiments found."
    )


# ==================================================
# PREDICTIONS
# ==================================================

st.markdown("---")

st.header(
    "🔮 Prediction History"
)


if not predictions_df.empty:

    # ----------------------------------------------
    # LATEST PREDICTION
    # ----------------------------------------------

    latest = predictions_df.iloc[0]


    prediction_value = (
        latest["Prediction"]
    )


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


    try:

        confidence = float(
            latest["Confidence"]
        )

        if confidence <= 1:

            confidence *= 100

        confidence_display = (
            f"{confidence:.2f}%"
        )

    except Exception:

        confidence_display = (
            "N/A"
        )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🎯 Latest Prediction",
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
                latest["Target"]
            )
        )


    st.markdown(
        "### 📋 Prediction Records"
    )


    st.dataframe(
        predictions_df[
            [
                "ID",
                "Model Type",
                "Target",
                "Prediction",
                "Confidence",
                "Created At"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


else:

    st.info(
        "No predictions found."
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "IntelliData AI • Database Management & Experiment Tracking"
)