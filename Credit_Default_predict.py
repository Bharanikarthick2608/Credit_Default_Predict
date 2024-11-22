import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestClassifier

# Load the RandomForest model
filename = 'random_forest_model.pkl'
loaded_model = joblib.load(open(filename, 'rb'))

def predict_default(features):
    # Predict the default status using the model
    prediction = loaded_model.predict([features])
    return prediction

def main():
    # Customizing the Streamlit app with some CSS and markdown
    st.set_page_config(page_title="Credit Default Prediction", page_icon="💳", layout="wide")

    # Custom Header with a background image and title
    st.markdown("""
        <style>
            .title {
                text-align: center;
                color: #4CAF50;
                font-size: 40px;
                font-weight: bold;
            }
            .info {
                font-size: 16px;
                color: #555555;
                text-align: center;
                margin-bottom: 30px;
            }
            .sidebar .sidebar-content {
                background-color: #F0F2F6;
            }
            .model-info {
                font-size: 14px;
                color: #333333;
                margin-top: 10px;
            }
            .prediction-info {
                font-size: 16px;
                color: rgba(255, 255, 255, 0.7); /* Half white (light gray) for visibility */
                margin-top: 20px;
            }
            .prediction-message {
                font-size: 18px;
                color: rgba(255, 255, 255, 0.7); /* Half white (light gray) for visibility */
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="title">Credit Default Prediction App 💳</p>', unsafe_allow_html=True)
    st.markdown('<p class="info">Predict the likelihood of a customer defaulting on credit based on their financial details.</p>', unsafe_allow_html=True)

    # Sidebar: Input Parameters
    st.sidebar.title("Input Parameters")
    st.sidebar.markdown('Fill in the details below to predict the likelihood of default.')

    # Inputs for all features in the sidebar with sliders and better layout
    credit_score = st.sidebar.slider("Credit Score", min_value=300, max_value=850, value=600)
    account_balance = st.sidebar.slider("Account Balance", min_value=0, max_value=100000, value=50000)
    transaction_count = st.sidebar.slider("Transaction Count", min_value=0, max_value=100, value=10)
    job = st.sidebar.selectbox(
        "Job",
        options=["Other", "IT Professional", "Entry-Level", "Skilled Worker", "Executive", "Managerial"],
        index=0
    )
    income = st.sidebar.slider("Income", min_value=0, max_value=200000, value=50000)

    # Create a dictionary for job mapping
    job_mapping = {
        "Other": 4, "IT Professional": 2, "Entry-Level": 0, "Skilled Worker": 5,
        "Executive": 3, "Managerial": 1
    }
    job_encoded = job_mapping[job]

    # Button to trigger prediction
    if st.sidebar.button("Predict"):
        features = [credit_score, account_balance, transaction_count, job_encoded, income]
        prediction = predict_default(features)

        # Output the prediction with a more informative message and design
        if prediction[0] == 0:
            st.success("The customer is **Not Likely** to Default. 🎉", icon="🎉")
        else:
            st.warning("The customer is **Likely** to Default. ⚠️", icon="⚠️")
        
        # Explanation of prediction result with visible text color
        if prediction[0] == 0:
            st.markdown('<p class="prediction-info">This prediction means that based on the financial profile, the customer is considered less risky and unlikely to default. 🎉</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="prediction-info">This prediction means that based on the financial profile, the customer is considered more risky and likely to default. ⚠️</p>', unsafe_allow_html=True)

    # Additional information about the Random Forest Model
    st.sidebar.markdown("### About the Model")
    st.sidebar.markdown("""
        **Random Forest Classifier**:
        - Random Forest is an ensemble learning method, which combines the predictions of multiple decision trees to improve the model's accuracy and robustness.
        - It works by creating several decision trees, each trained on a random subset of the data. The final prediction is made by averaging the results of all trees (for regression) or taking a vote (for classification).
        - It is highly effective at handling both classification and regression tasks and works well with complex datasets containing non-linear relationships.
    """)

    st.sidebar.markdown("### Instructions")
    st.sidebar.info(
        """
        1. Enter the customer's details in the sidebar.
        2. Click on "Predict" to check the likelihood of default.
        3. Use sliders and dropdowns for easier input.
        """
    )

if __name__ == '__main__':
    main()
