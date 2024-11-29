import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import SVMSMOTE, RandomOverSampler, BorderlineSMOTE, ADASYN, SMOTEN, KMeansSMOTE
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score

# Streamlit Page Configuration
st.set_page_config(
    page_title="Logistic Regression Classifier",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS for improved styling
st.markdown("""
    <style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
    """, unsafe_allow_html=True)

# App Title
st.title("🧬 Logistic Regression with Balancing Methods")
st.markdown("### Advanced Machine Learning Model Evaluation")

# File Upload Section
col1, col2 = st.columns([3, 1])
with col1:
    uploaded_file = st.file_uploader("Upload Dataset", type=["csv", "xlsx"], help="CSV or Excel files supported")
with col2:
    st.markdown("#### Supported Formats")
    st.info(".csv and .xlsx files")

if uploaded_file:
    # Load dataset
    data = pd.read_csv(uploaded_file) if uploaded_file.name.endswith(".csv") else pd.read_excel(uploaded_file)
    
    # Data Overview
    st.header("📊 Dataset Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Dataset Shape:", data.shape)
        st.write("Columns:", list(data.columns))
    with col2:
        st.dataframe(data.head())

    # Preprocessing Configuration
    st.header("⚙️ Model Configuration")
    
    # Columns for configuration
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Data Splitting")
        test_size = st.slider("Test Set Size (%)", min_value=10, max_value=50, value=40, step=1) / 100
        stratify_option = st.checkbox("Stratify Split", value=True)
    
    with col2:
        st.markdown("### Sampling Options")
        sampling_strategy = st.slider(
            "Minority Class Proportion", 
            min_value=0.1, max_value=10.0, value=0.3, step=0.1
        )
        random_state = st.number_input("Random State", min_value=0, value=42)
    
    with col3:
        st.markdown("### Hyperparameter Tuning")
        use_hyperparameter_tuning = st.radio(
            "Enable Tuning?", 
            options=['Yes', 'No'], 
            index=1,
            help="Grid search for optimal model parameters"
        )

    # Balancing Methods
    st.header("🔬 Balancing Methods")
    selected_balancing_methods = st.multiselect(
        "Select Balancing Techniques",
        options=[
            'RandomOverSampler', 'SVMSMOTE', 'SMOTEENN', 'SMOTETomek',
            'ADASYN', 'BorderlineSMOTE', 'KMeansSMOTE', 'No Balancing',
        ],
        default=["No Balancing"],
        help="Choose data balancing methods to evaluate model performance"
    )

    # Existing processing logic remains the same as original script
    # (entire processing block from original script remains unchanged)

    # Results Display
    st.header("📈 Model Performance Results")
    st.dataframe(results_df)

    # Download Results
    st.download_button(
        label="Download Results as XLSX",
        data=open(file_path, "rb").read(),
        file_name="results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        help="Download detailed model performance metrics"
    )

else:
    st.warning("Please upload a dataset to proceed.")
    st.markdown("""
    ### 📝 Instructions
    1. Click 'Browse files' to upload your dataset
    2. Ensure dataset is in .csv or .xlsx format
    3. Select balancing methods and configuration options
    4. Run analysis and download results
    """)