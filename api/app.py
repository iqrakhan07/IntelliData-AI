from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import joblib
import pandas as pd


# ==================================================
# APPLICATION CONFIGURATION
# ==================================================

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "best_model.pkl"
)

FRONTEND_DIR = os.path.join(
    BASE_DIR,
    "frontend"
)


# ==================================================
# HOME / WHITE FRONTEND DASHBOARD
# ==================================================

@app.route("/", methods=["GET"])
def home():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
    )


# ==================================================
# FRONTEND STATIC FILES
# ==================================================

@app.route("/<path:filename>", methods=["GET"])
def frontend_files(filename):

    return send_from_directory(
        FRONTEND_DIR,
        filename
    )


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

    try:

        model = joblib.load(
            MODEL_PATH
        )

        return jsonify({
            "status": "success",
            "model": "best_model.pkl",
            "model_type": type(model).__name__
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


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

        # Pipeline may contain the actual estimator
        if hasattr(
            model,
            "feature_names_in_"
        ):

            feature_names = (
                model.feature_names_in_.tolist()
            )

        elif hasattr(
            model,
            "named_steps"
        ):

            for step in model.named_steps.values():

                if hasattr(
                    step,
                    "feature_names_in_"
                ):

                    feature_names = (
                        step.feature_names_in_.tolist()
                    )

                    break

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

        feature_names = None

        if hasattr(
            model,
            "feature_names_in_"
        ):

            feature_names = (
                model.feature_names_in_.tolist()
            )

        elif hasattr(
            model,
            "named_steps"
        ):

            for step in model.named_steps.values():

                if hasattr(
                    step,
                    "feature_names_in_"
                ):

                    feature_names = (
                        step.feature_names_in_.tolist()
                    )

                    break

        return jsonify({
            "status": "success",
            "model_type": type(model).__name__,
            "has_predict_proba": hasattr(
                model,
                "predict_proba"
            ),
            "features": feature_names
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
        # GET MODEL FEATURES
        # ------------------------------------------

        feature_names = None

        if hasattr(
            model,
            "feature_names_in_"
        ):

            feature_names = (
                model.feature_names_in_.tolist()
            )

        elif hasattr(
            model,
            "named_steps"
        ):

            for step in model.named_steps.values():

                if hasattr(
                    step,
                    "feature_names_in_"
                ):

                    feature_names = (
                        step.feature_names_in_.tolist()
                    )

                    break


        # ------------------------------------------
        # CREATE INPUT DATAFRAME
        # ------------------------------------------

        input_data = pd.DataFrame(
            [data]
        )


        # ------------------------------------------
        # VALIDATE FEATURES
        # ------------------------------------------

        if feature_names:

            missing_features = [
                feature
                for feature in feature_names
                if feature not in input_data.columns
            ]

            if missing_features:

                return jsonify({
                    "status": "error",
                    "message": "Missing required features.",
                    "missing_features": missing_features
                }), 400

            # Keep exactly the same order
            # as the model expects.
            input_data = input_data[
                feature_names
            ]


        # ------------------------------------------
        # PREDICTION
        # ------------------------------------------

        prediction = model.predict(
            input_data
        )

        result = prediction[0]


        response = {
            "status": "success",
            "prediction": str(result)
        }


        # ------------------------------------------
        # CONFIDENCE
        # ------------------------------------------

        if hasattr(
            model,
            "predict_proba"
        ):

            probabilities = (
                model.predict_proba(
                    input_data
                )[0]
            )

            predicted_index = (
                list(model.classes_).index(
                    result
                )
            )

            confidence = (
                probabilities[
                    predicted_index
                ] * 100
            )

            response["confidence"] = round(
                float(confidence),
                2
            )

            response["probabilities"] = {
                str(cls): round(
                    float(probability * 100),
                    2
                )
                for cls, probability
                in zip(
                    model.classes_,
                    probabilities
                )
            }


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