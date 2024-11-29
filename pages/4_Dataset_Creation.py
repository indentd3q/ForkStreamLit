import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(layout="wide", page_title="Dataset Creation Tool")

# Title and Description
st.title("🧬 Dataset Creation for Machine Learning")
st.markdown("*Effortlessly filter and prepare your gene expression datasets*")

# Create two main columns
col1, col2 = st.columns([1, 1])

with col1:
    # DEG Genes File Uploader
    st.header("📤 Upload DEG Genes")
    deg_file = st.file_uploader("Select Differentially Expressed Genes (DEG) File", 
                                type=['csv'], 
                                key="deg_upload")

with col2:
    # Combined Dataset Uploader
    st.header("📊 Upload Combined Dataset")
    dataset_file = st.file_uploader("Select Combined Dataset", 
                                    type=['csv'], 
                                    key="dataset_upload")

# Process files if both are uploaded
if deg_file and dataset_file:
    # Read Files
    ensembl_id = pd.read_csv(deg_file)
    dataset = pd.read_csv(dataset_file)

    # Tabs for different views
    tab1, tab2, tab3 = st.tabs(["📋 Ensembl IDs", "🔍 Filtered Dataset", "📥 Export"])

    with tab1:
        st.header("Gene File Ensembl IDs")
        # Get Ensembl IDs
        ensembl_ids = ensembl_id['Ensembl_ID']
        
        # Display Ensembl IDs with pagination
        st.dataframe(ensembl_ids, use_container_width=True)
        
        # Basic stats
        st.metric("Total Unique Genes", len(ensembl_ids))

    with tab2:
        # Filter Dataset
        st.header("Created Counts Dataset")
        regulated_genes = dataset[dataset['Ensembl_ID'].isin(ensembl_ids)]
        regulated_genes = regulated_genes.set_index('Ensembl_ID')

        # Display filtered genes with improved formatting
        st.dataframe(regulated_genes, use_container_width=True)
        
        # Additional insights
        st.write(f"**Total Filtered Genes:** {len(regulated_genes)}")
        st.write(f"**Columns in Dataset:** {', '.join(regulated_genes.columns)}")

    with tab3:
        st.header("Export Filtered Dataset")
        
        # Multiple download options
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.download_button(
                label="💾 Download as CSV",
                data=regulated_genes.to_csv(index=True),
                file_name='Filtered_Dataset.csv',
                mime='text/csv',
                use_container_width=True
            )
        
        with col_b:
            st.download_button(
                label="📄 Download as Excel",
                data=regulated_genes.to_excel(index=True),
                file_name='Filtered_Dataset.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                use_container_width=True
            )

else:
    # Guidance for user when no files are uploaded
    st.info("""
    ### 📡 Ready to Create Your Dataset
    1. Upload a CSV file with Ensembl IDs
    2. Upload a combined dataset CSV
    3. The app will automatically filter and prepare your data
    """)