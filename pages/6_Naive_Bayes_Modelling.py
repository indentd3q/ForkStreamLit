import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import RandomOverSampler, BorderlineSMOTE, ADASYN, SMOTEN, KMeansSMOTE
from imblearn.combine import SMOTEENN, SMOTETomek
from sklearn.metrics import accuracy_score, classification_report, f1_score, precision_score, recall_score

def main():
    # App Title
    st.title("Naive Bayes with Balancing and Hyperparameters")

    # Upload dataset
    uploaded_file = st.file_uploader("Upload your dataset (.csv or .xlsx)", type=["csv", "xlsx"])

    if uploaded_file:
        # Load dataset
        if uploaded_file.name.endswith(".csv"):
            data = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            data = pd.read_excel(uploaded_file)

        st.write("Uploaded Dataset", data)

        features_df = data.iloc[:, 1:]
        features_df = features_df.round().astype(int).T
        X = np.asarray(features_df)

        # Dataset Configuration
        col1, col2 = st.columns(2)
        with col1:
            # Select index column
            index_col = st.selectbox("Select Index Column", options=data.columns)
            data = data.set_index(index_col)
            data = data.round().astype(int)
            data = data.T

        with col2:
            # Generate label column
            data['label'] = ['cancer' if '-01' in sample else 'normal' for sample in data.index]
            y = np.asarray(data['label'])

            # Display class distribution
            st.write("Class Distribution", data['label'].value_counts())

        # Data Splitting Configuration
        col3, col4, col5 = st.columns(3)
        with col3:
            test_size = st.slider("Test Set Size (%)", min_value=10, max_value=50, value=40, step=1) / 100
        
        with col4:
            stratify_option = st.checkbox("Stratify Split", value=True)
        
        with col5:
            random_state = st.number_input("Random State", min_value=0, value=42)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y if stratify_option else None
        )

        st.write("Training Set Size:", len(X_train))
        st.write("Test Set Size:", len(X_test))

        # Balancing Methods and Configuration
        col6, col7 = st.columns(2)
        with col6:
            selected_balancing_methods = st.multiselect(
                "Select Balancing Methods",
                options=[
                    'RandomOverSampler', 'SMOTEENN', 'SMOTETomek',
                    'ADASYN', 'BorderlineSMOTE', 'KMeansSMOTE', 'No Balancing',
                ],
                default=["No Balancing"]
            )

        with col7:
            sampling_strategy = st.slider(
                "Sampling Strategy (proportion of the minority class)", 
                min_value=0.1, max_value=1.0, value=0.3, step=0.1
            )

        # Hyperparameter Tuning
        col8, col9 = st.columns(2)
        with col8:
            use_hyperparameter_tuning = st.radio("Use Hyperparameter Tuning?", options=['Yes', 'No'], index=1)
        
        param_grid = {
            'var_smoothing': np.logspace(0, -9, num=100)
        }

        results_df = pd.DataFrame(columns=[
            'Balancing Method', 'Train Accuracy', 'Test Accuracy', 'Test F1 Score', 
            'Test Precision', 'Test Recall', 'Train Classification Report', 'Test Classification Report'
        ])

        # Process each balancing method
        for method_name in selected_balancing_methods:
            st.write(f"Processing with {method_name}...")

            # Dynamically create balancing method instances
            if method_name == 'RandomOverSampler':
                balancing_method = RandomOverSampler(random_state=random_state, sampling_strategy=sampling_strategy)
            elif method_name == 'SMOTEENN':
                balancing_method = SMOTEENN(random_state=random_state, sampling_strategy=sampling_strategy)
            elif method_name == 'SMOTETomek':
                balancing_method = SMOTETomek(random_state=random_state, sampling_strategy=sampling_strategy)
            elif method_name == 'ADASYN':
                balancing_method = ADASYN(random_state=random_state, sampling_strategy=sampling_strategy)
            elif method_name == 'BorderlineSMOTE':
                balancing_method = BorderlineSMOTE(random_state=random_state, sampling_strategy=sampling_strategy)
            elif method_name == 'KMeansSMOTE':
                balancing_method = KMeansSMOTE(random_state=random_state, sampling_strategy=sampling_strategy)
            elif method_name == 'SMOTEN':
                balancing_method = SMOTEN(random_state=random_state, sampling_strategy=sampling_strategy)
            elif method_name == "No Balancing":
                balancing_method = "No Balancing"

            if balancing_method == "No Balancing":
                X_train_resampled, y_train_resampled = X_train, y_train
            else:
                X_train_resampled, y_train_resampled = balancing_method.fit_resample(X_train, y_train)

            # Encode labels
            label_encoder = LabelEncoder()
            y_train_encoded = label_encoder.fit_transform(y_train_resampled)
            y_test_encoded = label_encoder.transform(y_test)

            # Train model
            if use_hyperparameter_tuning == "Yes":
                grid_search = GridSearchCV(GaussianNB(), param_grid, cv=5, scoring='accuracy', n_jobs=-1, verbose=0, return_train_score=True)
                grid_search.fit(X_train_resampled, y_train_encoded)
                model = grid_search.best_estimator_
                st.write("Best Hyperparameters:", grid_search.best_params_)
            else:
                model = GaussianNB()
                model.fit(X_train_resampled, y_train_encoded)

            # Evaluate model
            y_pred_train = model.predict(X_train_resampled)
            y_pred_test = model.predict(X_test)

            train_accuracy = accuracy_score(y_train_encoded, y_pred_train)
            test_accuracy = accuracy_score(y_test_encoded, y_pred_test)
            test_f1 = f1_score(y_test_encoded, y_pred_test, average='weighted')
            test_precision = precision_score(y_test_encoded, y_pred_test, average='weighted')
            test_recall = recall_score(y_test_encoded, y_pred_test, average='weighted')

            train_class_report = classification_report(y_train_encoded, y_pred_train, target_names=label_encoder.classes_)
            test_class_report = classification_report(y_test_encoded, y_pred_test, target_names=label_encoder.classes_)

            # Append results
            new_row = pd.DataFrame({
                'Balancing Method': [method_name],
                'Train Accuracy': [train_accuracy],
                'Test Accuracy': [test_accuracy],
                'Test F1 Score': [test_f1],
                'Test Precision': [test_precision],
                'Test Recall': [test_recall],
                'Train Classification Report': [train_class_report],
                'Test Classification Report': [test_class_report]
            })
            results_df = pd.concat([results_df, new_row], ignore_index=True)

        # Display results
        st.write("Results", results_df)

        # Download option
        @st.cache_data
        def convert_to_excel(df, file_path):
            with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='results')
            return file_path

        # Save DataFrame to a temporary path
        file_path = convert_to_excel(results_df, "results.xlsx")

        st.download_button(
            label="Download Results as XLSX",
            data=open(file_path, "rb").read(),
            file_name="results.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("Please upload a dataset to proceed.")

if __name__ == "__main__":
    main()