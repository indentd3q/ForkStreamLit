import streamlit as st
import pandas as pd
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

# Seperates Phenotypes by Race
def seperateByRace(file, race):
    """ 
        Searches the phenotype dataframe for the race.demographic column 
        and returns a new dataframe with only the rows that contains the race.
    """
    return file[file["race.demographic"].str.contains(race, case=False, na=False)]

# Matches Sample ID from phenotypes to counts
def matchingDNA(race, phenotypeDATA, countsDATA):
    """
        Matches the race phenotype data to the counts data 
        and returns a racial-dataframe with the matching data.
    """
    colA1 = phenotypeDATA.iloc[:, 0]

    newFile = countsDATA[['Ensembl_ID'] + [col for col in colA1 if col in countsDATA.columns[1:]]]    
    return pd.DataFrame(newFile)

# App Title
st.title("Differential Gene Expression Analysis with PyDESeq2")

# Upload phenotype data
st.sidebar.header("Input Files")
phenotypeFile = st.sidebar.file_uploader("Upload Phenotype Data (CSV)", type=["csv"])
countsFile = st.sidebar.file_uploader("Upload Counts Data (CSV)", type=["csv"])

if phenotypeFile and countsFile:
    phenotype = pd.read_csv(phenotypeFile)
    counts = pd.read_csv(countsFile)

    # Configurable Columns
    st.sidebar.header("Column Selections")
    phenotype_race_col = st.sidebar.selectbox(
        "Select Race Column in Phenotype Data", phenotype.columns
    )
    phenotype_sample_col = st.sidebar.selectbox(
        "Select Sample ID Column in Phenotype Data", phenotype.columns
    )
    counts_sample_col = st.sidebar.selectbox(
        "Select Sample ID Column in Counts Data", counts.columns
    )

    # Process by Race
    phenotype_unique_races = phenotype[phenotype_race_col].unique()
    selected_race = st.sidebar.selectbox(
        "Select Race to Analyze", phenotype_unique_races
    )

    phenotype_race_dataframes = {
        race: seperateByRace(phenotype, race) for race in phenotype_unique_races
    }
    counts_race_dataframes = {
        race: matchingDNA(race, phenotype, counts) for race in phenotype_unique_races
    }

    # Preprocess DEG
    st.sidebar.header("Preprocessing Options")
    index_col = st.sidebar.selectbox(
        "Select Index Column for Counts Data", counts.columns
    )

    def preprocess_deg(counts_data, index_col):
        counts_data = counts_data.set_index(index_col)
        counts_data = counts_data.fillna(0)
        counts_data = counts_data.round().astype(int)
        counts_data = counts_data[counts_data.sum(axis=1) > 0]
        counts_data = counts_data.T
        return counts_data

    preprocessed_counts_data = preprocess_deg(
        counts_race_dataframes[selected_race], index_col
    )

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
    st.sidebar.header("DEG Analysis Options")
    contrast_choice = st.sidebar.radio(
        "Select Contrast for Analysis", ["cancer", "normal"]
    )

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
    st.sidebar.header("DEG Filtering Options")
    cutoff_padj = st.sidebar.number_input("Cutoff for padj", value=0.05)
    cutoff_log2FoldChange = st.sidebar.number_input("Cutoff for log2FoldChange", value=0.5)
    cutoff_baseMean = st.sidebar.number_input("Cutoff for baseMean", value=10)
    cutoff_pvalue = st.sidebar.number_input("Cutoff for pvalue", value=0.05)
    cutoff_lfcSE = st.sidebar.number_input("Cutoff for lfcSE", value=0.1)
    cutoff_stat = st.sidebar.number_input("Cutoff for stat", value=0.1)

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
