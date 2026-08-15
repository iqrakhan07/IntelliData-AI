import streamlit as st
import pandas as pd

from database.database import save_dataset

from utils.data_loader import load_data

st.title("📁 Data Upload")

st.write(
    "Upload a CSV or Excel dataset to begin your analysis."
)

uploaded_file = st.file_uploader(
    "Choose a dataset",
    type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:

    try:

        df = load_data(uploaded_file)

        st.success(
            f"{uploaded_file.name} uploaded successfully!"
        )

        st.session_state["df"] = df
        st.session_state["filename"] = uploaded_file.name

        save_dataset(
            uploaded_file.name,
            df.shape[0],
            df.shape[1]
        )
        
        st.subheader("📋 Dataset Preview")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

        st.subheader("📊 Dataset Information")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Rows",
                df.shape[0]
            )

        with col2:
            st.metric(
                "Columns",
                df.shape[1]
            )

        with col3:
            st.metric(
                "Missing Values",
                int(df.isnull().sum().sum())
            )

        with col4:
            st.metric(
                "Duplicate Rows",
                int(df.duplicated().sum())
            )

        st.subheader("🔎 Column Information")

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values,
            "Unique Values": [
                df[column].nunique()
                for column in df.columns
            ]
        })

        st.dataframe(
            column_info,
            use_container_width=True
        )

    except Exception as e:

        st.error(
            f"Error while loading dataset: {e}"
        )

else:

    st.info(
        "Please upload a CSV or Excel file."
    )