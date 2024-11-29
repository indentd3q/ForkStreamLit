import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Cancer Detection Feature Selection", 
    page_icon="🧬", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    .reportview-container { 
        background-color: #f0f8ff; 
    }
    .stTitle {
        color: white;
        font-weight: bold;
    }
    .stMarkdown {
        color: white;
    }
    .stInfo {
        background-color: #e6f3ff;
        border-left: 6px solid #00a2ff;
        box-shadow: 0 4px 6px rgba(0,162,255,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Main Content Sections
def main():
    # Bright Title
    st.title("🧬 Optimized Feature Selection for Cancer Detection")

    # Workflow Section
    st.markdown("### 🌟 Advanced Genomic Exploration Platform")

    # Create two columns for data requirements and info
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        #### **Data Requirements:**
        1. **Gene Expression Data:**
           - *Source*: RNA-seq datasets (STAR-Counts), Retrieved from XenaBrowser by UCSC
           - *Format*: Tabular data 
           - *Columns*: Genes as rows, samples as columns
           - *Content*: Normalized gene expression levels

        2. **Phenotype Data:**
           - *Source*: Clinical datasets (GDC TCGA), Retrieved from XenaBrowser by UCSC
           - *Format*: Sample metadata
        """)

    with col2:
        st.info("""
        🚀 **Research Insights**
        - TCGA-Compliant Processing
        - Advanced Genomic Insights
        - Machine Learning Integration
        """)

    # Creator Section
    st.markdown("### 👥 Research Team")
    
    # Create columns for creator profiles
    creator_cols = st.columns(3)
    
    creators = [
        {
            "name": "Dr. Emily Rodriguez",
            "role": "Principal Investigator",
            "expertise": "Computational Genomics",
            "image": "🧬"
        },
        {
            "name": "Alex Chen",
            "role": "Data Scientist",
            "expertise": "Machine Learning",
            "image": "🤖"
        },
        {
            "name": "Dr. Michael Wong",
            "role": "Bioinformatics Specialist",
            "expertise": "Cancer Research",
            "image": "🔬"
        }
    ]
    
    for i, creator in enumerate(creators):
        with creator_cols[i]:
            st.markdown(f"""
            {creator['image']} **{creator['name']}**

            **Role:** {creator['role']}  
            **Expertise:** {creator['expertise']}
            """, unsafe_allow_html=True)

    # Future Work Section
    st.markdown("### 🔮 Future Directions")
    st.markdown("""
    - Expand machine learning models
    - Integrate more diverse datasets
    - Develop personalized cancer prediction algorithms
    """)

# Run the main function
if __name__ == "__main__":
    main()
