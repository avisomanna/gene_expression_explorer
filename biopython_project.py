import streamlit as st
import pandas as pd
import numpy as np

st.title("Gene Expression Explorer")


uploaded_file = st.file_uploader("Upload your own CSV if you want", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file, index_col=0)
else:
    data = pd.read_csv("sample_expression_data.csv", index_col=0)

st.write("Number of genes:", len(data))
st.write("Number of samples:", len(data.columns))
st.dataframe(data.head(10))


st.header("Summary statistics")
st.write(data.describe())


st.header("Filter low expression genes")
min_expr = st.slider("Minimum average expression", 0, 100, 10)
gene_means = data.mean(axis=1)
filtered = data[gene_means >= min_expr]
st.write("Genes remaining:", len(filtered))

if len(filtered) == 0:
    st.warning("No genes left, try a lower minimum.")
    st.stop()


st.header("Top expressed genes")
top_n = st.slider("How many genes?", 3, 20, 10)
top_genes = filtered.mean(axis=1).sort_values(ascending=False).head(top_n)
st.bar_chart(top_genes)


st.header("Look up a gene")
gene = st.selectbox("Pick a gene", filtered.index)
st.bar_chart(filtered.loc[gene])


st.header("Compare two groups")
samples = list(data.columns)
half = len(samples) // 2
group1 = st.multiselect("Group 1 : ", samples, default=samples[:half])
group2 = st.multiselect("Group 2 : ", samples, default=samples[half:])

if len(group1) > 0 and len(group2) > 0:
    mean1 = filtered[group1].mean(axis=1)
    mean2 = filtered[group2].mean(axis=1)
    # +1 so we never take log of zero
    log2_fc = np.log2((mean2 + 1) / (mean1 + 1))

    results = pd.DataFrame({
        "mean_group1": mean1,
        "mean_group2": mean2,
        "log2_fold_change": log2_fc,
    })
    results = results.sort_values("log2_fold_change", ascending=False)

    st.write("Genes higher in group 2:")
    st.dataframe(results.head(10))
    st.write("Genes lower in group 2:")
    st.dataframe(results.tail(10))
