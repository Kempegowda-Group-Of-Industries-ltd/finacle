import os
import streamlit as st
import pandas as pd

# Set page configuration - must be the first command
st.set_page_config(
    page_title="Infosys Finacle - Financial Data Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📊 Infosys Finacle - Financial Data Analysis")
st.write("Welcome to the financial data analysis app. Upload your CSV file to explore your financial data through visualizations and statistics.")

# Sidebar header
st.sidebar.header("File Upload Section")

# Create an 'uploads' directory if it doesn't exist
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# File upload logic
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Save the uploaded file to the 'uploads' directory
    save_path = os.path.join("uploads", uploaded_file.name)
    
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.sidebar.success(f"File successfully saved at: {save_path}")

    # Read the uploaded CSV file
    df = pd.read_csv(save_path)

    # Displaying the data
    st.subheader("Uploaded Data Preview")
    st.write("Here is a preview of the uploaded financial data:")
    st.dataframe(df)

    # Displaying basic statistics
    st.subheader("Basic Data Statistics")
    st.write("Some basic statistics of your data:")
    st.write(df.describe())

    # Sidebar options for analysis
    st.sidebar.subheader("Analysis Options")
    region = st.sidebar.selectbox("Select Region to Filter", df["Region"].unique())

    # Filter data by selected region
    st.subheader(f"Data for {region} region")
    filtered_df = df[df["Region"] == region]
    st.dataframe(filtered_df)

    # Plotting section
    st.subheader(f"Transaction Volume and Profit for {region}")
    
    col1, col2 = st.columns(2)

    with col1:
        st.bar_chart(filtered_df[["Date", "Transaction_Volume"]].set_index("Date"))

    with col2:
        st.line_chart(filtered_df[["Date", "Profit"]].set_index("Date"))

    # Additional insights
    st.subheader("Insights")
    st.write(f"Total Profit for {region}: {filtered_df['Profit'].sum()}")
    st.write(f"Average Transaction Volume for {region}: {filtered_df['Transaction_Volume'].mean()}")

else:
    st.sidebar.info("Please upload a CSV file to get started.")
    st.write("Awaiting file upload...")

# Footer
st.markdown("""
    <hr>
    <small>Developed by Suhas and KGI in collaboration. Powered by Streamlit.</small>
    """, unsafe_allow_html=True)
