import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import (
    SVMSMOTE, RandomOverSampler, BorderlineSMOTE,
    ADASYN, SMOTEN, KMeansSMOTE
)
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

    # Select Target Column
    st.header("⚙️ Preprocessing and Model Configuration")
    target_col = st.selectbox("Select Target Column", options=data.columns)
    features = data.drop(columns=[target_col])
    target = data[target_col]

    # Encode target if categorical
    if target.dtype == 'object':
        le = LabelEncoder()
        target = le.fit_transform(target)

    # Data Splitting Options
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### Data Splitting")
        test_size = st.slider("Test Set Size (%)", min_value=10, max_value=50, value=40, step=1) / 100
        stratify_option = st.checkbox("Stratify Split", value=True)
    with col2:
        st.markdown("### Sampling Options")
        sampling_strategy = st.slider("Minority Class Proportion", min_value=0.1, max_value=1.0, value=0.3, step=0.1)
        random_state = st.number_input("Random State", min_value=0, value=42)
    with col3:
        st.markdown("### Hyperparameter Tuning")
        use_hyperparameter_tuning = st.radio(
            "Enable Tuning?", options=['Yes', 'No'], index=1,
            help="Grid search for optimal model parameters"
        )

    # Balancing Methods
    st.header("🔬 Balancing Methods")
    balancing_methods = {
        'RandomOverSampler': RandomOverSampler,
        'SVMSMOTE': SVMSMOTE,
        'SMOTEENN': SMOTEENN,
        'SMOTETomek': SMOTETomek,
        'ADASYN': ADASYN,
        'BorderlineSMOTE': BorderlineSMOTE,
        'KMeansSMOTE': KMeansSMOTE,
        'No Balancing': None
    }
    selected_methods = st.multiselect(
        "Select Balancing Techniques",
        options=balancing_methods.keys(),
        default=["No Balancing"],
        help="Choose data balancing methods to evaluate model performance"
    )

    # Train-test split
    stratify = target if stratify_option else None
    X_train, X_test, y_train, y_test = train_test_split(
        features, target, test_size=test_size, random_state=random_state, stratify=stratify
    )

    # Initialize results DataFrame
    results_df = pd.DataFrame(columns=[
        'Balancing Method', 'Accuracy', 'Precision', 'Recall', 'F1-Score'
    ])

    # Evaluate models with selected balancing methods
    for method in selected_methods:
        if method == 'No Balancing':
            X_resampled, y_resampled = X_train, y_train
        else:
            sampler = balancing_methods[method](sampling_strategy=sampling_strategy, random_state=random_state)
            X_resampled, y_resampled = sampler.fit_resample(X_train, y_train)

        # Model training
        model = LogisticRegression(random_state=random_state, max_iter=500)
        if use_hyperparameter_tuning == 'Yes':
            param_grid = {'C': [0.1, 1, 10], 'solver': ['lbfgs', 'liblinear']}
            grid_search = GridSearchCV(model, param_grid, cv=3, scoring='f1')
            grid_search.fit(X_resampled, y_resampled)
            model = grid_search.best_estimator_
        else:
            model.fit(X_resampled, y_resampled)

        # Predictions and evaluation
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted')
        recall = recall_score(y_test, y_pred, average='weighted')
        f1 = f1_score(y_test, y_pred, average='weighted')

        # Append results
        results_df = pd.concat([results_df, pd.DataFrame([{
            'Balancing Method': method,
            'Accuracy': accuracy,
            'Precision': precision,
            'Recall': recall,
            'F1-Score': f1
        }])], ignore_index=True)

    # Display results
    st.header("📈 Model Performance Results")
    st.dataframe(results_df)

    # Download Results
    @st.cache_data
    def convert_df_to_excel(df):
        return df.to_excel(index=False)

    st.download_button(
        label="Download Results as XLSX",
        data=convert_df_to_excel(results_df),
        file_name="results.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
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
