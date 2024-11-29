import streamlit as st
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# Streamlit Page Configuration
st.set_page_config(
    page_title="DEG Analysis Tool",
    page_icon="🧬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .reportview-container { background-color: #f0f2f6; }
    .stButton>button { 
        background-color: #4CAF50; 
        color: white; 
        font-weight: bold; 
    }
    </style>
    """, unsafe_allow_html=True)

# App Title
st.title("🧬 Differential Gene Expression Analysis")
st.markdown("### Comprehensive Gene Expression Profiling")

# File Upload Section
col1, col2 = st.columns([3, 1])
with col1:
    racial_dataset = st.file_uploader(
        "Upload Phenotype Data", 
        type=["csv"], 
        help="CSV file with gene expression counts"
    )
with col2:
    st.markdown("#### File Requirements")
    st.info("CSV with Ensembl_ID column")

if racial_dataset:
    # Data Preprocessing
    st.header("📊 Data Preprocessing")
    data = pd.read_csv(racial_dataset)
    data = data.set_index("Ensembl_ID")
    data = data.fillna(0)
    data = data.round().astype(int)
    data = data[data.sum(axis=1) > 0]
    data = data.T

    col1, col2 = st.columns(2)
    with col1:
        st.write("Preprocessed Counts Data")
        st.dataframe(data.head(5))
    
    with col2:
        # Create Metadata
        metadata = pd.DataFrame(index=data.index)
        metadata['label'] = [
            'cancer' if '-01' in sample else 'normal' for sample in metadata.index
        ]
        st.write("Metadata Overview")
        st.dataframe(metadata)

    # DEG Analysis Configuration
    st.header("🔬 DEG Analysis Settings")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Analysis Parameters")
        contrast_choice = st.radio(
            "Select Contrast", 
            ["cancer", "normal"],
            help="Choose comparison group"
        )

    with col2:
        st.markdown("### Filtering Thresholds")
        cutoff_padj = st.number_input("padj Cutoff", value=0.05, format="%.3f")
        cutoff_log2FoldChange = st.number_input("log2FC Cutoff", value=0.0, format="%.2f")

    # Perform DEG Analysis
    def initiate_deg(counts_data, metadata):
        dds = DeseqDataSet(
            counts=counts_data,
            metadata=metadata,
            design_factors="label"
        )
        dds.deseq2()
        stat_res = DeseqStats(dds, contrast=("label", "cancer", "normal"))
        stat_res.summary()
        return stat_res.results_df

    deg_stats_results = initiate_deg(data, metadata)

    # Advanced Filtering
    st.header("🧩 Advanced Filtering")
    col1, col2 = st.columns(2)
    
    with col1:
        additional_cutoffs = st.expander("More Filtering Options")
        with additional_cutoffs:
            cutoff_baseMean = st.number_input("Base Mean Cutoff", value=10)
            cutoff_pvalue = st.number_input("P-value Cutoff", value=0.0, format="%.3f")

    with col2:
        additional_cutoffs = st.expander("Statistical Thresholds")
        with additional_cutoffs:
            cutoff_lfcSE = st.number_input("LFC Std Error Cutoff", value=0.0, format="%.2f")
            cutoff_stat = st.number_input("Stat Cutoff", value=0.0, format="%.2f")

    # Filter DEG Results
    def filter_deg_results(deg_results):
        filtered = deg_results[
            (deg_results['padj'] < cutoff_padj) & 
            (deg_results['log2FoldChange'].abs() > cutoff_log2FoldChange) & 
            (deg_results['baseMean'] > cutoff_baseMean) &
            (deg_results['pvalue'] < cutoff_pvalue) &
            (deg_results['lfcSE'] > cutoff_lfcSE) &
            (deg_results['stat'].abs() > cutoff_stat)
        ]
        return filtered

    filtered_deg_results = filter_deg_results(deg_stats_results)

    # Results Visualization
    st.header("📈 Analysis Results")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("DEG Statistics Results")
        st.dataframe(deg_stats_results)
    
    with col2:
        st.write("Filtered DEG Results")
        st.dataframe(filtered_deg_results)

    # Differential Genes
    st.subheader("🧬 Differentially Expressed Genes")
    deg_genes = filtered_deg_results.index.to_list()
    st.write(f"Total DEG Genes: {len(deg_genes)}")
    st.dataframe(deg_genes)

else:
    st.warning("Please upload a dataset to proceed.")
    st.markdown("""
    ### 📝 Instructions
    1. Upload CSV with gene expression data
    2. Ensure 'Ensembl_ID' column is present
    3. Adjust analysis and filtering parameters
    4. Review differential gene expression results
    """)