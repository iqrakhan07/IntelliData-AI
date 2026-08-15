import streamlit as st

from utils.data_cleaning import (
    get_missing_values,
    get_duplicate_count,
    remove_duplicates,
    fill_missing_numeric,
    fill_missing_categorical
)

st.title("🧹 Data Cleaning")

if "df" not in st.session_state:

    st.warning(
        "Please upload a dataset first."
    )

    st.stop()

df = st.session_state["df"].copy()

st.subheader("Dataset Before Cleaning")

st.dataframe(
    df.head(10),
    use_container_width=True
)

st.markdown("---")

st.subheader("🔍 Missing Values")

missing = get_missing_values(df)

missing_df = missing[
    missing > 0
].reset_index()

missing_df.columns = [
    "Column",
    "Missing Values"
]

if missing_df.empty:

    st.success(
        "No missing values found!"
    )

else:

    st.dataframe(
        missing_df,
        use_container_width=True
    )

st.markdown("---")

st.subheader("🔁 Duplicate Rows")

duplicate_count = get_duplicate_count(df)

st.metric(
    "Duplicate Rows",
    duplicate_count
)

if duplicate_count > 0:

    if st.button("Remove Duplicates"):

        df = remove_duplicates(df)

        st.session_state["df"] = df

        st.success(
            "Duplicate rows removed successfully!"
        )

st.markdown("---")

st.subheader("🩹 Handle Missing Values")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "Fill Numerical Missing Values"
    ):

        df = fill_missing_numeric(df)

        st.session_state["df"] = df

        st.success(
            "Numerical missing values filled using median."
        )

with col2:

    if st.button(
        "Fill Categorical Missing Values"
    ):

        df = fill_missing_categorical(df)

        st.session_state["df"] = df

        st.success(
            "Categorical missing values filled using mode."
        )

st.markdown("---")

st.subheader("✅ Cleaned Dataset")

st.dataframe(
    st.session_state["df"].head(10),
    use_container_width=True
)