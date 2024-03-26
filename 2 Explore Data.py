import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
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

st.title('Explore Analysis')
def load_lottieurl(url:str):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()
animation = load_lottieurl('https://lottie.host/a5bc462f-f206-467d-a988-5a3ea17e1d70/7gYeI6NANK.json')
st_lottie(animation , speed = 2.5 ,quality = 'high',height = 400 , width = 600)




interest = st.selectbox('Select a column to filter by:',
             ['selling_price' , 'km_driven' ,'engine','max_power'])

col1 , col2  = st.columns(2)
card1 = col1.container(border=1)
card1.metric(label = f'Min {interest}' , value = cars[interest].min())

card2 = col2.container(border=1)
card2.metric(label = f'Max {interest}' , value = cars[interest].max())

st.divider()
interest2 = st.selectbox('Select Analysis Type:',
             ['Univariate Analysis' , 'Bivariate Analysis' , 'Multivariate Analysis'])
if interest2 == 'Univariate Analysis':
       x = st.selectbox('Select Column',['Name', 'Year', 'Selling Price' , 'State or province' , 'City' , 'Seller Type','Engine','Max Power'])
       if x == 'Name':
              top_10 = cars.groupby('name')['sales_id'].count().reset_index().sort_values(by = 'sales_id' , ascending=False).head(10)
              st.plotly_chart(px.bar(top_10 , x = 'name' , y = 'sales_id', labels={'name':'Brand' , 'sales_id':'Number of cars'} 
                            , color = 'name' , title = 'Number of top 10 cars each brand'
                            , template = 'plotly_dark',text_auto=True))
              st.subheader('**Maruti is the most popular brand**')

              
       if x == 'Year':
              num_of_year = cars.groupby('year')['sales_id'].count().reset_index()
              st.plotly_chart(px.bar(num_of_year , x = 'year' , y = 'sales_id', labels={'year':'Year' , 'sales_id':'Number of cars'} 
                            , color = 'year' , title = 'Number of cars each year'
                            , template = 'plotly_dark',text_auto=True))
              st.subheader('**2017 is the most year have a car**')

              
       if x == 'Selling Price':
              st.plotly_chart(px.histogram(cars , 'selling_price' , template='presentation' 
                                          , title='selling price',labels={'selling_price':'Selling price'}))
              st.subheader('**Avg price between 0 --> 2M**')

              
       if x == 'State or province':
              num_of_state = cars.groupby('state_or_province')['sales_id'].count().reset_index().sort_values(by ='sales_id',ascending=False).head(10)
              st.plotly_chart(px.bar(num_of_state , x = 'state_or_province' , y = 'sales_id' ,labels={'state_or_province':'State' , 'sales_id':'Number of state'}
                     ,color='state_or_province', title = 'Number of top 10 state' , template = 'plotly_dark', text_auto = True))
              st.subheader('**California is the most popular state**')

              
       if x == 'City':
              popular_city = cars.groupby('city')['sales_id'].count().reset_index().sort_values(by ='sales_id',ascending=False).head(10)
              st.plotly_chart(px.bar(popular_city , y = 'city' , x = 'sales_id' ,labels={'city':'City' , 'sales_id':'Number of city'}
                     ,color='city', title = 'popular city' , template = 'simple_white', text_auto = True))
              st.subheader('**New York City is the most popular city**')

              
       if x == 'Seller Type':
              seller_type = cars.groupby('seller_type')['sales_id'].count().reset_index().sort_values(by ='sales_id',ascending=False).head(10)
              st.plotly_chart(px.pie(seller_type , values = 'sales_id' , names = 'seller_type' 
                     , title = 'Most seller type', hole = 0.3 ))
              st.subheader('**Individual is the most seller type**')

              
       if x == 'Engine':
              enginee = cars.groupby('name')['engine'].mean().reset_index().sort_values(by = 'engine' , ascending = False).head(10)
              st.plotly_chart(px.bar(enginee , y='name',x='engine',color='name',
                     title='Top 10 average engine',labels={'engine':'Engine' , 'name':'Brand'}
                     ,text_auto=True,template = 'plotly_dark'))
              st.subheader('**Isuzu have a max avg engine**')

              
       if x == 'Max Power':
              maxx = cars.groupby('name')['max_power'].mean().reset_index().sort_values(by = 'max_power' , ascending = False).head(10)
              st.plotly_chart(px.bar(maxx , y='name',x='max_power',color='name',
                     title='Top 10 average max power',labels={'max_power':'Max power' , 'name':'Brand'}
                     ,text_auto=True,template = 'plotly_dark'))
              st.subheader('**Lexus have a max avg max power**')

if interest2 == 'Bivariate Analysis':
       z = st.selectbox('Select Column',['Price' , 'Brand'])
       if z == 'Price':
              y = st.selectbox('Select Price Per',['Year', 'Model' , 'KM Driven'])

              if y == 'Year':
                     years= cars.groupby('year')['selling_price'].mean().reset_index()
                     st.plotly_chart(px.line(years,x='year', y='selling_price',
                     title='Average price of cars per year',
                     labels={'year':'Year' , 'selling_price':'Average price'},template = 'plotly_dark'))
                     st.subheader('**cars model 2019 are the most expensive average price**')
              
              
              if y == 'Model':
                     avg_price = cars.groupby('name')['selling_price'].mean().sort_values(ascending=False).reset_index().head(10)
                     st.plotly_chart(px.bar(avg_price , x = 'name' , y = 'selling_price' 
                     , color = 'name' , title = 'Top 10 average price per car model'
                     , template = 'plotly_dark', text_auto = True , labels={'name':'Brand' , 'selling_price':'Average price'}))
                     st.subheader('**Lexus is the most expensive car**')
              
              if y == 'KM Driven':
                     cars['km_driven_cat'] = pd.cut(cars['km_driven'] , bins = [0,10000,20000,30000,40000,50000,100000] , labels = ['<10k' , '10k-20k' , '20k-30k' , '30k-40k' , '40k-50k' , '50k+']) 
                     km_price = cars.groupby('km_driven_cat')['selling_price'].mean().reset_index()
                     st.plotly_chart(px.line(km_price,x='km_driven_cat', y='selling_price',
                     title='Average Price Per KM',
                     labels={'km_driven_cat':'KM' , 'selling_price':'Price'},template = 'plotly_dark'))
                     st.subheader('**Cars with the highest KM are the least Price**')
                     
       if z == 'Brand':
              brand = st.selectbox('Select Brand Per',['Engine', 'Power'])

              if brand == 'Engine':
                     enginee = cars.groupby('name')['engine'].mean().reset_index().sort_values(by = 'engine' , ascending = False).head(10)
                     st.plotly_chart(px.bar(enginee , y='name',x='engine',color='name',
                     title='Top 10 average engine',labels={'engine':'Engine' , 'name':'Brand'}
                     ,text_auto=True,template = 'plotly_dark'))
                     st.subheader('**Isuzu have a max avg engine**')
              
              if brand == 'Power':
                     maxx = cars.groupby('name')['max_power'].mean().reset_index().sort_values(by = 'max_power' , ascending = False).head(10)
                     st.plotly_chart(px.bar(maxx , y='name',x='max_power',color='name',
                     title='Top 10 average max power',labels={'max_power':'Max power' , 'name':'Brand'}
                     ,text_auto=True,template = 'plotly_dark'))
                     st.subheader('**Lexus have a max avg max power**')


if interest2 == 'Multivariate Analysis':
       statee = cars['state_or_province'].value_counts().reset_index().head(10)['index']
       namee = cars['name'].value_counts().reset_index().head(5)['index']
       x = cars.groupby(['state_or_province','name'])['sales_id'].count().reset_index().sort_values(by = 'sales_id' , ascending=False)
       x1 = x[x['state_or_province'].isin(statee)].reset_index()
       x2 = x[x['name'].isin(namee)].reset_index()
       x = pd.merge(x1,x2)
       st.plotly_chart(px.bar(x , x='state_or_province',y='sales_id',color='name',barmode='group',
       title='Top brands in each state',labels={'state_or_province':'State' , 'sales_id':'Number of cars'}
       ,text_auto=True,template = 'plotly_dark'))
       st.subheader('**California is the state with the most cars**')