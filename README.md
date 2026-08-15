# 🤖 IntelliData AI

### Smart Data Analytics & Machine Learning Platform

IntelliData AI is an integrated Python and Streamlit platform for data analysis, machine learning, prediction, AI-powered insights, database management, REST API integration, and automated PDF reporting.

## ✨ Features

- 📁 Data Upload — Upload and manage CSV/Excel datasets
- 🧹 Data Cleaning — Handle missing values and duplicate data
- 📊 Data Analytics — Analyze datasets using statistical methods
- 📈 Data Visualization — Generate interactive visualizations
- 🤖 Machine Learning Studio — Train and compare multiple ML algorithms
- 🔮 Prediction — Generate predictions using the selected best model
- 🧠 AI Insights — Generate automated dataset and ML insights
- 🗄️ Database Management — Store datasets, experiments, and predictions
- 📊 Dashboard — View KPIs, model performance, experiments, and prediction history
- 📄 PDF Reports — Generate professional reports containing dataset analysis, ML experiments, AI insights, and latest predictions
- 🔌 REST API — Flask API for health checks, model information, features, and predictions

## Machine Learning Algorithms

Classification
Logistic Regression
Decision Tree
Random Forest
Naive Bayes
Regression
Linear Regression
Random Forest
Clustering
K-Means Clustering

### Classification

- Logistic Regression
- Decision Tree
- Random Forest
- Naive Bayes

### Regression

- Linear Regression
- Random Forest

### Clustering

- K-Means Clustering

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Web application |
| Pandas | Data processing |
| NumPy | Numerical computation |
| Scikit-learn | Machine Learning |
| Matplotlib | Data visualization |
| Plotly | Interactive visualization |
| Joblib | Model saving/loading |
| Flask | REST API |
| Flask-CORS | API integration |
| SQLite | Database |
| ReportLab | PDF report generation |
| OpenPyXL | Excel file processing |

---

## 📂 Project Structure

```
IntelliData-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── api/
│   ├── __init__.py
│   └── app.py
│
├── database/
│   └── database.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── pages/
│   ├── 1_Data_Upload.py
│   ├── 2_Data_Cleaning.py
│   ├── 3_Analytics.py
│   ├── 4_ML_Studio.py
│   ├── 5_Prediction.py
│   ├── 6_Database.py
│   ├── 7_Dashboard.py
│   ├── 8_AI_Insights.py
│   └── 9_Reports.py
│
└── utils/
    ├── ai_insights.py
    ├── analytics.py
    ├── classification.py
    ├── clustering.py
    ├── data_cleaning.py
    ├── data_loader.py
    ├── model_comparison.py
    ├── model_evaluation.py
    ├── model_manager.py
    ├── preprocessing.py
    ├── regression.py
    └── report_generator.py

```

---

## ⚙️ Installation

### Clone the repository:

git clone https://github.com/YOUR_USERNAME/IntelliData-AI.git

Move into the project directory:

cd IntelliData-AI

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt
🚀 Run IntelliData AI

Start the Streamlit application:

streamlit run app.py

The application will open at:

http://localhost:8501
🔌 Run the Flask REST API

Open another terminal and activate the virtual environment.

Then run:

python api/app.py

The API runs at:

http://127.0.0.1:5000

### API Endpoints

| Endpoint         | Method | Purpose                    |
| ---------------- | ------ | -------------------------- |
| `/`              | GET    | API status                 |
| `/health`        | GET    | Health check               |
| `/model`         | GET    | Model information          |
| `/features`      | GET    | Model features             |
| `/model-details` | GET    | Detailed model information |
| `/predict`       | POST   | Generate prediction        |

### Example:

GET http://127.0.0.1:5000/

Response:

{
  "application": "IntelliData AI",
  "message": "IntelliData AI REST API",
  "status": "running"
}

## 🔄 Application Workflow

```

📁 Upload Dataset
        ↓
🧹 Clean Data
        ↓
📊 Analyze & Visualize
        ↓
🤖 Train & Compare ML Models
        ↓
🏆 Select Best Model
        ↓
🔮 Generate Prediction
        ↓
🧠 Generate AI Insights
        ↓
📄 Generate PDF Report
        ↓
📊 View Results on Dashboard

```

---

## 📄 Reports

The Reports module generates a professional PDF containing:

Dataset summary
Dataset columns and data types
Missing-value information
Duplicate-row information
Machine learning experiments
AI-generated insights
Latest prediction
Prediction confidence

---

## 🗄️ Database

IntelliData AI maintains records for:

Uploaded datasets
Machine learning experiments
Predictions
Prediction confidence
Timestamps

This information is displayed through the Database and Dashboard modules.

---

## 🔐 Security

Sensitive files and local development resources should not be committed to GitHub.

The project .gitignore excludes items such as:

.venv/
.env
*.db
*.sqlite
*.pkl
*.pdf
__pycache__/

Do not commit API keys, credentials, tokens, or other sensitive information.

---

## 🎯 Project Objective

The objective of IntelliData AI is to provide a single platform for the complete data science workflow, from dataset upload and preprocessing to machine learning, prediction, insights, visualization, database tracking, REST API access, and automated reporting.

---

## Author

**Iqra Khan**

Computer Engineering Student
Python & Machine Learning Project

📌 **Project Status**

Status: Completed / Functional Prototype

Project: IntelliData AI

Primary Technologies: Python, Streamlit, Scikit-learn, Flask, SQLite

---

⭐ If you find this project useful, feel free to explore the repository and give it a star!
