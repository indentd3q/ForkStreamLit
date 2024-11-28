import streamlit as st
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# Separates Phenotypes by Race
def seperateByRace(file, race, race_col):
    """
    Searches the phenotype dataframe for the race.demographic column
    and returns a new dataframe with only the rows that contain the race.
    """
    return file[file[race_col].str.contains(race, case=False, na=False)]

# Matches Sample ID from phenotypes to counts
def matchingDNA(phenotypeDATA, countsDATA, phenotype_sample_col, counts_sample_col):
    """
    Matches the race phenotype data to the counts data 
    and returns a racial-dataframe with the matching data.
    """
    colA1 = phenotypeDATA[phenotype_sample_col]

    newFile = countsDATA[['Ensembl_ID'] + [col for col in colA1 if col in countsDATA[counts_sample_col]]]
    return pd.DataFrame(newFile)

# App Title
st.title("Differential Gene Expression Analysis with PyDESeq2")

# File Uploads
st.header("Input Files")
phenotypeFile = st.file_uploader("Upload Phenotype Data (CSV)", type=["csv"])
countsFile = st.file_uploader("Upload Counts Data (CSV)", type=["csv"])

if phenotypeFile and countsFile:
    phenotype = pd.read_csv(phenotypeFile)
    counts = pd.read_csv(countsFile)

    # Configurable Columns
    st.header("Column Selections")
    phenotype_race_col = st.selectbox(
        "Select Race Column in Phenotype Data", phenotype.columns
    )
    phenotype_sample_col = st.selectbox(
        "Select Sample ID Column in Phenotype Data", phenotype.columns
    )
    counts_sample_col = st.selectbox(
        "Select Sample ID Column in Counts Data", counts.columns
    )

    # Process by Race
    st.header("Race Selection and Preprocessing")
    phenotype_unique_races = phenotype[phenotype_race_col].unique()
    selected_race = st.selectbox("Select Race to Analyze", phenotype_unique_races)

    phenotype_race_df = seperateByRace(phenotype, selected_race, phenotype_race_col)
    counts_race_df = matchingDNA(
        phenotype_race_df, counts, phenotype_sample_col, counts_sample_col
    )

    def preprocess_deg(counts_data, index_col):
        counts_data = counts_data.set_index(index_col)
        return counts_data

    preprocessed_counts_data = preprocess_deg(counts_race_df, counts_sample_col)
    preprocessed_counts_data = preprocessed_counts_data.fillna(0)
    preprocessed_counts_data = preprocessed_counts_data.round().astype(int)
    preprocessed_counts_data = preprocessed_counts_data[preprocessed_counts_data.sum(axis=1) > 0]
    preprocessed_counts_data = preprocessed_counts_data.T
    st.write("Preprocessed Counts Data", preprocessed_counts_data)

    # Create Metadata
    def create_metadata(counts_data):
        metadata = pd.DataFrame(index=counts_data.index)
        metadata['label'] = [
            'cancer' if '-01' in sample else 'normal' for sample in metadata.index
        ]
        return metadata

    metadata = create_metadata(preprocessed_counts_data)
    st.write("Metadata", metadata)

    # DEG Analysis
    st.header("DEG Analysis")
    contrast_choice = st.radio("Select Contrast for Analysis", ["cancer", "normal"])

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

    deg_stats_results = initiate_deg(preprocessed_counts_data, metadata)
    st.write("DEG Statistics Results", deg_stats_results)

    # Filter DEG Results
    st.header("DEG Filtering Options")
    cutoff_padj = st.number_input("Cutoff for padj", value=0.05)
    cutoff_log2FoldChange = st.number_input("Cutoff for log2FoldChange", value=0.5)
    cutoff_baseMean = st.number_input("Cutoff for baseMean", value=10)
    cutoff_pvalue = st.number_input("Cutoff for pvalue", value=0.05)
    cutoff_lfcSE = st.number_input("Cutoff for lfcSE", value=0.1)
    cutoff_stat = st.number_input("Cutoff for stat", value=0.1)

    def filter_deg_results(deg_results):
        deg_results = deg_results[deg_results['padj'] < cutoff_padj]
        deg_results = deg_results[deg_results['log2FoldChange'] > cutoff_log2FoldChange]
        deg_results = deg_results[deg_results['baseMean'] > cutoff_baseMean]
        deg_results = deg_results[deg_results['pvalue'] > cutoff_pvalue]
        deg_results = deg_results[deg_results['lfcSE'] > cutoff_lfcSE]
        deg_results = deg_results[deg_results['stat'] > cutoff_stat]
        return deg_results

    filtered_deg_results = filter_deg_results(deg_stats_results)
    st.write("Filtered DEG Results", filtered_deg_results)

    # Display DEG Genes
    st.write("DEG Genes", filtered_deg_results.index.to_list())