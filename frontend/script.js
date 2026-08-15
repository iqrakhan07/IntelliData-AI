const form =
    document.getElementById("prediction-form");

const resultBox =
    document.getElementById("result");


// ==========================================
// LOAD MODEL INFORMATION
// ==========================================

async function loadModelInformation() {

    try {

        const response =
            await fetch("/model-details");

        const data =
            await response.json();


        if (
            response.ok &&
            data.status === "success"
        ) {

            document.getElementById(
                "model-type"
            ).textContent =
                data.model_type || "Unknown";


            document.getElementById(
                "model-name"
            ).textContent =
                "best_model.pkl";


            document.getElementById(
                "probability-status"
            ).textContent =
                data.has_predict_proba
                    ? "Available"
                    : "Not Available";


            document.getElementById(
                "feature-count"
            ).textContent =
                data.features
                    ? `${data.features.length} Features`
                    : "Unknown";

        }

    } catch (error) {

        console.error(
            "Model information error:",
            error
        );

        document.getElementById(
            "model-type"
        ).textContent =
            "Unavailable";

        document.getElementById(
            "model-name"
        ).textContent =
            "Unavailable";
    }
}


// ==========================================
// CHECK API STATUS
// ==========================================

async function checkAPIStatus() {

    try {

        const response =
            await fetch("/health");

        const data =
            await response.json();


        const status =
            document.getElementById(
                "api-status"
            );


        if (
            response.ok &&
            data.status === "healthy"
        ) {

            status.textContent =
                data.model_available
                    ? "Online"
                    : "No Model";

        } else {

            status.textContent =
                "Offline";
        }

    } catch (error) {

        document.getElementById(
            "api-status"
        ).textContent =
            "Offline";
    }
}


// ==========================================
// PREDICTION
// ==========================================

form.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        const button =
            form.querySelector(
                ".predict-btn"
            );


        button.disabled = true;

        button.textContent =
            "⏳ Making Prediction...";


        resultBox.className =
            "result loading";


        resultBox.innerHTML = `
            <h3>⏳ Processing Prediction</h3>
            <p>
                Please wait while IntelliData AI
                processes the passenger information.
            </p>
        `;


        // --------------------------------------
        // INPUT DATA
        // --------------------------------------

        const data = {

            PassengerId: Number(
                document.getElementById(
                    "PassengerId"
                ).value
            ),

            Pclass: Number(
                document.getElementById(
                    "Pclass"
                ).value
            ),

            Name:
                document.getElementById(
                    "Name"
                ).value,

            // IMPORTANT:
            // Your dataset uses Gender
            Gender:
                document.getElementById(
                    "Gender"
                ).value,

            Age: Number(
                document.getElementById(
                    "Age"
                ).value
            ),

            SibSp: Number(
                document.getElementById(
                    "SibSp"
                ).value
            ),

            Parch: Number(
                document.getElementById(
                    "Parch"
                ).value
            ),

            Ticket:
                document.getElementById(
                    "Ticket"
                ).value,

            Fare: Number(
                document.getElementById(
                    "Fare"
                ).value
            ),

            Cabin:
                document.getElementById(
                    "Cabin"
                ).value,

            Embarked:
                document.getElementById(
                    "Embarked"
                ).value
        };


        console.log(
            "Prediction input:",
            data
        );


        // --------------------------------------
        // CALL FLASK API
        // --------------------------------------

        try {

            const response =
                await fetch(
                    "/predict",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(data)
                    }
                );


            const result =
                await response.json();


            console.log(
                "Prediction response:",
                result
            );


            if (
                !response.ok ||
                result.status === "error"
            ) {

                throw new Error(
                    result.message ||
                    "Prediction failed."
                );
            }


            // ----------------------------------
            // PREDICTION
            // ----------------------------------

            const prediction =
                String(
                    result.prediction
                );


            let predictionText;

            let resultClass;


            if (prediction === "1") {

                predictionText =
                    "🎉 Passenger is likely to Survive";

                resultClass =
                    "success";

            }

            else if (prediction === "0") {

                predictionText =
                    "⚠️ Passenger is likely to Not Survive";

                resultClass =
                    "warning";

            }

            else {

                predictionText =
                    `Prediction: ${prediction}`;

                resultClass =
                    "success";
            }


            // ----------------------------------
            // CONFIDENCE
            // ----------------------------------

            let confidenceHTML = "";


            if (
                result.confidence !==
                    undefined &&
                result.confidence !== null
            ) {

                const confidence =
                    Number(
                        result.confidence
                    );


                confidenceHTML = `

                    <div class="confidence">

                        <span>
                            Confidence
                        </span>

                        <strong>
                            ${confidence.toFixed(2)}%
                        </strong>

                    </div>

                `;
            }


            // ----------------------------------
            // DISPLAY RESULT
            // ----------------------------------

            resultBox.className =
                `result ${resultClass}`;


            resultBox.innerHTML = `

                <h3>
                    🎯 Prediction Result
                </h3>


                <div class="prediction-main">

                    <span>
                        Predicted Value
                    </span>

                    <strong>
                        ${prediction}
                    </strong>

                </div>


                <p class="prediction-text">
                    ${predictionText}
                </p>


                ${confidenceHTML}


                <p class="success-note">
                    Prediction generated successfully.
                </p>

            `;

        }


        catch (error) {

            console.error(
                "Prediction error:",
                error
            );


            resultBox.className =
                "result error";


            resultBox.innerHTML = `

                <h3>
                    ❌ Prediction Error
                </h3>

                <p>
                    ${error.message}
                </p>

                <p class="success-note">
                    Check that Flask is running and
                    the model features match the
                    submitted input.
                </p>

            `;

        }


        finally {

            button.disabled = false;

            button.textContent =
                "🔮 Make Prediction";
        }

    }
);


// ==========================================
// INITIALIZE
// ==========================================

loadModelInformation();

checkAPIStatus();