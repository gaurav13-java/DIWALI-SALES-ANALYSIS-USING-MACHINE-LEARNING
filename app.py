import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import iplot
import Backend as bd

# import csv file
df = pd.read_csv('Diwali Sales Data.csv', encoding= 'unicode_escape')
df.drop(columns=['Status','unnamed1','Age Group'], inplace=True)
df.dropna(inplace=True)
df['State'] = df['State'].str.replace('Andhra\xa0Pradesh', 'Andhra Pradesh')
df['Product_Category'] = df['Product_Category'].str.split(' & ').str[0]

# st.title("Diwali Sale DashBoard")
st.sidebar.title("Diwali Sale DashBoard")

# Lists
states =list(set(df['State'].unique()))
Occupation = list(set(df['Occupation'].unique()))
product_cat = list(set(df['Product_Category'].unique()))
zones = list(set(df['Zone'].unique()))

select = ["","Zone-Wise Analysis","State Wise Analysis", "OverALL Analysis"]
selectAna = st.sidebar.selectbox('Select Analysis',select)
# SelectOcc= st.sidebar.selectbox('Select Occupation',Occupation)
# SelectCat = st.sidebar.selectbox('Select Product Category',product_cat)
# SelectZone = st.sidebar.selectbox('Select Zone',zones)


if selectAna == "Zone-Wise Analysis":
    bd.zone_analysis()
elif selectAna =="OverALL Analysis":
    bd.Overall_Analysis()
elif selectAna =="State Wise Analysis":
    bd.State_Analysis()
