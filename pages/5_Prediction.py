import streamlit as st
import pandas as pd

from database.database import save_prediction


# ==================================================
# PAGE TITLE
# ==================================================

st.title("🔮 Prediction")

st.caption(
    "Use the selected machine learning model to generate predictions."
)


# ==================================================
# CHECK MODEL
# ==================================================

if "best_model" not in st.session_state:

    st.warning(
        "No trained model is available."
    )

    st.info(
        "Go to Machine Learning Studio, "
        "compare models and select the best model first."
    )

    st.stop()


model = st.session_state["best_model"]


problem_type = st.session_state.get(
    "best_model_type",
    "Classification"
)


target_column = st.session_state.get(
    "best_target"
)


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
# MODEL INFORMATION
# ==================================================

st.subheader(
    "📊 Model Information"
)


col1, col2 = st.columns(2)


with col1:

    st.write(
        f"**Problem Type:** {problem_type}"
    )


with col2:

    st.write(
        f"**Target Column:** {target_column}"
    )


st.markdown("---")


# ==================================================
# INPUT FEATURES
# ==================================================

st.subheader(
    "📝 Enter Input Values"
)


feature_columns = [
    column
    for column in df.columns
    if column != target_column
]


input_data = {}


for column in feature_columns:

    # ----------------------------------------------
    # NUMERIC FEATURE
    # ----------------------------------------------

    if pd.api.types.is_numeric_dtype(
        df[column]
    ):

        median_value = df[column].median()


        if pd.isna(
            median_value
        ):

            median_value = 0


        input_data[column] = st.number_input(
            column,
            value=float(
                median_value
            )
        )


    # ----------------------------------------------
    # CATEGORICAL FEATURE
    # ----------------------------------------------

    else:

        values = (
            df[column]
            .dropna()
            .unique()
            .tolist()
        )


        values = [
            str(value)
            for value in values
        ]


        if values:

            input_data[column] = st.selectbox(
                column,
                values
            )

        else:

            input_data[column] = ""


# ==================================================
# CREATE INPUT DATAFRAME
# ==================================================

input_df = pd.DataFrame(
    [input_data]
)


st.markdown("---")


# ==================================================
# INPUT PREVIEW
# ==================================================

st.subheader(
    "🔍 Input Preview"
)


st.dataframe(
    input_df,
    use_container_width=True
)


# ==================================================
# PREDICTION BUTTON
# ==================================================

if st.button(
    "🔮 Make Prediction",
    type="primary"
):

    try:

        # ==========================================
        # PREDICT
        # ==========================================

        prediction = model.predict(
            input_df
        )


        result = prediction[0]


        confidence = None


        # ==========================================
        # CLASSIFICATION
        # ==========================================

        if problem_type == "Classification":

            # --------------------------------------
            # CREATE PREDICTION LABEL
            # --------------------------------------

            if str(result) == "1":

                prediction_label = (
                    "Survived"
                )

            elif str(result) == "0":

                prediction_label = (
                    "Not Survived"
                )

            else:

                prediction_label = str(
                    result
                )


            # --------------------------------------
            # SUCCESS MESSAGE
            # --------------------------------------

            st.success(
                "🎉 Prediction generated successfully!"
            )


            st.subheader(
                "🎯 Prediction Result"
            )


            # --------------------------------------
            # TITANIC RESULT
            # --------------------------------------

            if prediction_label == "Survived":

                st.success(
                    "✅ Passenger is likely to Survive"
                )

            elif prediction_label == "Not Survived":

                st.error(
                    "❌ Passenger is likely to Not Survive"
                )

            else:

                st.info(
                    f"Prediction: {prediction_label}"
                )


            # --------------------------------------
            # PREDICTION VALUE
            # --------------------------------------

            st.write(
                f"**Prediction:** "
                f"{prediction_label}"
            )


            # ======================================
            # PREDICT PROBABILITY
            # ======================================

            if hasattr(
                model,
                "predict_proba"
            ):

                probabilities = (
                    model.predict_proba(
                        input_df
                    )[0]
                )


                classes = model.classes_


                # ----------------------------------
                # FIND PREDICTED CLASS
                # ----------------------------------

                predicted_index = list(
                    classes
                ).index(
                    result
                )


                confidence = (
                    probabilities[
                        predicted_index
                    ] * 100
                )


                # ----------------------------------
                # SAVE FOR REPORTS
                # ----------------------------------

                st.session_state[
                    "last_prediction"
                ] = result


                st.session_state[
                    "last_confidence"
                ] = confidence


                # ----------------------------------
                # CONFIDENCE
                # ----------------------------------

                st.metric(
                    "Confidence",
                    f"{confidence:.2f}%"
                )


                # ----------------------------------
                # PROBABILITY TABLE
                # ----------------------------------

                probability_df = pd.DataFrame({

                    "Class": classes,

                    "Probability": (
                        probabilities * 100
                    ).round(2)

                })


                st.subheader(
                    "📊 Prediction Probability"
                )


                st.dataframe(
                    probability_df,
                    use_container_width=True
                )


            else:

                # ----------------------------------
                # MODEL WITHOUT PROBABILITY
                # ----------------------------------

                st.session_state[
                    "last_prediction"
                ] = result


                st.session_state[
                    "last_confidence"
                ] = None


                st.info(
                    "This model does not provide "
                    "prediction probabilities."
                )


        # ==========================================
        # REGRESSION
        # ==========================================

        else:

            st.success(
                "🎉 Prediction generated successfully!"
            )


            st.subheader(
                "🎯 Prediction Result"
            )


            st.metric(
                "Predicted Value",
                f"{float(result):.4f}"
            )


            # --------------------------------------
            # SAVE FOR REPORTS
            # --------------------------------------

            st.session_state[
                "last_prediction"
            ] = result


            st.session_state[
                "last_confidence"
            ] = None


        # ==========================================
        # SAVE PREDICTION TO DATABASE
        # ==========================================

        save_prediction(
            problem_type,
            target_column,
            result,
            confidence
        )


        st.success(
            "✅ Prediction saved to database!"
        )


    # ==============================================
    # ERROR HANDLING
    # ==============================================

    except Exception as e:

        st.error(
            f"Prediction error: {e}"
        )