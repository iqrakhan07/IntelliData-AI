import streamlit as st
import pandas as pd
import os
import tempfile

from database.database import get_experiments

from utils.ai_insights import (
    generate_dataset_insights
)

from utils.report_generator import (
    generate_pdf_report
)


# ==================================================
# PAGE TITLE
# ==================================================

st.title("📄 Report Generator")

st.caption(
    "Generate a professional PDF report from your IntelliData AI analysis."
)


# ==================================================
# CHECK DATASET
# ==================================================

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset first."
    )

    st.stop()


df = st.session_state["df"]


# ==================================================
# GENERATE AI INSIGHTS
# ==================================================

st.subheader(
    "🧠 Generate Insights"
)


if st.button(
    "Generate Dataset Insights"
):

    with st.spinner(
        "Analyzing dataset..."
    ):

        try:

            insights = generate_dataset_insights(
                df
            )

            st.session_state[
                "report_insights"
            ] = insights

            st.success(
                "Insights generated successfully!"
            )

        except Exception as e:

            st.error(
                f"Insight generation error: {e}"
            )


# ==================================================
# DISPLAY INSIGHTS
# ==================================================

insights = st.session_state.get(
    "report_insights",
    []
)


if insights:

    st.subheader(
        "💡 Report Insights"
    )

    for insight in insights:

        st.info(
            insight
        )


# ==================================================
# LOAD EXPERIMENTS
# ==================================================

try:

    experiments = get_experiments()

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

except Exception as e:

    st.warning(
        f"Could not load experiments: {e}"
    )

    experiments_df = pd.DataFrame()


# ==================================================
# CURRENT MODEL INFORMATION
# ==================================================

problem_type = st.session_state.get(
    "best_model_type",
    "Classification"
)


target_column = st.session_state.get(
    "best_target"
)


prediction = st.session_state.get(
    "last_prediction"
)


confidence = st.session_state.get(
    "last_confidence"
)


# ==================================================
# CURRENT ANALYSIS SUMMARY
# ==================================================

st.markdown("---")

st.subheader(
    "📊 Current Analysis"
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Dataset Rows",
        f"{len(df):,}"
    )


with col2:

    st.metric(
        "Dataset Columns",
        f"{len(df.columns):,}"
    )


with col3:

    if prediction is not None:

        if str(prediction) == "1":

            display_prediction = "Survived"

        elif str(prediction) == "0":

            display_prediction = "Not Survived"

        else:

            display_prediction = str(
                prediction
            )

    else:

        display_prediction = "Not Available"


    st.metric(
        "Latest Prediction",
        display_prediction
    )


st.write(
    f"**Problem Type:** {problem_type}"
)

st.write(
    f"**Target Column:** "
    f"{target_column if target_column else 'Not Available'}"
)


if confidence is not None:

    st.write(
        f"**Prediction Confidence:** "
        f"{float(confidence):.2f}%"
    )


# ==================================================
# EXPERIMENT HISTORY
# ==================================================

st.markdown("---")

st.subheader(
    "🤖 Machine Learning Experiments"
)


if (
    experiments_df is not None
    and not experiments_df.empty
):

    display_columns = [
        "Algorithm",
        "Problem Type",
        "Target",
        "Score",
        "Created At"
    ]

    available_columns = [
        column
        for column in display_columns
        if column in experiments_df.columns
    ]

    st.dataframe(
        experiments_df[
            available_columns
        ],
        use_container_width=True
    )

else:

    st.info(
        "No machine learning experiments available."
    )


# ==================================================
# GENERATE PDF
# ==================================================

st.markdown("---")

st.subheader(
    "📄 Generate PDF Report"
)


st.write(
    "Generate a complete IntelliData AI report "
    "containing dataset information, machine learning "
    "experiments, AI insights and prediction results."
)


if st.button(
    "📥 Generate IntelliData AI Report",
    type="primary"
):

    try:

        # ------------------------------------------
        # CREATE TEMPORARY PDF FILE
        # ------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            pdf_path = temp_file.name


        # ------------------------------------------
        # GENERATE REPORT
        # ------------------------------------------

        with st.spinner(
            "Generating professional PDF report..."
        ):

            generate_pdf_report(
                filename=pdf_path,
                df=df,
                experiments_df=experiments_df,
                insights=insights,
                prediction=prediction,
                confidence=confidence,
                problem_type=problem_type,
                target_column=target_column
            )


        # ------------------------------------------
        # READ PDF
        # ------------------------------------------

        with open(
            pdf_path,
            "rb"
        ) as pdf_file:

            pdf_data = pdf_file.read()


        # ------------------------------------------
        # SUCCESS MESSAGE
        # ------------------------------------------

        st.success(
            "✅ PDF report generated successfully!"
        )


        # ------------------------------------------
        # DOWNLOAD BUTTON
        # ------------------------------------------

        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_data,
            file_name="IntelliData_AI_Report.pdf",
            mime="application/pdf"
        )


        # ------------------------------------------
        # REMOVE TEMPORARY FILE
        # ------------------------------------------

        try:

            os.remove(
                pdf_path
            )

        except Exception:

            pass


    except Exception as e:

        st.error(
            f"Report generation error: {e}"
        )