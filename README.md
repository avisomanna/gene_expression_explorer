# Gene Expression Explorer

A simple web app for exploring gene expression data, built with Python and Streamlit.

## What it does
- Loads a gene expression CSV (genes as rows, samples as columns) or uses the sample data
- Summary statistics
- Filters out low-expression genes
- Shows the top expressed genes and lets you look up a single gene
- Compares two groups of samples using log2 fold change

## Run it
```
pip install -r requirements.txt
streamlit run app.py
```

## Notes
The sample data file is synthetic (made up for demonstration).
The group comparison only uses fold change, with no statistical test yet.
