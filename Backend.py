from multiprocessing.managers import State

import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Load data
df = pd.read_csv('Diwali Sales Data.csv', encoding='unicode_escape')
ldf = pd.read_csv("Latitude and Longitude State wise centroids 2020.csv")

# Data cleaning
df.drop(columns=['Status', 'unnamed1', 'Age Group'], inplace=True)
df.dropna(inplace=True)
df['State'] = df['State'].str.replace('Andhra\xa0Pradesh', 'Andhra Pradesh')
df['Product_Category'] = df['Product_Category'].str.split(' & ').str[0]


# Lists
states = list(set(df['State'].unique()))
occupations = list(set(df['Occupation'].unique()))
product_cat = list(set(df['Product_Category'].unique()))
zones = list(set(df['Zone'].unique()))


def zone_analysis():
    st.title("Zone Analysis")

    # Zone selection
    zone = st.selectbox("Select the Zone", zones)
    zone_df = df[df['Zone'] == zone]

    st.subheader(f"Overview of {zone} Zone")
    total_sales = zone_df['Amount'].sum()
    total_orders = zone_df['Orders'].sum()
    avg_sales = zone_df['Amount'].mean()
    avg_orders = zone_df['Orders'].mean()

    st.write(f"**Total Sales:** ₹{total_sales:,.2f}")
    st.write(f"**Total Orders:** {total_orders}")
    st.write(f"**Average Sales per Transaction:** ₹{avg_sales:,.2f}")
    st.write(f"**Average Orders per Transaction:** {avg_orders:.2f}")

    # Gender and Marital Status Analysis
    st.subheader("Demographic Analysis")
    gender_sales = zone_df.groupby('Gender')['Amount'].sum().reset_index()
    marital_sales = zone_df.groupby('Marital_Status')['Amount'].sum().reset_index()

    col1, col2 = st.columns(2)
    with col1:
        fig_gender = px.pie(gender_sales, names='Gender', values='Amount', title='Sales by Gender')
        st.plotly_chart(fig_gender, use_container_width=True)

    with col2:
        fig_marital = px.pie(marital_sales, names='Marital_Status', values='Amount', title='Sales by Marital Status')
        st.plotly_chart(fig_marital, use_container_width=True)

    # Product Category Analysis
    st.subheader("Product Category Analysis")
    category_sales = zone_df.groupby('Product_Category')['Amount'].sum().reset_index()
    fig_category = px.bar(
        category_sales,
        x='Product_Category',
        y='Amount',
        title='Sales by Product Category',
        text_auto='.2s',
        color='Product_Category'
    )
    fig_category.update_layout(xaxis_title="Product Category", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_category, use_container_width=True)

    # Occupation Analysis
    st.subheader("Occupation Analysis")
    occupation_sales = zone_df.groupby('Occupation')['Amount'].sum().reset_index()
    fig_occupation = px.bar(
        occupation_sales,
        x='Occupation',
        y='Amount',
        title='Sales by Occupation',
        text_auto='.2s',
        color='Occupation'
    )
    fig_occupation.update_layout(xaxis_title="Occupation", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_occupation, use_container_width=True)

    # State-wise Analysis in Zone
    st.subheader("State-Wise Analysis in Zone")
    state_sales = zone_df.groupby('State')['Amount'].sum().reset_index()
    fig_state = px.bar(
        state_sales,
        x='State',
        y='Amount',
        title=f'Sales by State in {zone}',
        text_auto='.2s',
        color='State'
    )
    fig_state.update_layout(xaxis_title="State", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_state, use_container_width=True)

    # Interactive Map
    st.subheader("Zone States on Map")
    merged_df = pd.merge(ldf, zone_df, left_on='State', right_on='State', how='inner')
    map_data = merged_df.groupby('State')[["Longitude", "Latitude"]].first().reset_index()

    fig_map = px.scatter_mapbox(
        map_data,
        lat="Latitude",
        lon="Longitude",
        size_max=25,
        zoom=4,
        mapbox_style="carto-positron",
        title=f"Map of States in {zone} Zone"
    )
    st.plotly_chart(fig_map, use_container_width=True)




def Overall_Analysis():
    st.title("Overall Analysis")

    # Key Metrics
    total_sales = df['Amount'].sum()
    total_orders = df['Orders'].sum()
    avg_sales = df['Amount'].mean()
    avg_orders = df['Orders'].mean()
    total_customers = df['User_ID'].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="🛍️ **Total Sales**", value=f"₹{total_sales:,.2f}")
    with col2:
        st.metric(label="📦 **Total Orders**", value=f"{total_orders:,}")
    with col3:
        st.metric(label="👥 **Unique Customers**", value=f"{total_customers:,}")

    col4, col5 = st.columns(2)
    with col4:
        st.metric(label="📊 **Average Sales**", value=f"₹{avg_sales:,.2f}")
    with col5:
        st.metric(label="📈 **Average Orders**", value=f"{avg_orders:.2f}")

    # Sales Distribution by Zones
    st.subheader("Sales Distribution by Zone")
    zone_sales = df.groupby('Zone')['Amount'].sum().reset_index()
    fig_zone = px.bar(
        zone_sales,
        x='Zone',
        y='Amount',
        color='Zone',
        title="Sales by Zone",
        text_auto='.2s'
    )
    fig_zone.update_layout(xaxis_title="Zone", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_zone, use_container_width=True)

    # Gender Distribution
    st.subheader("Gender-Wise Sales Distribution")
    gender_sales = df.groupby('Gender')['Amount'].sum().reset_index()
    fig_gender = px.pie(
        gender_sales,
        names='Gender',
        values='Amount',
        title="Sales by Gender",
        hole=0.4
    )
    st.plotly_chart(fig_gender, use_container_width=True)

    # Occupation Analysis
    st.subheader("Occupation Analysis")
    occupation_sales = df.groupby('Occupation')['Amount'].sum().reset_index()
    fig_occupation = px.bar(
        occupation_sales,
        x='Occupation',
        y='Amount',
        title='Sales by Occupation',
        text_auto='.2s',
        color='Occupation'
    )
    fig_occupation.update_layout(xaxis_title="Occupation", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_occupation, use_container_width=True)

    # Product Category Analysis
    st.subheader("Product Category Analysis")
    product_sales = df.groupby('Product_Category')['Amount'].sum().reset_index()
    fig_product = px.bar(
        product_sales,
        x='Product_Category',
        y='Amount',
        color='Product_Category',
        title='Sales by Product Category',
        text_auto='.2s'
    )
    fig_product.update_layout(xaxis_title="Product Category", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_product, use_container_width=True)

    # Age Group Distribution
    st.subheader("Age Group Sales Distribution")
    age_sales = df.groupby('Age')['Amount'].sum().reset_index()
    fig_age = px.line(
        age_sales,
        x='Age',
        y='Amount',
        title='Sales by Age Group',
        markers=True
    )
    fig_age.update_layout(xaxis_title="Age Group", yaxis_title="Sales (₹)")
    st.plotly_chart(fig_age, use_container_width=True)


def State_Analysis():
    st.title("State Analysis")

    # Select State
    state = st.selectbox("Select the State", states)
    state_df = df[df['State'] == state]

    # State Overview
    st.subheader(f"Overview of {state}")
    total_sales = state_df['Amount'].sum()
    total_orders = state_df['Orders'].sum()
    unique_customers = state_df['User_ID'].nunique()
    avg_sales = state_df['Amount'].mean()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="🛍️ **Total Sales**", value=f"₹{total_sales:,.2f}")
    with col2:
        st.metric(label="📦 **Total Orders**", value=f"{total_orders:,}")
    with col3:
        st.metric(label="👥 **Unique Customers**", value=f"{unique_customers:,}")
    with col4:
        st.metric(label="📊 **Average Sales**", value=f"₹{avg_sales:,.2f}")

    # Select Product Category
    st.subheader("Product Category Analysis")
    st.write("There are lots of Product Categories in this dataset!")
    category = st.selectbox("Select a Product Category", product_cat)
    category_df = state_df[state_df['Product_Category'] == category]
    category_sales = category_df['Amount'].sum()
    category_orders = category_df['Orders'].sum()

    st.write(f"**Total Sales for {category}:** ₹{category_sales:,.2f}")
    st.write(f"**Total Orders for {category}:** {category_orders:,}")

    # Sales by Product Categories in the State
    product_sales = state_df.groupby('Product_Category')['Amount'].sum().reset_index()
    fig_product = px.bar(
        product_sales,
        x='Product_Category',
        y='Amount',
        color='Product_Category',
        title=f"Sales by Product Category in {state}",
        text_auto='.2s'
    )
    fig_product.update_layout(xaxis_title="Product Category", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_product, use_container_width=True)

    # Occupation Analysis
    st.subheader("Occupation Analysis")
    st.write("There are Types of Occupation in this dataset!")
    occupation_type = st.radio("Select Occupation Type", occupations)
    occupation_df = state_df[state_df['Occupation'] == occupation_type]
    occupation_sales = occupation_df['Amount'].sum()
    occupation_orders = occupation_df['Orders'].sum()

    st.write(f"**Total Sales for {occupation_type}:** ₹{occupation_sales:,.2f}")
    st.write(f"**Total Orders for {occupation_type}:** {occupation_orders:,}")

    # Occupation Sales Distribution
    occupation_sales_data = state_df.groupby('Occupation')['Amount'].sum().reset_index()
    fig_occupation = px.bar(
        occupation_sales_data,
        x='Occupation',
        y='Amount',
        color='Occupation',
        title=f"Sales by Occupation in {state}",
        text_auto='.2s'
    )
    fig_occupation.update_layout(xaxis_title="Occupation", yaxis_title="Sales (₹)", showlegend=False)
    st.plotly_chart(fig_occupation, use_container_width=True)

    # Gender Analysis
    st.subheader("Gender-Wise Sales Distribution")
    gender_sales = state_df.groupby('Gender')['Amount'].sum().reset_index()
    fig_gender = px.pie(
        gender_sales,
        names='Gender',
        values='Amount',
        title=f"Sales by Gender in {state}",
        hole=0.4
    )
    st.plotly_chart(fig_gender, use_container_width=True)

    # Age Analysis
    st.subheader("Sales Distribution by Age")
    age_sales = state_df.groupby('Age')['Amount'].sum().reset_index()
    fig_age = px.line(
        age_sales,
        x='Age',
        y='Amount',
        title=f"Sales by Age Group in {state}",
        markers=True
    )
    fig_age.update_layout(xaxis_title="Age Group", yaxis_title="Sales (₹)")
    st.plotly_chart(fig_age, use_container_width=True)

    # Summary of Selected State
    st.subheader(f"Summary for {state}")
    st.write("Here is the detailed data for the selected state:")
    st.dataframe(state_df)
