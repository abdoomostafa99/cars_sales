import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import random
import requests
from streamlit_lottie import st_lottie
import json

st.set_page_config(layout = 'wide' , page_title = 'Home Page')

cars = pd.read_csv('UserCarData.csv')
cars.drop(['mileage' , 'torque'] , axis=1 , inplace=True)
cars.columns = cars.columns.str.lower().str.strip()
cars.columns = cars.columns.str.replace(' ' , '_')
cars.sold= cars.sold.apply(lambda x: 'sold' if x == 'Y' else 'not sold')



st.title('Used Car Sales Analysis')
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
animation = load_lottieurl('https://lottie.host/3081ee29-1f84-40ab-b52b-9210dcd94ef8/VlfJxatkOm.json')
st_lottie(animation,speed = .99,quality = 'high',height = 400,width = 600)

# st.image('https://www.cars.com/images/sell/sale-dealer-woman.jpg')
st.markdown('''
## Welcome to the Used Car Data Analysis App!

### Summary:
This application analyzes and displays data about used cars. It allows you to explore and examine the data in a simple and detailed manner.

### Features:
- **Filtering:** Filter cars based on various criteria such as brand, model, price, and more.
- **Statistics and Analysis:** Explore detailed statistics on prices, most common brands, and more.
- **Interactive Charts:** Enjoy a fun browsing experience with interactive charts to illustrate trends and statistics.

### How to Use the App:
1. Select your preferred criteria using the dropdown menu.
2. Click the "Update" button to refresh the data and view the updated results.
3. Enjoy a comprehensive analysis of used car data!

### Column Descriptions:
- **Sales ID**: Sales ID\n
- **Name**: Name of the used car\n
- **Year**: Year of the car purchase\n
- **Selling Price**: Current sellling price for used car\n
- **Km Driven**: Total km driven\n
- **Region**:	Region where it is used\n
- **State or Province**: State or Province where it is used\n
- **City**: City where it is used\n
- **Fuel**: Fuel type\n
- **Seller Type**: Who is selling the car\n
- **Transmission**: Transmission type of the car\n
- **Owner**: Owner type\n
- **Mileage**: Mileage of the car\n
- **Engine**:	Engine Power\n
- **Max Power**: Max Power\n
- **Seats**: Number of seats\n
- **Sold**: used car sold or not
''')

st.write("<span style='color: white; font-family: Arial, sans-serif; font-size: 20px;'>this is resourse data from <a href='https://www.kaggle.com/datasets/austinreese/craigslist-carstrucks-data'>Kaggle</a></span>", unsafe_allow_html=True)

st.title('Sample of Data')
if st.checkbox('View Sample of Data'):
    st.dataframe(cars.head(10))