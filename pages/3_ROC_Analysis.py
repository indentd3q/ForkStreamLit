import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from sklearn.metrics import roc_curve, auc

# Page Configuration
st.set_page_config(layout="wide", page_title="Gene ROC Analysis")

# Title and Description
st.title("🧬 Gene ROC Analysis")
st.markdown("*Analyze and Visualize Gene Performance Using ROC Curves*")

# Create columns for file uploaders
col1, col2 = st.columns(2)

with col1:
    upregulated_file = st.file_uploader("📊 Upload Upregulated Dataset", type=['csv', 'xlsx'])

with col2:
    combined_dataset_file = st.file_uploader("📁 Upload Combined Dataset", type=['csv', 'xlsx'])

# ROC Curve Configuration
st.header("Analysis Parameters")
auc_threshold = st.slider("AUC Threshold", min_value=0.5, max_value=1.0, value=0.9, step=0.05)

if upregulated_file and combined_dataset_file:
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Sample Info", "📈 ROC Curves", "🧬 High AUC Genes", "💾 Export"])

    with tab1:
        # Load and process data
        data = pd.read_csv(upregulated_file)
        geneID = data.iloc[:,0]
        features_df = data.iloc[:,1:]
        data = data.set_index("Ensembl_ID")
        data = data.T
        data['label'] = ['cancer' if '-01' in sample else 'normal' for sample in data.index]
        
        # Sample count information
        st.header("Sample Distribution")
        class_counts = data['label'].value_counts()
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.metric("Cancer Samples", class_counts['cancer'])
        with col_b:
            st.metric("Normal Samples", class_counts['normal'])
        with col_c:
            st.metric("Total Samples", len(data))

    with tab2:
        # Prepare data for ROC
        X = np.asarray(features_df.round().astype(int).T)
        y = np.asarray(data['label'])
        
        y_bin = label_binarize(y, classes=np.unique(y))
        
        fpr = dict()
        tpr = dict()
        roc_auc = dict()

        for i in range(X.shape[1]):
            fpr[i], tpr[i], _ = roc_curve(y_bin.ravel(), X[:, i].ravel())
            roc_auc[i] = auc(fpr[i], tpr[i])
        
        # Plot ROC Curve
        plt.figure(figsize=(12, 8))
        
        high_auc_genes = []
        for i in range(len(geneID)):
            if roc_auc[i] > auc_threshold:
                plt.plot(fpr[i], tpr[i], lw=2, label=f'Gene {geneID[i]} (AUC = {roc_auc[i]:.4f})')
                high_auc_genes.append(geneID[i])
        
        plt.plot([0, 1], [0, 1], 'k--', lw=2)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve for Genes with AUC > {auc_threshold}')
        plt.legend(loc="lower right", bbox_to_anchor=(1.05, 0))
        plt.tight_layout()
        st.pyplot(plt)

    with tab3:
        # Display high AUC genes
        st.header("High AUC Genes")
        
        # ROC DataFrame
        roc_df = pd.DataFrame({
            'Ensembl_ID': geneID,
            'ROC_AUC': [roc_auc[i] for i in range(len(geneID))]
        })
        
        # Filter and sort high AUC genes
        high_auc_df = roc_df[roc_df['ROC_AUC'] > auc_threshold].sort_values('ROC_AUC', ascending=False)
        
        st.dataframe(high_auc_df, use_container_width=True)
        st.write(f"**Total High AUC Genes:** {len(high_auc_df)}")

    with tab4:
        # Filtered Dataset Export
        st.header("Filtered Dataset Export")
        
        # Read combined dataset and filter
        combined_dataset = pd.read_csv(combined_dataset_file)
        regulated_genes = combined_dataset[combined_dataset['Ensembl_ID'].isin(high_auc_genes)]
        
        # Display and download options
        st.dataframe(regulated_genes, use_container_width=True)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.download_button(
                label="💾 Download CSV",
                data=regulated_genes.to_csv(index=False),
                file_name="ROC_Results.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col_b:
            st.download_button(
                label="📄 Download Excel",
                data=regulated_genes.to_excel(index=False),
                file_name="ROC_Results.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

else:
    # Guidance for user
    st.info("""
    ### 🧬 Gene ROC Analysis Tool
    1. Upload an Upregulated Dataset
    2. Upload a Combined Dataset
    3. Adjust AUC Threshold as needed
    4. Analyze gene performance
    """)