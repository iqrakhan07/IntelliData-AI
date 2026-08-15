const API_BASE = window.location.origin;


/* ==========================================
   API REQUEST
   ========================================== */

async function apiRequest(endpoint, options = {}) {

    const response = await fetch(
        `${API_BASE}${endpoint}`,
        options
    );

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            data.message || "API request failed."
        );
    }

    return data;
}


/* ==========================================
   API STATUS
   ========================================== */

async function checkAPI() {

    try {

        const data = await apiRequest("/health");

        const online =
            data.status === "healthy";

        const dot =
            document.getElementById("apiDot");

        const topDot =
            document.getElementById("topStatusDot");

        const text =
            document.getElementById("apiText");

        const topStatus =
            document.getElementById("topStatus");

        const dashboardApi =
            document.getElementById("dashboardApi");

        const modelApiStatus =
            document.getElementById(
                "modelApiStatus"
            );


        if (online) {

            dot.classList.add(
                "api-online"
            );

            topDot.classList.add(
                "api-online"
            );

            text.textContent =
                "API Connected";

            topStatus.textContent =
                "API Connected";

            dashboardApi.textContent =
                "Connected";

            modelApiStatus.textContent =
                "Connected";

        } else {

            throw new Error(
                "API unavailable"
            );

        }

    } catch (error) {

        document
            .getElementById("apiDot")
            .classList.add(
                "api-offline"
            );

        document
            .getElementById("topStatusDot")
            .classList.add(
                "api-offline"
            );

        document
            .getElementById("apiText")
            .textContent =
            "API Offline";

        document
            .getElementById("topStatus")
            .textContent =
            "API Offline";

        document
            .getElementById("dashboardApi")
            .textContent =
            "Offline";

        document
            .getElementById("modelApiStatus")
            .textContent =
            "Offline";
    }
}


/* ==========================================
   LOAD MODEL DETAILS
   ========================================== */

async function loadModelDetails() {

    try {

        const data =
            await apiRequest(
                "/model-details"
            );


        const modelType =
            data.model_type ||
            "Unknown";


        document.getElementById(
            "dashboardModel"
        ).textContent =
            modelType;


        document.getElementById(
            "modelType"
        ).textContent =
            modelType;


        document.getElementById(
            "modelProbability"
        ).textContent =
            data.has_predict_proba
                ? "Available"
                : "Not Available";


        loadFeatures(
            data.features
        );


    } catch (error) {

        document.getElementById(
            "dashboardModel"
        ).textContent =
            "Unavailable";


        document.getElementById(
            "modelType"
        ).textContent =
            "Unavailable";


        document.getElementById(
            "modelProbability"
        ).textContent =
            "Unavailable";


        document.getElementById(
            "featureList"
        ).innerHTML =
            `<span class="loading">
                Unable to load model information.
            </span>`;
    }
}


/* ==========================================
   LOAD FEATURES
   ========================================== */

async function loadFeatures(
    suppliedFeatures = null
) {

    try {

        let features =
            suppliedFeatures;


        if (!features) {

            const data =
                await apiRequest(
                    "/features"
                );

            features =
                data.features;
        }


        const container =
            document.getElementById(
                "featureList"
            );


        if (
            !features ||
            features.length === 0
        ) {

            container.innerHTML =
                `<span class="loading">
                    No model features available.
                </span>`;

            return;
        }


        container.innerHTML =
            features
                .map(
                    feature =>
                        `<span class="feature">
                            ${escapeHTML(feature)}
                        </span>`
                )
                .join("");

    } catch (error) {

        document.getElementById(
            "featureList"
        ).innerHTML =
            `<span class="loading">
                Unable to load features.
            </span>`;
    }
}


/* ==========================================
   MAKE PREDICTION
   ========================================== */

async function makePrediction() {

    const errorBox =
        document.getElementById(
            "predictionError"
        );

    errorBox.classList.add(
        "hidden"
    );


    const payload = {

        PassengerId:
            Number(
                document.getElementById(
                    "PassengerId"
                ).value
            ),

        Pclass:
            Number(
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

        Age:
            Number(
                document.getElementById(
                    "Age"
                ).value
            ),

        SibSp:
            Number(
                document.getElementById(
                    "SibSp"
                ).value
            ),

        Parch:
            Number(
                document.getElementById(
                    "Parch"
                ).value
            ),

        Ticket:
            document.getElementById(
                "Ticket"
            ).value,

        Fare:
            Number(
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


    const button =
        document.querySelector(
            ".predict-button"
        );


    button.disabled = true;

    button.textContent =
        "⏳ Generating Prediction...";


    try {

        const data =
            await apiRequest(
                "/predict",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            payload
                        )
                }
            );


        displayPrediction(
            data
        );


    } catch (error) {

        errorBox.textContent =
            `Prediction error: ${error.message}`;

        errorBox.classList.remove(
            "hidden"
        );

    } finally {

        button.disabled = false;

        button.textContent =
            "🔮 Make Prediction";
    }
}


/* ==========================================
   DISPLAY PREDICTION
   ========================================== */

function displayPrediction(data) {

    const result =
        String(
            data.prediction
        );


    const resultBox =
        document.getElementById(
            "resultBox"
        );

    const resultTitle =
        document.getElementById(
            "resultTitle"
        );

    const resultIcon =
        document.getElementById(
            "resultIcon"
        );


    let isSurvived =
        result === "1";


    let isNotSurvived =
        result === "0";


    resultBox.classList.remove(
        "waiting",
        "success",
        "danger"
    );


    if (isSurvived) {

        resultBox.classList.add(
            "success"
        );

        resultBox.innerHTML = `
            <div class="result-number">
                Survived
            </div>

            <p>
                🎉 Passenger is likely to survive.
            </p>
        `;

        resultTitle.textContent =
            "Prediction Generated";

        resultIcon.textContent =
            "🎉";

    } else if (isNotSurvived) {

        resultBox.classList.add(
            "danger"
        );

        resultBox.innerHTML = `
            <div class="result-number">
                Not Survived
            </div>

            <p>
                Passenger is likely not to survive.
            </p>
        `;

        resultTitle.textContent =
            "Prediction Generated";

        resultIcon.textContent =
            "⚠️";

    } else {

        resultBox.classList.add(
            "success"
        );

        resultBox.innerHTML = `
            <div class="result-number">
                ${escapeHTML(result)}
            </div>

            <p>
                Prediction generated successfully.
            </p>
        `;

        resultTitle.textContent =
            "Prediction Generated";

        resultIcon.textContent =
            "🎯";
    }


    /* ------------------------------------------
       CONFIDENCE
       ------------------------------------------ */

    const confidenceSection =
        document.getElementById(
            "confidenceSection"
        );


    if (
        data.confidence !== undefined &&
        data.confidence !== null
    ) {

        const confidence =
            Number(
                data.confidence
            );


        document.getElementById(
            "confidence"
        ).textContent =
            `${confidence.toFixed(2)}%`;


        document.getElementById(
            "confidenceBar"
        ).style.width =
            `${Math.min(
                confidence,
                100
            )}%`;


        confidenceSection.classList.remove(
            "hidden"
        );

    } else {

        confidenceSection.classList.add(
            "hidden"
        );
    }


    /* ------------------------------------------
       PROBABILITIES
       ------------------------------------------ */

    displayProbabilities(
        data.probabilities
    );
}


/* ==========================================
   DISPLAY PROBABILITIES
   ========================================== */

function displayProbabilities(
    probabilities
) {

    const section =
        document.getElementById(
            "probabilitySection"
        );

    const list =
        document.getElementById(
            "probabilityList"
        );


    if (
        !probabilities ||
        Object.keys(
            probabilities
        ).length === 0
    ) {

        section.classList.add(
            "hidden"
        );

        return;
    }


    list.innerHTML =
        Object.entries(
            probabilities
        )
        .map(
            ([label, probability]) => {

                let displayLabel =
                    label;

                if (label === "1") {
                    displayLabel =
                        "Survived";
                }

                if (label === "0") {
                    displayLabel =
                        "Not Survived";
                }

                return `
                    <div class="probability-row">
                        <span>
                            ${escapeHTML(
                                displayLabel
                            )}
                        </span>

                        <strong>
                            ${Number(
                                probability
                            ).toFixed(2)}%
                        </strong>
                    </div>
                `;
            }
        )
        .join("");


    section.classList.remove(
        "hidden"
    );
}


/* ==========================================
   HTML ESCAPE
   ========================================== */

function escapeHTML(value) {

    return String(value)
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );
}


/* ==========================================
   NAVIGATION
   ========================================== */

document
    .querySelectorAll(".nav-link")
    .forEach(link => {

        link.addEventListener(
            "click",
            () => {

                document
                    .querySelectorAll(
                        ".nav-link"
                    )
                    .forEach(
                        item =>
                            item.classList.remove(
                                "active"
                            )
                    );

                link.classList.add(
                    "active"
                );
            }
        );

    });


/* ==========================================
   INITIALIZE
   ========================================== */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        checkAPI();

        loadModelDetails();

    }
);