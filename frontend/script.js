const predictionForm =
    document.getElementById(
        "predictionForm"
    );


const resultCard =
    document.getElementById(
        "resultCard"
    );


const resultMessage =
    document.getElementById(
        "resultMessage"
    );


const predictionValue =
    document.getElementById(
        "predictionValue"
    );


const confidenceValue =
    document.getElementById(
        "confidenceValue"
    );


const loading =
    document.getElementById(
        "loading"
    );



predictionForm.addEventListener(
    "submit",
    async function (event) {

        event.preventDefault();


        // ==============================
        // GET FORM VALUES
        // ==============================

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


        // ==============================
        // SHOW LOADING
        // ==============================

        loading.style.display =
            "block";

        predictionValue.textContent =
            "--";

        confidenceValue.textContent =
            "Confidence: --";

        resultMessage.textContent =
            "Sending data to ML model...";


        try {

            // ==============================
            // SEND REQUEST TO FLASK
            // ==============================

            const response =
                await fetch(
                    "http://127.0.0.1:5000/predict",
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


            // ==============================
            // HANDLE ERROR
            // ==============================

            if (!response.ok) {

                throw new Error(
                    result.message ||
                    "Prediction failed."
                );

            }


            // ==============================
            // DISPLAY RESULT
            // ==============================

            predictionValue.textContent =
                result.prediction;


            resultMessage.textContent =
                "Prediction generated successfully.";


            if (
                result.confidence !==
                undefined
            ) {

                confidenceValue.textContent =
                    `Confidence: ${
                        result.confidence
                    }%`;

            }


        }

        catch (error) {

            console.error(
                error
            );


            resultMessage.textContent =
                "Unable to connect to the Flask API.";


            predictionValue.textContent =
                "Error";


            confidenceValue.textContent =
                error.message;

        }


        finally {

            loading.style.display =
                "none";

        }

    }
);