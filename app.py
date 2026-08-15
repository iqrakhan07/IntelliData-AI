import streamlit as st

from database.database import initialize_database


# ==================================================
# DATABASE INITIALIZATION
# ==================================================

initialize_database()


# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="IntelliData AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# HEADER
# ==================================================

st.title("🤖 IntelliData AI")

st.subheader(
    "Smart Data Analytics & Machine Learning Platform"
)

st.write(
    "An integrated platform for data analysis, "
    "machine learning, prediction, AI insights "
    "and automated reporting."
)


# ==================================================
# QUICK STATS
# ==================================================

st.markdown("---")

st.subheader("🚀 Platform Modules")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.info(
        "📁\n\n"
        "**Data Management**\n\n"
        "Upload and manage datasets."
    )


with col2:

    st.info(
        "📊\n\n"
        "**Data Analytics**\n\n"
        "Explore and visualize your data."
    )


with col3:

    st.info(
        "🤖\n\n"
        "**Machine Learning**\n\n"
        "Train and compare ML models."
    )


with col4:

    st.info(
        "🔮\n\n"
        "**Prediction**\n\n"
        "Generate predictions using trained models."
    )


# ==================================================
# WORKFLOW
# ==================================================

st.markdown("---")

st.subheader("🔄 IntelliData AI Workflow")


workflow = [
    ("1️⃣", "Upload", "Upload your dataset"),
    ("2️⃣", "Clean", "Prepare and clean the data"),
    ("3️⃣", "Analyze", "Explore patterns and statistics"),
    ("4️⃣", "Train", "Train machine learning models"),
    ("5️⃣", "Predict", "Generate predictions"),
    ("6️⃣", "Insights", "Generate AI-powered insights"),
    ("7️⃣", "Report", "Create a professional PDF report")
]


cols = st.columns(len(workflow))


for col, item in zip(cols, workflow):

    icon, title, description = item

    with col:

        st.markdown(
            f"### {icon}"
        )

        st.markdown(
            f"**{title}**"
        )

        st.caption(
            description
        )


# ==================================================
# FEATURES
# ==================================================

st.markdown("---")

st.subheader("✨ Key Features")


col1, col2 = st.columns(2)


with col1:

    st.markdown(
        """
        **📂 Data Management**
        
        • Dataset upload  
        • Dataset history  
        • Data cleaning  
        • Missing-value handling  
        • Duplicate detection
        """
    )

    st.markdown(
        """
        **🤖 Machine Learning**
        
        • Classification  
        • Regression  
        • Model comparison  
        • Performance evaluation  
        • Best-model selection
        """
    )


with col2:

    st.markdown(
        """
        **🧠 AI Intelligence**
        
        • Dataset insights  
        • ML insights  
        • Automated analysis  
        • Experiment tracking
        """
    )

    st.markdown(
        """
        **📄 Reporting**
        
        • Automated PDF reports  
        • Dataset summary  
        • ML experiment results  
        • AI-generated insights  
        • Latest prediction
        """
    )


# ==================================================
# GET STARTED
# ==================================================

st.markdown("---")

st.subheader("🚀 Get Started")


st.info(
    "Use the sidebar to navigate through the IntelliData AI modules."
)


st.markdown(
    """
    **Recommended workflow:**

    `📁 Data Upload`
    → `🧹 Data Cleaning`
    → `📊 Analytics`
    → `🤖 ML Studio`
    → `🔮 Prediction`
    → `🧠 AI Insights`
    → `📄 Reports`
    """
)


# ==================================================
# FOOTER
# ==================================================

st.markdown("---")

st.caption(
    "IntelliData AI • Smart Data Analytics & Machine Learning Platform"
)