import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Configure the page
st.set_page_config(
    page_title="Data Exploration of Invistico Airline Dataset",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit style for a cleaner look
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Load data function
@st.cache_data
def load_data():
    df = pd.read_csv('Invistico_Airline.csv')
    return df

# Main Content

# Sidebar Navigation
st.sidebar.title("Navigation")
options = st.sidebar.radio("Go to", ['Introduction', 'Data Exploration', 'Conclusions and Recommendations'])

if options == 'Introduction':
    # Group Information
    st.markdown("""
    <h1 style='text-align: center;'>Group Activity: Report on Data Exploration Techniques</h1>

    ## Group Information

    **Group Name:** Group Nime

    **Group Leader:** Mark Kenneth S. Badilla

    **Group Members:**
    - James Alein Ocampo
    - Alestair Cyril Coyoca
    - Rob S. Borinaga
    - Carmelyn Nime T. Gerali
    """, unsafe_allow_html=True)

    # Introduction
    st.markdown("""
    ## Introduction

    Welcome to our data exploration app! In this activity, our group, **Group Nime**, dives into the **Invistico Airline Dataset** sourced from Kaggle. This dataset is rich with customer satisfaction information, featuring both numerical and categorical variables related to airline services.

    ### Objective

    Our primary goal is to perform data exploration using descriptive statistics to understand the central tendencies, spread, and relationships within the dataset. By the end of this exploration, we aim to present valuable insights and identify potential areas for further analysis.

    ### Tools Used

    - **pandas** for data manipulation
    - **numpy** for numerical operations
    - **seaborn** and **matplotlib** for data visualization
    - **Streamlit** for building this interactive web application

    **Let's embark on this data journey together! Use the navigation bar on the left to explore different sections of the analysis.**
    """, unsafe_allow_html=True)

elif options == 'Data Exploration':
    # Load the Dataset
    st.header("Load the Dataset")
    df = load_data()
    st.success("Dataset loaded successfully! Let's take a peek at what we're working with.")

    # Initial Data Exploration
    st.header("Initial Data Exploration")

    st.subheader("Dataset Preview")
    st.write(df.head())

    st.markdown("""
    *Here we can see a snapshot of the dataset, which gives us an initial understanding of the data structure and variables involved.*
    """)

    with st.expander("View DataFrame Info"):
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        st.text(s)
        st.markdown("""
        *This summary provides information about the data types and non-null counts of each column, helping us identify any immediate issues.*
        """)

    st.subheader("Missing Values in Each Column")
    st.write(df.isnull().sum())

    st.markdown("""
    *It's essential to check for missing values early on. Here, we see that the 'Arrival Delay in Minutes' column has some missing values that we'll need to address.*
    """)

    st.subheader("Statistical Summary")
    st.write(df.describe())

    st.markdown("""
    *The statistical summary offers a quick glance at the central tendencies and dispersion of our numerical variables.*
    """)

    # Data Cleaning
    st.header("Data Cleaning")

    st.markdown("""
    **Data cleaning is a crucial step to ensure the accuracy and reliability of our analysis. Let's clean the dataset based on our initial findings.**
    """)

    # Handling Missing Values
    st.subheader("Handling Missing Values")

    st.markdown("""
    We observed missing values in the **'Arrival Delay in Minutes'** column. Since they represent a small fraction of the data, we'll remove these rows to maintain data integrity.
    """)

    st.write("Number of missing values before cleaning:")
    st.write(df.isnull().sum())

    # Drop rows with missing 'Arrival Delay in Minutes'
    df = df.dropna(subset=['Arrival Delay in Minutes'])

    st.write("Number of missing values after cleaning:")
    st.write(df.isnull().sum())

    st.markdown("""
    *Great! The missing values have been handled, ensuring our dataset is complete for the analysis.*
    """)

    # Data Type Conversion
    st.subheader("Data Type Conversion")

    st.markdown("""
    Converting data types can improve performance and make analysis more straightforward. We'll convert categorical columns to the **'category'** data type and ensure numerical columns are appropriately formatted.
    """)

    # Convert categorical columns to 'category' data type
    categorical_cols = ['satisfaction', 'Gender', 'Customer Type', 'Type of Travel', 'Class']
    for col in categorical_cols:
        df[col] = df[col].astype('category')

    # Convert 'Arrival Delay in Minutes' to integer type
    df['Arrival Delay in Minutes'] = df['Arrival Delay in Minutes'].astype(int)

    st.write("Data types after conversion:")
    st.write(df.dtypes)

    st.markdown("""
    *Data type conversion complete! This will help optimize memory usage and improve computation speed.*
    """)

    # Check for Duplicates
    st.subheader("Check for Duplicates")

    st.markdown("""
    Duplicate entries can skew our analysis. Let's check if there are any and remove them if necessary.
    """)

    duplicates = df.duplicated().sum()
    st.write(f"Number of duplicate rows: **{duplicates}**")

    # Remove duplicate rows if any
    df = df.drop_duplicates()

    duplicates_after = df.duplicated().sum()
    st.write(f"Number of duplicate rows after removal: **{duplicates_after}**")

    st.markdown("""
    *No more duplicates! Our dataset is now clean and ready for exploration.*
    """)

    # Outlier Detection and Handling
    st.subheader("Outlier Detection and Handling")

    st.markdown("""
    Outliers can significantly impact our analysis. We'll cap extreme values in **'Departure Delay in Minutes'** and **'Arrival Delay in Minutes'** at the 99th percentile to mitigate their effect.
    """)

    # Cap outliers at the 99th percentile
    departure_delay_cap = df['Departure Delay in Minutes'].quantile(0.99)
    arrival_delay_cap = df['Arrival Delay in Minutes'].quantile(0.99)

    df['Departure Delay in Minutes'] = np.where(
        df['Departure Delay in Minutes'] > departure_delay_cap,
        departure_delay_cap,
        df['Departure Delay in Minutes']
    )

    df['Arrival Delay in Minutes'] = np.where(
        df['Arrival Delay in Minutes'] > arrival_delay_cap,
        arrival_delay_cap,
        df['Arrival Delay in Minutes']
    )

    st.write("Outliers capped at the 99th percentile.")

    st.markdown("""
    *By capping outliers, we prevent them from distorting our statistical analyses and visualizations.*
    """)

    # Data Exploration
    st.header("Data Exploration")

    st.markdown("""
    **Now comes the exciting part! Let's dive into the data to uncover patterns and insights through visualizations and statistical summaries.**
    """)

    # Define numerical columns
    numerical_cols = [
        'Age', 'Flight Distance', 'Departure Delay in Minutes', 'Arrival Delay in Minutes'
    ]

    for col in numerical_cols:
        col_var = col.replace(' ', '_')

        st.subheader(f"Analysis of {col}")

        st.markdown(f"""
        Let's explore the **{col}** variable to understand its distribution and key statistics.
        """)

        # Histogram
        fig, ax = plt.subplots(figsize=(10, 4))
        sns.histplot(df[col], bins=30, kde=True, color='skyblue', ax=ax)
        ax.set_title(f'Histogram of {col}')
        ax.set_xlabel(col)
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

        st.markdown(f"""
        *The histogram provides a visual representation of the distribution of **{col}**.*
        """)

        # Display statistics in columns
        mean_value = df[col].mean()
        median_value = df[col].median()
        std_value = df[col].std()
        min_value = df[col].min()
        max_value = df[col].max()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Mean", f"{mean_value:.2f}")
        col2.metric("Median", f"{median_value:.2f}")
        col3.metric("Std Dev", f"{std_value:.2f}")
        col4.metric("Min", f"{min_value:.2f}")
        col5.metric("Max", f"{max_value:.2f}")

        st.markdown(f"""
        *Here are some key statistics for **{col}** to complement the visual insights.*
        """)

        # Provide insights
        if col == 'Age':
            insight_md = """### Insights from Histogram of Age

- The **Age** distribution is approximately symmetrical with a slight right skew.
- The mean age is around **39 years**, with most passengers between **27 and 51 years old**.
- This indicates a diverse passenger age range, focusing on the working-age population.
- Minimal outliers suggest a consistent customer age demographic.
"""
        elif col == 'Flight Distance':
            insight_md = """### Insights from Histogram of Flight Distance

- The **Flight Distance** shows a bimodal distribution, hinting at two primary flight distance categories.
- Peaks at shorter and medium distances suggest operations in both regional and medium-haul flights.
- Mean flight distance is approximately **1981 km**.
- This information helps in tailoring services for different flight lengths.
"""
        elif col == 'Departure Delay in Minutes':
            insight_md = """### Insights from Histogram of Departure Delay in Minutes

- Majority of flights have **zero departure delay**, highlighting operational efficiency.
- A long tail indicates some flights experience significant delays (up to **180 minutes**).
- Mean delay is around **13 minutes**, but the median is **0**, emphasizing the effect of outliers.
- Reducing delays can boost customer satisfaction and lower operational costs.
"""
        elif col == 'Arrival Delay in Minutes':
            insight_md = """### Insights from Histogram of Arrival Delay in Minutes

- Most flights **arrive on time**, similar to departure punctuality.
- The long tail shows some flights have significant arrival delays.
- Strong correlation with departure delays suggests late departures often lead to late arrivals.
- Improving departure times can positively impact arrival punctuality.
"""
        st.markdown(insight_md)

        # Box Plot
        fig_box, ax_box = plt.subplots(figsize=(10, 2))
        sns.boxplot(x=df[col], color='lightgreen', ax=ax_box)
        ax_box.set_title(f'Box Plot of {col}')
        ax_box.set_xlabel(col)
        st.pyplot(fig_box)

        st.markdown(f"""
        *The box plot provides insights into the spread and outliers of **{col}**.*
        """)

        # Quartiles and IQR in columns
        Q1 = df[col].quantile(0.25)
        Q2 = df[col].quantile(0.5)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("25th Percentile (Q1)", f"{Q1:.2f}")
        col2.metric("Median (Q2)", f"{Q2:.2f}")
        col3.metric("75th Percentile (Q3)", f"{Q3:.2f}")
        col4.metric("Interquartile Range (IQR)", f"{IQR:.2f}")

        st.markdown(f"""
        *Understanding the quartiles helps in identifying the middle 50% of the data for **{col}**.*
        """)

        # Provide insights
        if col == 'Age':
            insight_md = """### Insights from Box Plot of Age

- Confirms a symmetrical distribution of **Age**.
- IQR spans from **27 to 51 years**, where 50% of passengers fall.
- Minimal outliers indicate a stable age demographic.
- Useful for targeted marketing strategies.
"""
        elif col == 'Flight Distance':
            insight_md = """### Insights from Box Plot of Flight Distance

- Wide IQR from **1359 km to 2543 km**.
- Presence of outliers up to **6951 km** indicates some long-haul flights.
- Helps in planning fleet utilization and fuel management.
"""
        elif col == 'Departure Delay in Minutes':
            insight_md = """### Insights from Box Plot of Departure Delay in Minutes

- Most flights have **no departure delay**.
- IQR from **0 to 12 minutes**, with many outliers up to **180 minutes**.
- Highlights the need to address factors causing significant delays.
"""
        elif col == 'Arrival Delay in Minutes':
            insight_md = """### Insights from Box Plot of Arrival Delay in Minutes

- Similar pattern to departure delays.
- IQR from **0 to 13 minutes**, with outliers up to **182 minutes**.
- Emphasizes the impact of departure delays on arrival times.
"""
        st.markdown(insight_md)

    # Correlation Matrix and Heatmap
    st.subheader("Correlation Matrix and Heatmap")

    st.markdown("""
    Let's examine how the numerical variables relate to each other using a correlation matrix and heatmap.
    """)

    # Compute correlation matrix
    corr_matrix = df[numerical_cols].corr()

    st.write("Correlation Matrix:")
    st.write(corr_matrix)

    # Plot heatmap
    fig_corr, ax_corr = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', ax=ax_corr)
    ax_corr.set_title('Correlation Heatmap of Numerical Variables')
    st.pyplot(fig_corr)

    # Insights from Correlation
    st.markdown("""
    ### Insights from Correlation Matrix and Heatmap

    - **Strong Positive Correlation between Departure and Arrival Delays**: Flights that depart late tend to arrive late.
    - **Negative Correlation between Age and Flight Distance**: Younger passengers often take longer flights, possibly due to travel preferences.
    - **Positive Correlation between Flight Distance and Delays**: Longer flights may experience more delays.
    - These insights can guide operational improvements and customer service strategies.
    """)

elif options == 'Conclusions and Recommendations':
    st.header("Conclusions and Recommendations")

    st.markdown("""
    **After a thorough exploration of the dataset, we've gathered key insights and formulated recommendations to enhance the airline's operations and customer satisfaction.**
    """)

    st.subheader("Key Insights")

    st.markdown("""
    - **Passenger Demographics**: A wide age range is served, with a significant portion between **27 and 51 years old**. Younger passengers tend to take longer flights.
    - **Flight Operations**: The airline operates short-haul, medium-haul, and some long-haul flights, as indicated by the bimodal flight distance distribution.
    - **Delays**: Most flights are on time, but significant delays occur and are highly correlated between departure and arrival times.
    """)

    st.subheader("Recommendations")

    st.markdown("""
    1. **Address Significant Delays**:
       - Investigate root causes such as operational inefficiencies or maintenance issues.
       - Implement predictive maintenance and optimize scheduling.
    2. **Enhance On-Time Performance**:
       - Improve ground operations for faster boarding and turnaround.
       - Proactively communicate with passengers about delays.
    3. **Customer Satisfaction Initiatives**:
       - Develop targeted marketing for different age groups, focusing on younger passengers for longer flights.
       - Offer personalized services and loyalty programs.
    4. **Optimize Flight Routes**:
       - Analyze route profitability to focus on high-demand flights.
       - Adjust flight frequencies based on demand patterns.

    **Conclusion**

    By implementing these recommendations, the airline can improve operational efficiency, enhance customer satisfaction, and strengthen its market position. Continuous data analysis will support ongoing improvements and adaptation to changing market dynamics.

    **Thank you for exploring the data with us!**
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed by **Group Nime**")
