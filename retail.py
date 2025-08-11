import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# --------- Page Config ---------
st.set_page_config(page_title="E-Commerce Sales Dashboard",
                   page_icon="🛒",
                   layout="wide")

# Heading
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50; font-size: 38px;'>
        📊 E-Commerce Sales Dashboard 
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <hr style='border: 1px solid #4CAF50; margin-top: -5px; margin-bottom: 20px;'>
    """,
    unsafe_allow_html=True
)


# Load Dataset
df = pd.read_csv(r"C:\Users\deepu\PycharmProjects\PythonProject2\Cleaned_Retail_data")

# Changing the currency type
def format_currency(num):
    if num >= 1_00_00_000:  # Cr
        return f"{num / 1_00_00_000:.2f} Cr"
    elif num >= 1_00_000:  # Lakhs
        return f"{num / 1_00_000:.2f} L"
    elif num >= 1_000:  # Thousands
        return f"{num / 1_000:.2f} K"
    else:
        return f"{num:.2f}"


# Reusable metrics function
def show_metrics(df):
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Unique Customers", df["CustomerID"].nunique())
    col2.metric("Total Quantity", df["Quantity"].sum())
    col3.metric("Total Invoices", df["InvoiceNo"].nunique())
    col4.metric("Total Revenue", f"${format_currency(df['Total Revenue'].sum())}")

# Reusable monthly trend function
def plot_monthly_trend(df, color, marker):
    monthly_sales = df.resample('ME', on='Date')['Total Revenue'].sum().reset_index()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly_sales['Date'], monthly_sales['Total Revenue'], marker=marker, color=color)
    ax.set_title("Monthly Revenue Trend", fontsize=11)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Revenue")
    st.pyplot(fig)


def product_wise(df):

    show_metrics(df)
    plot_monthly_trend(df,color = 'green', marker = '*')



    st.subheader("Top Countries by Revenue Spend for this Product")
    # Aggregate data
    top_country = (
        df.groupby('Country')
        .agg(Total_Spend=('Total Revenue', 'sum'),
             Total_Quantity=('Quantity', 'sum'))
        .sort_values('Total_Spend', ascending=False)
        .head(5)
        .reset_index()
    )

    # Bar chart for revenue
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(top_country['Country'], top_country['Total_Spend'], color='skyblue')
    ax.set_title("Top 5 Countries by Revenue")
    ax.set_xlabel("Country")
    ax.set_ylabel("Total Revenue")
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)

    # Show the data table below
    st.dataframe(top_country.style.format({
        'Total_Spend': '${:,.2f}',
        'Total_Quantity': '{:,}'
    }))


def country_wise(df):

    show_metrics(df)
    plot_monthly_trend(df, color = 'blue', marker = 'o')

    # Top 10 Products by Total Revenue
    top_products = (
        df.groupby('Description')['Total Revenue']
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    top_products.plot(kind='bar', ax=ax2, color='green')
    ax2.set_title("Top 10 Products by Total Revenue", fontsize=12)
    ax2.set_xlabel("Product")
    ax2.set_ylabel("Total Revenue")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)


    # Top Customers by Revenue
    st.subheader("Top Customers by Revenue")
    top_customers = (
        df.groupby('CustomerID')
        .agg(Total_Spend=('Total Revenue', 'sum'),
             Total_Quantity=('Quantity', 'sum'))
        .sort_values('Total_Spend', ascending=False)
        .head()
        .reset_index()
    )
    st.dataframe(top_customers)

    # Top products by Quantity Sold
    st.subheader("Top Products by Quantity Sold")
    top_products_qty = (
        df.groupby('Description')['Quantity']
        .sum()
        .sort_values(ascending=False)
        .head()
        .reset_index()
    )
    st.dataframe(top_products_qty)



# Sidebar Title
st.sidebar.title("Explore Sales Insights")


# Date range filter
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

col1, col2 = st.sidebar.columns(2)
start_date = col1.date_input(
    "Start Date",
    value=min_date,
    min_value=min_date,
    max_value=max_date
)
end_date = col2.date_input(
    "End Date",
    value=max_date,
    min_value=min_date,
    max_value=max_date
)

# Filter data based on selected range
filtered_df = df[
    (df["Date"].dt.date >= start_date) &
    (df["Date"].dt.date <= end_date)
]





# Dropdown to select type
analysis_type = st.sidebar.selectbox('Select One', ['Country Wise', 'Product Wise'])



if analysis_type == 'Country Wise':
    country = st.sidebar.selectbox("Select Country : ", df["Country"].unique())


    if st.sidebar.button('Find Country Wise'):
        st.subheader(f"Analysis for **{country}**")
        country_df = filtered_df[filtered_df["Country"] == country]
        country_wise(country_df)



else:
    product = st.sidebar.selectbox("Select Product : ", df["Description"].unique())

    if st.sidebar.button('Find Product Details'):
        st.subheader(f"Analysis for **{product}**")
        product_df = filtered_df[filtered_df["Description"] == product]
        product_wise(product_df)


