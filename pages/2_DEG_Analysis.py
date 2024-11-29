import streamlit as st
import pandas as pd
import numpy as np
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

def main():
    st.set_page_config(page_title="DEG Analysis", layout="wide")
    st.title("🧬 Differential Gene Expression Analysis")

    # File Upload Section
    st.header("📂 Data Upload")
    racial_dataset = st.file_uploader(
        "Upload Counts Data", 
        type=["csv", "xlsx"], 
        help="Upload your gene expression counts data"
    )

    if racial_dataset:
        data = load_and_preprocess_data(racial_dataset)
        
        tab1, tab2, tab3 = st.tabs([
            "📊 Data Overview", 
            "🧮 DEG Analysis", 
            "🔍 Filtered Results"
        ])
        
        with tab1:
            display_data_overview(data)
        
        with tab2:
            deg_results = perform_deg_analysis(data)
            st.write("DEG Statistics Results")
            st.dataframe(deg_results)
        
        with tab3:
            deg_filtering_section(deg_results)

def load_and_preprocess_data(uploaded_file):
    st.success("File Uploaded Successfully!")
    
    if uploaded_file.name.endswith(".csv"):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file, engine="openpyxl")
    
    data = data.set_index("Ensembl_ID")
    data = data.fillna(0)
    data = data.round().astype(np.int32)
    data = data[data.sum(axis=1) > 0]
    data = data.T
    
    return data

def display_data_overview(data):
    st.subheader("Preprocessed Counts Data")
    st.dataframe(data.head(5))
    
    metadata = create_metadata(data)
    st.subheader("Metadata")
    st.dataframe(metadata)

def create_metadata(counts_data):
    conditions = ['cancer' if '-01' in sample else 'normal' for sample in counts_data.index]
    metadata = pd.DataFrame({'Ensembl_ID': counts_data.index, 'Condition': conditions})
    return metadata.set_index('Ensembl_ID')

def perform_deg_analysis(data):
    metadata = create_metadata(data)
    
    dds = DeseqDataSet(
        counts=data,
        metadata=metadata,
        design_factors="Condition",
        n_cpus=-1
    )
    dds.deseq2()
    
    stat_res = DeseqStats(dds, contrast=("Condition", "cancer", "normal"))
    stat_res.summary()
    
    return stat_res.results_df

def deg_filtering_section(deg_results):
    st.subheader("DEG Filtering Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cutoff_padj = st.number_input("Padj Cutoff", value=0.05, min_value=0.0, max_value=1.0, step=0.01)
        cutoff_log2FoldChange = st.number_input("Log2 Fold Change", value=0.0, step=0.5)
    
    with col2:
        cutoff_baseMean = st.number_input("Base Mean", value=10, min_value=0)
        cutoff_pvalue = st.number_input("P-value", value=0.0, min_value=0.0, max_value=1.0, step=0.01)
    
    with col3:
        cutoff_lfcSE = st.number_input("LFC Standard Error", value=0.0, step=0.1)
        cutoff_stat = st.number_input("Stat", value=0.0, step=0.1)
    
    if st.button("Apply Filters"):
        filtered_results = filter_deg_results(
            deg_results, 
            cutoff_padj, 
            cutoff_log2FoldChange, 
            cutoff_baseMean, 
            cutoff_pvalue, 
            cutoff_lfcSE, 
            cutoff_stat
        )
        
        st.subheader("Filtered Results")
        st.dataframe(filtered_results)
        
        st.subheader("DEG Genes")
        st.write(filtered_results.index.to_list())

def filter_deg_results(
    deg_results, 
    cutoff_padj, 
    cutoff_log2FoldChange, 
    cutoff_baseMean, 
    cutoff_pvalue, 
    cutoff_lfcSE, 
    cutoff_stat
):
    filtered_results = deg_results.copy()
    
    filtered_results = filtered_results[filtered_results['padj'] < cutoff_padj]
    filtered_results = filtered_results[filtered_results['log2FoldChange'].abs() > cutoff_log2FoldChange]
    filtered_results = filtered_results[filtered_results['baseMean'] > cutoff_baseMean]
    filtered_results = filtered_results[filtered_results['pvalue'] < cutoff_pvalue]
    filtered_results = filtered_results[filtered_results['lfcSE'] > cutoff_lfcSE]
    filtered_results = filtered_results[filtered_results['stat'].abs() > cutoff_stat]
    
    return filtered_results

if __name__ == "__main__":
    main()