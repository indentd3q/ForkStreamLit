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
        background: linear-gradient(135deg, #f0f8ff 0%, #e6f2ff 100%);
    }
    .stTitle {
        color: #0066cc;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,102,204,0.2);
        text-align: center;
    }
    .stMarkdown {
        color: #2c3e50;
    }
    .stInfo {
        background-color: #e6f3ff;
        border-left: 6px solid #00a2ff;
        border-radius: 5px;
        box-shadow: 0 4px 6px rgba(0,162,255,0.1);
        padding: 15px;
    }
    .creator-card {
        background-color: #ffffff;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        padding: 20px;
        text-align: center;
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
           - *Source*: RNA-seq datasets (STAR-Counts)
           - *Format*: Tabular data 
           - *Columns*: Genes as rows, samples as columns
           - *Content*: Normalized gene expression levels

        2. **Phenotype Data:**
           - *Source*: Clinical datasets (GDC TCGA)
           - *Format*: Sample metadata
        """)

    with col2:
        st.info("""
        🚀 **Research Accelerator**
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
            <div class="creator-card">
                <h3>{creator['image']} {creator['name']}</h3>
                <p><strong>Role:</strong> {creator['role']}</p>
                <p><strong>Expertise:</strong> {creator['expertise']}</p>
            </div>
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