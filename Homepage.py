import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Cancer Detection Feature Selection", 
    page_icon="🧬", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Bright and vibrant custom CSS
st.markdown("""
    <style>
    .reportview-container { 
        background-color: #f0f8ff; 
    }
    .stTitle {
        color: #0066cc;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,102,204,0.2);
    }
    .stMarkdown {
        color: #2c3e50;
    }
    .stInfo {
        background-color: #e6f3ff;
        border-left: 6px solid #00a2ff;
        box-shadow: 0 4px 6px rgba(0,162,255,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Bright Title
st.title("🧬 Optimized Feature Selection for Cancer Detection using Machine Learning")

# Workflow with Vibrant Formatting
st.markdown("""
    ### 🌟 Advanced Genomic Exploration Platform

    #### **Workflow Dynamics:**
    1. **Data Segregation** 🔍
       - Precision phenotype processing
       - Targeted racial demographic analysis

    2. **Gene Expression Analysis** 📊
       - Intelligent Data Refinement
       - Molecular Pattern Recognition

    3. **Performance Validation** ✨
       - Comprehensive Gene Screening
       - Predictive Marker Identification

    4. **Intelligent Modeling** 🤖
       - Multi-Model Predictive Strategies
       - Adaptive Machine Learning Techniques
""")

# Bright Call to Action
st.info("""
    🚀 **Accelerate Your Research**
    - TCGA-Compliant Data Processing
    - Cutting-Edge Genomic Insights
""")

