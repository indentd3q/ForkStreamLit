import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Cancer Detection Feature Selection", 
    page_icon="🧬", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .reportview-container { 
        background-color: #f0f2f6; 
    }
    .stTitle {
        color: #2c3e50;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Main Page
st.title("🧬 Optimized Feature Selection for Cancer Detection")

# Subtitle with styled information
st.markdown("""
    ### Advanced Genomic Analysis Platform
    
    **Key Requirements:**
    - Ensure sample IDs follow TCGA format
    - Prepare high-quality genomic datasets
""")

# Quick Start Guide
st.info("""
    🚀 Quick Start:
    1. Prepare your genomic data
    2. Ensure TCGA sample ID formatting
    3. Navigate through feature selection tools
""")

# Optional additional context
st.markdown("""
    #### About This Application
    Cutting-edge tool for precise cancer detection using advanced feature selection techniques.
""")