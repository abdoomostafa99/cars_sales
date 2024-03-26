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



st.title('Check Average Price')
cars['km_driven_cat'] = pd.cut(cars['km_driven'] , bins = [0,10000,20000,30000,40000,50000,100000] , labels = ['<10k' , '10k-20k' , '20k-30k' , '30k-40k' , '40k-50k' , '50k+']) 
cars['engine_cat'] = pd.cut(cars['engine'] , bins = [0,1000,2000,3000,4000] , labels = ['<1000' , '1000-2000' , '2000-3000' , '3000-4000'])

Brand = st.selectbox('Select Brand' , cars.name.unique())

Transmission = st.selectbox('Select Transmission' , cars.transmission.unique())

Engine = st.selectbox('Select Engine' , cars.engine_cat.unique())

Km = st.selectbox('Select KM' , cars.km_driven_cat.unique())

if st.button('Check'):
    filter = cars[
            (cars['name'] == Brand) &
            (cars['engine_cat'] == Engine) &
            (cars['transmission'] == Transmission) & 
            (cars['km_driven_cat'] == Km)
            ]['selling_price'].mean()    
    try :
            filter = filter.round(2)
    except:
        filter = 'nan'

    if filter == 'nan':
        x = cars['selling_price'].mean()
        st.subheader(f'Average Price is {x.round(2)}')
    else:
        st.subheader(f'Average Price is {filter}')