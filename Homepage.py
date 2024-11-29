import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Cancer Detection Feature Selection", 
    page_icon="🧬", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .reportview-container { 
        background-color: #f4f6f9; 
    }
    .stTitle {
        color: #1a5f7a;
        font-weight: bold;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .stMarkdown {
        color: #2c3e50;
    }
    .stInfo {
        background-color: #e6f2ff;
        border-left: 5px solid #3498db;
    }
    </style>
""", unsafe_allow_html=True)

# Main Page Title
st.title("🧬 Comprehensive Cancer Detection Pipeline")

# Workflow Overview
st.markdown("""
    ### Advanced Genomic Analysis Platform

    #### Workflow Stages:
    1. **Data Segregation**
       - Process phenotype and counts files
       - Segment data based on white race criteria

    2. **Differential Expression Gene (DEG) Analysis**
       - Data Cleaning
         * Remove missing values
         * Round values to integers
       - Data Labeling
         * Classify samples as normal or cancer
       - Feature Selection
         * Identify most significant genes
         * Prepare for ROC analysis

    3. **ROC Analysis**
       - Evaluate gene performance
       - Select top-performing genes

    4. **Predictive Modeling**
       - Supported Models:
         * Support Vector Machine (SVM)
         * Naive Bayes
         * Logistic Regression
       
       Key Modeling Steps:
       - Data Splitting (normal vs. cancer)
       - Data Balancing (1:3 ratio)
       - Hyperparameter Tuning
       - Model Performance Comparison
""")

# Quick Start Guide
st.info("""
    🚀 **Getting Started**
    - Ensure sample IDs follow TCGA format
    - Prepare high-quality genomic datasets
    - Navigate through intuitive feature selection tools
""")

# Additional Context
st.markdown("""
    #### About This Application
    A cutting-edge genomic analysis platform designed to streamline cancer detection 
    through advanced feature selection and machine learning techniques.
""")