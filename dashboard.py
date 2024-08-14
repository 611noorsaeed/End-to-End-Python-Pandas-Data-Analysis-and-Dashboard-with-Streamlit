import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Custome functions===========================================================================
def about_df(df):
    # Sample view
    df_sample = df.sample(10)

    # Get size
    size = df.shape[0]

    # Get info (this will print info and not return it, so we capture it separately)
    buffer = io.StringIO()
    df.info(buf=buffer)
    info = buffer.getvalue()

    # Get column names and types
    columns = df.dtypes

    # Get missing values
    missing_values = df.isnull().sum()

    # Get statistics for numerical columns
    stats = df.describe(include='all')  # Include 'all' to get stats for non-numerical columns as well

    return df_sample, size, info, columns, missing_values, stats


# customer statistic funtion=========================================================================
def customer_statistics(df):
    # Calculate the relevant statistics
    average_age = df.iloc[:, 1].mean()
    average_tenure = df.iloc[:, 3].mean()
    total_spend = df.iloc[:, 9].sum()
    average_support_calls = df.iloc[:, 5].mean()
    churn_rate = df.iloc[:, 11].mean() * 100
    payment_delay_std_dev = df.iloc[:, 6].std()

    # Create a dictionary to store the statistics
    statistics = {
        'Average Age': average_age,
        'Average Tenure': average_tenure,
        'Total Spend': total_spend,
        'Average Support Calls': average_support_calls,
        'Churn Rate (%)': churn_rate,
        'Payment Delay Std Dev': payment_delay_std_dev
    }

    return statistics


# future insights====================================================================
def future_insights(df):
    # 1. Projected Total Spend for next year assuming similar behavior
    average_monthly_spend = df.iloc[:, 9].mean()
    projected_total_spend_next_year = average_monthly_spend * 12 * len(df)

    # 2. Churn Prediction: If churn rate remains the same, expected churn next year
    churn_rate = df.iloc[:, 11].mean()
    projected_churn_next_year = churn_rate * len(df)

    # 3. Increase in Support Calls: Predict next year's average support calls if trend continues
    average_support_calls = df.iloc[:, 5].mean()
    projected_support_calls_increase = average_support_calls * 1.1  # Assuming a 10% increase

    # 4. Payment Delay Trend: If delay continues to increase, predict future average delay
    average_payment_delay = df.iloc[:, 6].mean()
    projected_payment_delay_increase = average_payment_delay * 1.05  # Assuming a 5% increase

    # 5. Subscription Upgrades: Estimate the number of customers who might upgrade their subscription
    standard_and_basic_users = df[(df.iloc[:, 7] == 'Standard') | (df.iloc[:, 7] == 'Basic')]
    projected_upgrades = len(standard_and_basic_users) * 0.15  # Assuming 15% might upgrade

    # 6. Tenure Growth: Estimate how much tenure might increase if retention strategies are improved
    average_tenure = df.iloc[:, 3].mean()
    projected_tenure_growth = average_tenure * 1.2  # Assuming a 20% improvement in retention

    # Create a dictionary to store the future insights
    insights = {
        'Projected Total Spend Next Year': projected_total_spend_next_year,
        'Projected Churn Next Year': projected_churn_next_year,
        'Projected Support Calls Increase': projected_support_calls_increase,
        'Projected Payment Delay Increase': projected_payment_delay_increase,
        'Projected Subscription Upgrades': projected_upgrades,
        'Projected Tenure Growth': projected_tenure_growth
    }

    return insights



# dashboard functions (graphs)=========================================================================
def age_distribution_graph(df):
    fig, ax = plt.subplots()
    df['Age'].plot(kind='hist', bins=10, color='skyblue', edgecolor='black', ax=ax)
    ax.set_title('Distribution of Age')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    return fig

# Average Total Spend by Subscription Type
def avg_total_spend_subscription_type(df):
    fig, ax = plt.subplots()
    df.groupby('Subscription Type')['Total Spend'].mean().plot(kind='bar', color='lightgreen', ax=ax)
    ax.set_title('Average Total Spend by Subscription Type')
    ax.set_xlabel('Subscription Type')
    ax.set_ylabel('Average Total Spend')
    return fig

# Gender Distribution
def gender_distribution(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df['Gender'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    ax.set_title('Gender Distribution')
    ax.set_ylabel('')
    return fig

# Total Spend Distribution by Contract Length
def total_spend_distribution_by_contract_length(df):
    fig, ax = plt.subplots(figsize=(10, 6))
    df.groupby('Contract Length')['Total Spend'].sum().plot(kind='pie', autopct='%1.1f%%', colors=['#ff9999', '#66b3ff', '#99ff99'], ax=ax)
    ax.set_title('Total Spend Distribution by Contract Length')
    ax.set_ylabel('')
    return fig

# Churn Rate by Gender
def churn_rate_by_gender(df):
    fig, ax = plt.subplots()
    churn_rate_by_gender = df.groupby('Gender')['Churn'].mean() * 100
    churn_rate_by_gender.plot(kind='bar', color='coral', ax=ax)
    ax.set_title('Churn Rate by Gender')
    ax.set_xlabel('Gender')
    ax.set_ylabel('Churn Rate (%)')
    return fig

# Age Distribution by Gender
def age_distribution_by_gender(df):
    fig, ax = plt.subplots()
    df[df['Gender'] == 'Male']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='blue', label='Male', ax=ax)
    df[df['Gender'] == 'Female']['Age'].plot(kind='hist', bins=10, alpha=0.5, color='red', label='Female', ax=ax)
    ax.set_title('Age Distribution by Gender')
    ax.set_xlabel('Age')
    ax.set_ylabel('Frequency')
    ax.legend()
    return fig

# python main===================================
if __name__=="__main__":

    # Defaul message
    st.title("Customer Churn Dashboard")
    st.subheader("Data Analysis and Customer Insights")
    st.write("----------------------------------------------------------------------------------------")
    # sidebar==========
    # read data

    st.sidebar.title("Customers Analysis")
    uploaded_file = st.sidebar.file_uploader("choose a csv file", type='csv')

    df = pd.DataFrame()
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)

    # about dataset
    if st.sidebar.button("About Dataset"):
        st.subheader("About Dataset")
        # Get DataFrame information
        df_sample, size, info, columns, missing_values, stats = about_df(df)

        # Display results
        st.subheader('DataFrame Sample:')
        st.write(df_sample)

        st.subheader('DataFrame Size:')
        st.write(size)

        st.subheader('DataFrame Info:')
        st.text(info)

        st.subheader('Column Names and Types:')
        st.write(columns)

        st.subheader('Missing Values:')
        st.write(missing_values)

        st.subheader('Statistics:')
        st.write(stats)


    # customers statistics===============================
    if st.sidebar.button("Customer Statistics"):
        st.subheader('Customer Statistics:')
        # Get and display customer statistics
        customer_stats = customer_statistics(df)
        for key, value in customer_stats.items():
            st.write(f'{key}: {round(value, 2)}')


    # future insights ==================================
    if st.sidebar.button("Future Insights"):
        st.subheader("Future Insights")
        # Get the future insights
        future_stats = future_insights(df)
        # Print the future insights
        for key, value in future_stats.items():
            st.write(f'{key}: {round(value,2)}')


    # dashboard here====================================
    if st.sidebar.button("Dashboard"):
        st.subheader("Customer Dashboard")
        col1,col2 = st.columns(2)
        with col1:
            st.subheader("Age Distribution")
            fig = age_distribution_graph(df)
            st.pyplot(fig)
        with col2:
            st.subheader("Avg Spend Sub Type")
            fig = avg_total_spend_subscription_type(df)
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Gender Distribution")
            fig = gender_distribution(df)
            st.pyplot(fig)
        with col2:
            st.subheader("T/Spend Contact Length")
            fig = total_spend_distribution_by_contract_length(df)
            st.pyplot(fig)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Churn Rate By Gender")
            fig = churn_rate_by_gender(df)
            st.pyplot(fig)
        with col2:
            st.subheader("Age Dist By Gender")
            fig = age_distribution_by_gender(df)
            st.pyplot(fig)

