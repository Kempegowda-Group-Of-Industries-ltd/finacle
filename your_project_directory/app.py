# app.py

import streamlit as st
import pandas as pd
import numpy as np
import os

# Title and description
st.title("Infosys Finacle Financial Dashboard")
st.write("Upload financial data files (CSV or Excel) to analyze them interactively.")

# File uploader
uploaded_file = st.file_uploader("Choose a financial data file", type=['csv', 'xlsx'])

# Save the uploaded file and process it
if uploaded_file is not None:
    # Save the uploaded file to the 'uploads' directory
    save_path = os.path.join("uploads", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.write(f"File saved at: {save_path}")
    
    # Load the file based on its extension
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(save_path)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(save_path, engine='openpyxl')
    
    # Display the data
    st.write("### Data Preview:")
    st.dataframe(df.head())

    # Show basic statistics
    st.write("### Basic Statistics:")
    st.write(df.describe())

    # Visualizing numerical data (e.g., transaction volume and profits)
    st.write("### Visualization of Financial Data:")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    if numeric_columns:
        column_to_plot = st.selectbox("Choose a column to visualize", numeric_columns)
        st.line_chart(df[column_to_plot])
    else:
        st.write("No numerical columns to visualize.")
else:
    st.write("Please upload a CSV or Excel file to continue.")
