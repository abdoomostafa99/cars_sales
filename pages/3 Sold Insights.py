import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import random
import requests
from streamlit_lottie import st_lottie
import json
st.set_page_config(layout = 'wide' , page_title = 'Sold Insights')
cars = pd.read_csv('UserCarData.csv')
cars.drop(['mileage' , 'torque'] , axis=1 , inplace=True)
cars.columns = cars.columns.str.lower().str.strip()
cars.columns = cars.columns.str.replace(' ' , '_')
cars.sold= cars.sold.apply(lambda x: 'sold' if x == 'Y' else 'not sold')
st.title('Sold Insights Analysis')

def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
animation = load_lottieurl('https://lottie.host/3124bd5f-7ac0-4dde-8b4b-173b2966da66/CATdYF6lH0.json')
st_lottie(animation,speed = .99,quality = 'high',height = 400,width = 600)

c1,c33,c2 = st.columns([4,1,4])


with c1 :

    cars['km_driven_cat'] = pd.cut(cars['km_driven'] , bins = [0,10000,20000,30000,40000,50000,100000] , labels = ['<10k' , '10k-20k' , '20k-30k' , '30k-40k' , '40k-50k' , '50k+']) 
    km = cars.groupby(['km_driven_cat', 'sold'])['sales_id'].count().reset_index().sort_values(by = 'km_driven_cat' , ascending = True)
    st.plotly_chart(px.line(km,x='km_driven_cat', y='sales_id', color='sold',
                title='Sold vs Available Cars per KM',
                labels={'km_driven_cat':'KM' , 'sales_id':'Number of cars'},template = 'plotly_dark',width=600,height=400))
    st.subheader('**Cars with the highest KM are the least sold**')

with c2:

    cars['price_cat'] = pd.cut(cars['selling_price'] , bins = [0,100000,200000,300000,400000,500000,1000000] , labels = ['<100k' , '100k-200k' , '200k-300k' , '300k-400k' , '400k-500k' , '500k+'])
    price = cars.groupby(['price_cat' , 'sold'])['sales_id'].count().reset_index().sort_values(by = 'price_cat' , ascending = True)
    st.plotly_chart(px.line(price , x = 'price_cat' , y = 'sales_id' , color='sold',
                title='Sold vs Available Cars per price',
                labels={'price_cat':'Price' , 'sales_id':'Number of cars'},template = 'simple_white',width=600,height=400))
    st.subheader('**Cars with the price 500K+ are the least sold**')
st.divider()

c3,c44,c4 = st.columns([4,1,4])
with c3:

    y_s = cars.groupby(['year', 'sold'])['sales_id'].count().reset_index().sort_values(by = 'year' , ascending = True)

    st.plotly_chart(px.bar(y_s,x='year', y='sales_id', color='sold',barmode='group'
                        ,title='Sold vs Available Cars per year',labels={'year':'Year' , 'sales_id':'Number of cars'}
                        ,template = 'plotly_dark',width=600,height=400))
    st.subheader('**2017 is the most model sold**')
with c4:

    region = cars.groupby(['region','sold'])['sales_id'].count().reset_index()
    st.plotly_chart(px.bar(region , x = 'region' , y = 'sales_id' , color='sold',
                title='Sold vs Available Cars per Region',
                labels={'region':'Region' , 'sales_id':'Number of cars'},template = 'simple_white' , barmode='group',width=600,height=400))
    st.subheader('**most sold cars in the East**')
st.divider()
c5,c55,c6 = st.columns([4,1,4])
with c5:

    fuel = cars.groupby(['fuel' , 'sold'])['sales_id'].count().reset_index()
    st.plotly_chart(px.bar(data_frame=fuel , x='fuel' , y='sales_id' , color='sold' ,
                title='Sold vs Available Cars per fuel type',
                labels={'fuel':'Fuel Type' , 'sales_id':'Number of cars'},template = 'simple_white' , barmode='group',width=600,height=400))
    st.subheader('**cars use Diesel is the most common sales**')

with c6:
    fig = px.sunburst(cars.groupby(['transmission' , 'sold'])['sales_id'].count().reset_index() , path=['transmission','sold'],values='sales_id',color='transmission')
    fig.update_traces(textinfo='label+percent parent')
    st.plotly_chart(fig)
    st.subheader('**Automatic cars sold more than Manual**')

st.divider()
c7,c66,c8 = st.columns([4,1,4])
with c7:

    cars['engine_cat'] = pd.cut(cars['engine'] , bins = [0,1000,2000,3000,4000] , labels = ['<1000' , '1000-2000' , '2000-3000' , '3000-4000'])
    engine = cars.groupby(['engine_cat','sold'])['sales_id'].count().reset_index()
    st.plotly_chart(px.bar(engine,x='engine_cat', y='sales_id', color='sold',
                title='Sold vs Available Cars engine',
                labels={'engine_cat':'Engine' , 'sales_id':'Number of cars'},template = 'simple_white',barmode='group',width=600,height=400))
    st.subheader('**Cars with engine 1000-2000 are the most sold**')

with c8:

    cars['max_power_cat'] = pd.cut(cars['max_power'] , bins = [0,50,100,150,200,250,300,350,400] , labels = ['<50' , '50-100' , '100-150' , '150-200' , '200-250' , '250-300' , '300-350' , '350-400'])
    max_power = cars.groupby(['max_power_cat','sold'])['sales_id'].count().reset_index()
    st.plotly_chart(px.bar(max_power,x='max_power_cat', y='sales_id', color='sold',
                title='Sold vs Available Cars max power',
                labels={'max_power_cat':'Max Power' , 'sales_id':'Number of cars'},template = 'simple_white',barmode='group',width=600,height=400))
    st.subheader('**Cars with max power 50-100 are the most sold**')
st.divider()
c9,c77,c10 = st.columns([4,1,4])
with c9:

    namee = cars['name'].value_counts().reset_index().head(10)['index']
    x = cars.groupby(['sold','name'])['sales_id'].count().reset_index().sort_values(by = 'sales_id' , ascending=False)
    soldd = x[x['name'].isin(namee)].reset_index()
    st.plotly_chart(px.bar(soldd,x='name', y='sales_id', color='sold',
                barmode='group',title='Sold vs Available Cars',
                labels={'name':'Brand' , 'sales_id':'Number of cars'},template = 'plotly_dark',width=600,height=400))
    st.subheader('**Maruti is the most sold car**')

with c10:

    statee = cars['state_or_province'].value_counts().reset_index().head(10)['index']
    state = cars.groupby(['state_or_province','sold'])['sales_id'].count().reset_index()
    s = state[state['state_or_province'].isin(statee)].reset_index()
    st.plotly_chart(px.bar(s , x = 'state_or_province' , y = 'sales_id' , color='sold',
                title='Sold vs Available Cars per State',
                labels={'state_or_province':'State' , 'sales_id':'Number of cars'},template = 'plotly_dark' , barmode='group',width=600,height=400))
    st.subheader('**New York most state sold cars**')
