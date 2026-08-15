from flask import (
    Flask,
    jsonify,
    request,
    send_from_directory
)

from flask_cors import CORS

import os
import joblib
import pandas as pd


# ==================================================
# PATHS
# ==================================================

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
# FLASK APP
# ==================================================

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path="/static"
)

CORS(app)


# ==================================================
# HOME / API STATUS
# ==================================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "application": "IntelliData AI",
        "status": "running",
        "message": "IntelliData AI REST API",
        "frontend": "/app",
        "endpoints": {
            "health": "/health",
            "model": "/model",
            "features": "/features",
            "model_details": "/model-details",
            "prediction": "/predict"
        }
    })


# ==================================================
# FLASK FRONTEND
# ==================================================

@app.route("/app", methods=["GET"])
def frontend():

    return send_from_directory(
        FRONTEND_DIR,
        "index.html"
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
            "model_type": type(model).__name__,
            "has_predict_proba": hasattr(
                model,
                "predict_proba"
            )
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

        # ------------------------------------------
        # Pipeline feature names
        # ------------------------------------------

        if hasattr(
            model,
            "feature_names_in_"
        ):

            feature_names = (
                model.feature_names_in_.tolist()
            )

        # ------------------------------------------
        # Pipeline fallback
        # ------------------------------------------

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

@app.route(
    "/model-details",
    methods=["GET"]
)
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

            "model_type":
                type(model).__name__,

            "has_predict_proba":
                hasattr(
                    model,
                    "predict_proba"
                ),

            "features":
                feature_names

        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ==================================================
# PREDICTION
# ==================================================

@app.route(
    "/predict",
    methods=["POST"]
)
def predict():

    # ----------------------------------------------
    # CHECK MODEL
    # ----------------------------------------------

    if not os.path.exists(MODEL_PATH):

        return jsonify({
            "status": "error",
            "message": "Model not found."
        }), 404

    try:

        # ------------------------------------------
        # GET JSON DATA
        # ------------------------------------------

        data = request.get_json(
            silent=True
        )

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

        expected_features = None

        if hasattr(
            model,
            "feature_names_in_"
        ):

            expected_features = (
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

                    expected_features = (
                        step.feature_names_in_.tolist()
                    )

                    break


        # ------------------------------------------
        # VALIDATE FEATURES
        # ------------------------------------------

        if expected_features:

            missing_features = [
                feature
                for feature in expected_features
                if feature not in input_data.columns
            ]

            if missing_features:

                return jsonify({
                    "status": "error",
                    "message": (
                        "Missing required features."
                    ),
                    "missing_features":
                        missing_features,
                    "expected_features":
                        expected_features,
                    "received_features":
                        input_data.columns.tolist()
                }), 400


            # Keep exactly the model's
            # expected column order.

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
        # RESPONSE
        # ------------------------------------------

        response = {

            "status":
                "success",

            "prediction":
                str(result)
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

            confidence = (
                max(probabilities) * 100
            )

            response[
                "confidence"
            ] = round(
                float(confidence),
                2
            )


            # --------------------------------------
            # PROBABILITIES
            # --------------------------------------

            if hasattr(
                model,
                "classes_"
            ):

                classes = (
                    model.classes_
                )

                response[
                    "probabilities"
                ] = {

                    str(cls):
                        round(
                            float(prob) * 100,
                            2
                        )

                    for cls, prob
                    in zip(
                        classes,
                        probabilities
                    )
                }


        return jsonify(
            response
        )


    # ----------------------------------------------
    # ERROR HANDLING
    # ----------------------------------------------

    except Exception as e:

        return jsonify({

            "status":
                "error",

            "message":
                str(e)

        }), 500


# ==================================================
# RUN SERVER
# ==================================================

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("🤖 IntelliData AI Flask API")
    print("=" * 55)
    print(
        f"📁 Model: {MODEL_PATH}"
    )
    print(
        f"🌐 Frontend: http://127.0.0.1:5000/app"
    )
    print(
        f"🔌 API: http://127.0.0.1:5000/"
    )
    print("=" * 55)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )