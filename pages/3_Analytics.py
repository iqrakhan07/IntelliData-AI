import streamlit as st
import matplotlib.pyplot as plt

from utils.analytics import (
    get_basic_statistics,
    get_numeric_columns,
    get_categorical_columns,
    get_correlation
)

st.title("📊 Data Analytics")

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset first."
    )

    st.stop()

df = st.session_state["df"]

st.subheader("📌 Dataset Overview")

numeric_columns = get_numeric_columns(df)
categorical_columns = get_categorical_columns(df)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Rows",
        df.shape[0]
    )

with col2:
    st.metric(
        "Numerical Columns",
        len(numeric_columns)
    )

with col3:
    st.metric(
        "Categorical Columns",
        len(categorical_columns)
    )

st.markdown("---")

st.subheader("📈 Statistical Summary")

statistics = get_basic_statistics(df)

st.dataframe(
    statistics,
    use_container_width=True
)

st.markdown("---")

st.subheader("🔗 Correlation Matrix")

if len(numeric_columns) >= 2:

    correlation = get_correlation(df)

    fig, ax = plt.subplots()

    image = ax.imshow(
        correlation,
        cmap="coolwarm"
    )

    ax.set_xticks(
        range(len(correlation.columns))
    )

    ax.set_yticks(
        range(len(correlation.columns))
    )

    ax.set_xticklabels(
        correlation.columns,
        rotation=45,
        ha="right"
    )

    ax.set_yticklabels(
        correlation.columns
    )

    fig.colorbar(image)

    st.pyplot(fig)

else:

    st.info(
        "At least two numerical columns are required."
    )

st.markdown("---")

st.subheader("📊 Column Visualization")

if numeric_columns:

    selected_column = st.selectbox(
        "Select numerical column",
        numeric_columns
    )

    fig, ax = plt.subplots()

    ax.hist(
        df[selected_column].dropna(),
        bins=20
    )

    ax.set_title(
        f"Distribution of {selected_column}"
    )

    ax.set_xlabel(
        selected_column
    )

    ax.set_ylabel(
        "Frequency"
    )

    st.pyplot(fig)

else:

    st.info(
        "No numerical columns available."
    )