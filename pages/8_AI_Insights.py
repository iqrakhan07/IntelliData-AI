import streamlit as st
import pandas as pd

from utils.ai_insights import (
    generate_dataset_insights,
    generate_ml_insights
)

from database.database import (
    get_experiments
)


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Insights - IntelliData AI",
    page_icon="🧠",
    layout="wide"
)


# ==================================================
# TITLE
# ==================================================

st.title("🧠 AI Insights")

st.caption(
    "Automatically generated insights from your dataset "
    "and machine learning experiments."
)


# ==================================================
# DATASET INSIGHTS
# ==================================================

st.markdown("---")

st.header("📊 Dataset Intelligence")


if "df" not in st.session_state:

    st.warning(
        "📂 Please upload a dataset first."
    )

else:

    df = st.session_state["df"].copy()

    # ----------------------------------------------
    # DATASET SUMMARY
    # ----------------------------------------------

    rows, columns = df.shape

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    numeric_columns = len(
        df.select_dtypes(
            include="number"
        ).columns
    )

    categorical_columns = len(
        df.select_dtypes(
            exclude="number"
        ).columns
    )


    col1, col2, col3, col4, col5 = st.columns(5)


    with col1:

        st.metric(
            "Rows",
            f"{rows:,}"
        )


    with col2:

        st.metric(
            "Columns",
            columns
        )


    with col3:

        st.metric(
            "Missing Values",
            f"{missing_values:,}"
        )


    with col4:

        st.metric(
            "Duplicates",
            f"{duplicate_rows:,}"
        )


    with col5:

        st.metric(
            "Numeric Columns",
            numeric_columns
        )


    st.markdown("### 📋 Dataset Structure")

    structure_df = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [
            str(dtype)
            for dtype in df.dtypes
        ],
        "Missing Values": [
            int(df[column].isnull().sum())
            for column in df.columns
        ],
        "Unique Values": [
            int(df[column].nunique())
            for column in df.columns
        ]
    })


    st.dataframe(
        structure_df,
        use_container_width=True,
        hide_index=True
    )


    # ----------------------------------------------
    # GENERATE DATASET INSIGHTS
    # ----------------------------------------------

    if st.button(
        "🧠 Analyze Dataset",
        type="primary"
    ):

        with st.spinner(
            "Analyzing dataset..."
        ):

            try:

                insights = (
                    generate_dataset_insights(
                        df
                    )
                )

                st.session_state[
                    "dataset_insights"
                ] = insights

                st.success(
                    "✅ Dataset analysis completed!"
                )

            except Exception as e:

                st.error(
                    f"Dataset analysis error: {e}"
                )


    # ----------------------------------------------
    # DISPLAY DATASET INSIGHTS
    # ----------------------------------------------

    dataset_insights = (
        st.session_state.get(
            "dataset_insights",
            []
        )
    )


    if dataset_insights:

        st.markdown(
            "### 💡 Generated Dataset Insights"
        )

        for index, insight in enumerate(
            dataset_insights,
            start=1
        ):

            st.info(
                f"💡 **Insight {index}:** {insight}"
            )


# ==================================================
# MACHINE LEARNING INSIGHTS
# ==================================================

st.markdown("---")

st.header(
    "🤖 Machine Learning Intelligence"
)


experiments = get_experiments()


if not experiments:

    st.info(
        "🧪 Train at least one model to generate "
        "machine learning insights."
    )

else:

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


    # ----------------------------------------------
    # EXPERIMENT SUMMARY
    # ----------------------------------------------

    total_experiments = len(
        experiments_df
    )

    best_index = (
        experiments_df["Score"].idxmax()
    )

    best_experiment = (
        experiments_df.loc[
            best_index
        ]
    )


    best_algorithm = (
        best_experiment["Algorithm"]
    )

    best_problem_type = (
        best_experiment["Problem Type"]
    )

    best_target = (
        best_experiment["Target"]
    )

    best_score = float(
        best_experiment["Score"]
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🧪 Experiments",
            total_experiments
        )


    with col2:

        st.metric(
            "🏆 Best Algorithm",
            best_algorithm
        )


    with col3:

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


    with col4:

        st.metric(
            "🎯 Target",
            best_target
        )


    # ----------------------------------------------
    # BEST MODEL
    # ----------------------------------------------

    st.markdown("### 🏆 Best ML Experiment")


    best_model_df = pd.DataFrame({
        "Algorithm": [
            best_algorithm
        ],
        "Problem Type": [
            best_problem_type
        ],
        "Target": [
            best_target
        ],
        "Score": [
            best_score
        ]
    })


    st.dataframe(
        best_model_df,
        use_container_width=True,
        hide_index=True
    )


    # ----------------------------------------------
    # MODEL PERFORMANCE
    # ----------------------------------------------

    st.markdown(
        "### 📊 Algorithm Performance"
    )


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
    # GENERATE ML INSIGHTS
    # ----------------------------------------------

    if st.button(
        "🤖 Generate ML Insights",
        type="primary"
    ):

        with st.spinner(
            "Analyzing machine learning experiments..."
        ):

            try:

                ml_insights = (
                    generate_ml_insights(
                        best_algorithm,
                        best_problem_type,
                        best_score,
                        best_target
                    )
                )

                st.session_state[
                    "ml_insights"
                ] = ml_insights

                st.success(
                    "✅ ML analysis completed!"
                )

            except Exception as e:

                st.error(
                    f"ML analysis error: {e}"
                )


    # ----------------------------------------------
    # DISPLAY ML INSIGHTS
    # ----------------------------------------------

    ml_insights = (
        st.session_state.get(
            "ml_insights",
            []
        )
    )


    if ml_insights:

        st.markdown(
            "### 💡 Generated ML Insights"
        )

        for index, insight in enumerate(
            ml_insights,
            start=1
        ):

            st.success(
                f"🤖 **Insight {index}:** {insight}"
            )


# ==================================================
# OVERALL SUMMARY
# ==================================================

st.markdown("---")

st.header(
    "📋 IntelliData AI Summary"
)


if "df" in st.session_state:

    df = st.session_state["df"]

    rows, columns = df.shape

    missing = int(
        df.isnull().sum().sum()
    )

    duplicates = int(
        df.duplicated().sum()
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "📊 Dataset Rows",
            f"{rows:,}"
        )


    with col2:

        st.metric(
            "📋 Dataset Columns",
            columns
        )


    with col3:

        st.metric(
            "⚠️ Missing Values",
            f"{missing:,}"
        )


    with col4:

        st.metric(
            "♻️ Duplicate Rows",
            f"{duplicates:,}"
        )


else:

    st.info(
        "Upload a dataset to view the IntelliData AI summary."
    )


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "IntelliData AI • AI-powered Data Analytics & Machine Learning"
)