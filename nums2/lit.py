import streamlit as st
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import time
from datetime import date, timedelta
#import os

def cleanDates(days):
    daysNew = []
    for day in days:
        ds = day.split('/')
        month = ds[0]
        day = ds[1]
        year = ds[2]
    
        if int(day) < 10:
            day = '0'+day
        if int(month) < 10:
            month = '0'+month
        daysNew.append(day+"."+month)#+"."+year)
    return daysNew


st.title('Corona statistics')
#csvs = [fl for fl in os.listdir('data/')]
csv = (date.today()-timedelta(1)).strftime('%m-%d-%Y')+".csv"

#data = load_data(10000)
#data = [pd.read_csv('./data/'+x).rename(columns={"Lat": "latitude","Long_": "longitude"}) for x in csvs]
data = [pd.read_csv('./data/'+csv).rename(columns={"Lat": "latitude","Long_": "longitude"})]
newestDay = data[-1].groupby('Country_Region').sum().drop(columns=['FIPS','Unnamed: 0'])



st.subheader('Draw today\'s pie chart')
country = 'Germany'
df_country_selected = newestDay.loc[country].drop(['longitude','latitude'])

st.write("Total cases: ",str(df_country_selected.Confirmed)[:-2])
plt.pie(x=df_country_selected.drop(['Confirmed', 'Incident_Rate', 'Case_Fatality_Ratio']),colors=(list(['black','green','darkred'])),
        labels=list(['Dead: '+str(df_country_selected[1])[:-2],
                    'Recovered: '+str(df_country_selected[2])[:-2],
                    'Infected: '+str(df_country_selected[3])[:-2]]))
st.pyplot()


st.header('Display information about some countries')

cs2 = st.multiselect("Select countries",list(newestDay.index.values),default=['Germany','Spain','France','United Kingdom','Italy','Austria'])
cs = newestDay.loc[cs2].drop(columns=['latitude','longitude'])
if st.checkbox('Show table'):
    st.write(cs)
if cs2:
    st.bar_chart(cs.drop(columns='Confirmed'))
else:
    st.error("Enter a country above first!")

##

confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv').groupby('Country/Region').sum()
dead = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv').groupby('Country/Region').sum()
recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv').groupby('Country/Region').sum()


st.header('Timelines')

confirmedClean = confirmed.loc[cs2].drop(columns=['Lat','Long'])
confirmedClean.columns = cleanDates(confirmedClean.columns.values)
deadClean = dead.loc[cs2].drop(columns=['Lat','Long'])
deadClean.columns = cleanDates(deadClean.columns.values)
recoveredClean = recovered.loc[cs2].drop(columns=['Lat','Long'])
recoveredClean.columns = cleanDates(recoveredClean.columns.values)

typ = st.radio(
    "Which plot?",
    ('Confirmed cases', 'Dead', 'Recovered'))

if typ == 'Confirmed cases' and cs2:
    st.subheader('Confirmed cases:')
    startday = 25
    for country in cs2:
        plt.plot(confirmedClean.columns[startday:], confirmedClean.loc[country][startday:], label=country)
    plt.legend()
    plt.xticks(confirmedClean.columns[startday::7])
    plt.grid('b')
    st.pyplot()
elif typ == 'Dead' and cs2:
    st.subheader('Total dead:')
    startday = 25
    for country in cs2:
        plt.plot(deadClean.columns[startday:], deadClean.loc[country][startday:], label=country)
    plt.legend()
    plt.xticks(deadClean.columns[startday::7])
    plt.grid('b')
    st.pyplot()
elif typ == 'Recovered' and cs2:
    st.subheader('Total recovered:')
    startday = 25
    for country in cs2:
        plt.plot(recoveredClean.columns[startday:], recoveredClean.loc[country][startday:], label=country)
    plt.legend()
    plt.xticks(recoveredClean.columns[startday::7])
    plt.grid('b')
    st.pyplot()
else:
    st.error("Enter a country above first!")



add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone'))

#st.header('It\'s a map!')
#st.map(data[-1])

st.subheader('Most recent raw data')
if st.checkbox('Orig data'):
    st.write(data[-1])
if st.checkbox('Clean data'):
    st.write(newestDay)
