from flask import Flask, jsonify, request
from flask_cors import CORS

import os
import joblib
import pandas as pd


# ==================================================
# APP CONFIGURATION
# ==================================================

app = Flask(__name__)

CORS(app)


MODEL_PATH = os.path.join(
    "models",
    "best_model.pkl"
)


# ==================================================
# HOME
# ==================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "application": "IntelliData AI",
        "status": "running",
        "message": "IntelliData AI REST API"
    })


# ==================================================
# HEALTH CHECK
# ==================================================

@app.route("/health", methods=["GET"])
def health():

    model_available = os.path.exists(
        MODEL_PATH
    )

    return jsonify({
        "status": "healthy",
        "model_available": model_available
    })


# ==================================================
# MODEL INFORMATION
# ==================================================

@app.route("/model", methods=["GET"])
def model_info():

    if not os.path.exists(MODEL_PATH):

        return jsonify({
            "status": "error",
            "message": "No trained model found."
        }), 404

    return jsonify({
        "status": "success",
        "model": "best_model.pkl"
    })


# ==================================================
# MODEL FEATURES
# ==================================================

@app.route("/features", methods=["GET"])
def features():

    if not os.path.exists(MODEL_PATH):

        return jsonify({
            "status": "error",
            "message": "Model not found."
        }), 404

    try:

        model = joblib.load(
            MODEL_PATH
        )

        feature_names = None

        if hasattr(
            model,
            "feature_names_in_"
        ):

            feature_names = (
                model.feature_names_in_.tolist()
            )

        return jsonify({
            "status": "success",
            "features": feature_names
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==================================================
# MODEL DETAILS
# ==================================================

@app.route("/model-details", methods=["GET"])
def model_details():

    if not os.path.exists(MODEL_PATH):

        return jsonify({
            "status": "error",
            "message": "Model not found."
        }), 404

    try:

        model = joblib.load(
            MODEL_PATH
        )

        features = None

        if hasattr(
            model,
            "feature_names_in_"
        ):

            features = (
                model.feature_names_in_.tolist()
            )

        return jsonify({
            "status": "success",
            "model_type": type(model).__name__,
            "has_predict_proba": hasattr(
                model,
                "predict_proba"
            ),
            "features": features
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==================================================
# PREDICTION
# ==================================================

@app.route("/predict", methods=["POST"])
def predict():

    if not os.path.exists(MODEL_PATH):

        return jsonify({
            "status": "error",
            "message": "Model not found."
        }), 404

    try:

        # ------------------------------------------
        # GET JSON DATA
        # ------------------------------------------

        data = request.get_json()

        if not data:

            return jsonify({
                "status": "error",
                "message": "No input data provided."
            }), 400


        # ------------------------------------------
        # LOAD MODEL
        # ------------------------------------------

        model = joblib.load(
            MODEL_PATH
        )


        # ------------------------------------------
        # CREATE DATAFRAME
        # ------------------------------------------

        input_data = pd.DataFrame(
            [data]
        )


        # ------------------------------------------
        # GET EXPECTED FEATURES
        # ------------------------------------------

        if hasattr(
            model,
            "feature_names_in_"
        ):

            expected_features = (
                model.feature_names_in_.tolist()
            )

            missing_features = [
                feature
                for feature in expected_features
                if feature not in input_data.columns
            ]

            if missing_features:

                return jsonify({
                    "status": "error",
                    "message": "Missing input features.",
                    "missing_features": missing_features
                }), 400

            input_data = input_data[
                expected_features
            ]


        # ------------------------------------------
        # PREDICTION
        # ------------------------------------------

        prediction = model.predict(
            input_data
        )

        result = prediction[0]


        # ------------------------------------------
        # BASE RESPONSE
        # ------------------------------------------

        response = {
            "status": "success",
            "prediction": int(result)
            if str(result).isdigit()
            else str(result)
        }


        # ------------------------------------------
        # PROBABILITY / CONFIDENCE
        # ------------------------------------------

        if hasattr(
            model,
            "predict_proba"
        ):

            probabilities = model.predict_proba(
                input_data
            )[0]


            classes = model.classes_


            predicted_index = list(
                classes
            ).index(result)


            probability = (
                probabilities[
                    predicted_index
                ] * 100
            )


            response[
                "confidence"
            ] = round(
                float(probability),
                2
            )


            # --------------------------------------
            # TITANIC LABEL
            # --------------------------------------

            if result == 1:

                response[
                    "prediction_label"
                ] = "Survived"

            elif result == 0:

                response[
                    "prediction_label"
                ] = "Not Survived"


        # ------------------------------------------
        # RETURN RESPONSE
        # ------------------------------------------

        return jsonify(
            response
        )


    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==================================================
# RUN SERVER
# ==================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )