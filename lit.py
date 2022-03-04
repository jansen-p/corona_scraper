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
        daysNew.append(day+"."+month+"."+year)
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
fig, ax = plt.subplots()
ax.pie(x=df_country_selected.drop(['Incident_Rate', 'Case_Fatality_Ratio', 'Recovered','Active']),colors=(list(['orange','black'])),#'darkred'])),
        labels=list(['Confirmed: '+str(df_country_selected[0])[:-2],
                     'Dead: '+str(df_country_selected[1])[:-2],
                    ]))
                    #'Infected: '+str(df_country_selected[3])[:-2]]))

st.pyplot(fig)


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

src = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_'
confirmed = pd.read_csv(src+'confirmed_global.csv').groupby('Country/Region').sum()
dead = pd.read_csv(src+'deaths_global.csv').groupby('Country/Region').sum()
recovered = pd.read_csv(src+'recovered_global.csv').groupby('Country/Region').sum()


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

startday = 25
stepsize = int(len(confirmedClean.columns[startday:])/10)
rotation = 45
fig, ax = plt.subplots()
if typ == 'Confirmed cases' and cs2:
    st.subheader('Confirmed cases:')
    for country in cs2:
        ax.plot(confirmedClean.columns[startday:], confirmedClean.loc[country][startday:], label=country)
    ax.set_xticks(confirmedClean.columns[startday::stepsize])
    ax.set_xticklabels(list(confirmedClean.columns[startday::stepsize]),rotation=rotation)
elif typ == 'Dead' and cs2:
    st.subheader('Total dead:')
    for country in cs2:
        ax.plot(deadClean.columns[startday:], deadClean.loc[country][startday:], label=country)
    ax.set_xticks(deadClean.columns[startday::stepsize])
    ax.set_xticklabels(list(deadClean.columns[startday::stepsize]),rotation=rotation)
elif typ == 'Recovered' and cs2:
    st.subheader('Total recovered:')
    for country in cs2:
        ax.plot(recoveredClean.columns[startday:], recoveredClean.loc[country][startday:], label=country)
    ax.set_xticks(recoveredClean.columns[startday::stepsize])
    ax.set_xticklabels(list(recoveredClean.columns[startday::stepsize]),rotation=rotation)
else:
    st.error("Enter a country above first!")
ax.legend()
ax.grid('b')
st.pyplot(fig)


#add_selectbox = st.sidebar.selectbox(
#    'How would you like to be contacted?',
#    ('Email', 'Home phone', 'Mobile phone'))

#st.header('It\'s a map!')
#st.map(data[-1])

st.subheader('Most recent raw data')
if st.checkbox('Orig data'):
    st.write(data[-1])
if st.checkbox('Clean data'):
    st.write(newestDay)
