import os
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Set page configuration - must be the first command
st.set_page_config(
    page_title="Financial Data Analysis with Predictions",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📊 Financial Data Analysis with Future Predictions")
st.write("Welcome to the financial data analysis app. Upload your CSV file to explore your financial data through visualizations, statistics, and predictions using machine learning.")

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

    # Plotting section with animated and interactive visualizations
    st.subheader(f"Visualizations for {region}")
    
    # Area Chart for Profit over Time
    st.markdown("### Profit Over Time")
    area_chart = px.area(filtered_df, x="Date", y="Profit", title='Profit Over Time', 
                          labels={'Date': 'Date', 'Profit': 'Profit'},
                          template='plotly_dark')
    st.plotly_chart(area_chart, use_container_width=True)

    # Bar Chart for Transaction Volume
    st.markdown("### Transaction Volume Over Time")
    bar_chart = px.bar(filtered_df, x="Date", y="Transaction_Volume", title='Transaction Volume Over Time',
                        labels={'Date': 'Date', 'Transaction_Volume': 'Transaction Volume'},
                        template='plotly_dark')
    st.plotly_chart(bar_chart, use_container_width=True)

    # Pie Chart for Distribution of Profit by Region
    st.markdown("### Profit Distribution by Region")
    profit_distribution = df.groupby("Region")["Profit"].sum().reset_index()
    pie_chart = px.pie(profit_distribution, names='Region', values='Profit', 
                        title='Profit Distribution by Region',
                        template='plotly_dark')
    st.plotly_chart(pie_chart, use_container_width=True)

    # Scatter plot for Transaction Volume vs Profit
    st.markdown("### Scatter Plot: Transaction Volume vs Profit")
    scatter_plot = px.scatter(filtered_df, x="Transaction_Volume", y="Profit", 
                               color="Region", title="Transaction Volume vs Profit",
                               trendline="ols",
                               labels={'Transaction_Volume': 'Transaction Volume', 'Profit': 'Profit'},
                               template='plotly_dark')
    st.plotly_chart(scatter_plot, use_container_width=True)

   # Machine Learning Model for Future Predictions
    #st.subheader("Machine Learning: Predicting Future Profits")

    # Check if required columns exist for ML
    #  if "Profit" in df.columns and "Transaction_Volume" in df.columns:
        # Prepare the data for training the ML model
       # X = df[["Transaction_Volume"]]
        #y = df["Profit"]
        
        # Split the data into training and testing sets
       # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train a linear regression model
        # model = LinearRegression()
        # model.fit(X_train, y_train)
        
        # Predict future profits
        # y_pred = model.predict(X_test)
        
        # Display metrics
        # st.write(f"**R-squared score:** {r2_score(y_test, y_pred):.2f}")
        # st.write(f"**Mean Squared Error:** {mean_squared_error(y_test, y_pred):.2f}")
        
        # Plot predictions vs actual values
        # prediction_plot = px.scatter(x=y_test, y=y_pred, labels={"x": "Actual Profit", "y": "Predicted Profit"},
                           #          title="Actual vs Predicted Profit", template='plotly_dark')
        #st.plotly_chart(prediction_plot, use_container_width=True)

    # else:
        # st.warning("Required columns (Profit, Transaction Volume) not found in the dataset for predictions.")

    # Correlation Heatmap
    st.subheader("Correlation Heatmap")
    st.write("Heatmap of the correlation between numeric variables:")

    # Filter out non-numeric columns
    numeric_df = df.select_dtypes(include=['float64', 'int64'])
    correlation = numeric_df.corr()

    # Plot heatmap using Plotly
    fig = ff.create_annotated_heatmap(
        z=correlation.values,
        x=list(correlation.columns),
        y=list(correlation.index),
        annotation_text=correlation.round(2).values,
        colorscale='Viridis',
    )
    st.plotly_chart(fig, use_container_width=True)

    # Additional insights
    st.subheader("Insights")
    st.write(f"**Total Profit for {region}:** ${filtered_df['Profit'].sum():,.2f}")
    st.write(f"**Average Transaction Volume for {region}:** {filtered_df['Transaction_Volume'].mean():,.2f}")

else:
    st.sidebar.info("Please upload a CSV file to get started.")
    st.write("Awaiting file upload...")

# Footer
st.markdown("""<hr>
    <small>Developed by Suhas and KGI in collaboration. Powered by Streamlit.</small>
    """, unsafe_allow_html=True)
