import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

#reading the datra
filepath = r"reviews_with_center.csv"
data = pd.read_csv(filepath)
#some cleaning  data
data['CenterNew']=data['Center'].apply(lambda s: s.split("_")[0])
data['CenterNew']=data['CenterNew'].replace({'at':'bengaluru'})
data['CenterNew']=data['CenterNew'].replace({'club':'ahmedabad'})
data['CenterNew']=data['CenterNew'].replace({'courtyard':'ahmedabad'})
data['CenterNew']=data['CenterNew'].replace({'forum':'chennai'})
data['CenterNew']=data['CenterNew'].replace({'hyatt':'goa'})
data['CenterNew']=data['CenterNew'].replace({'le':'kodaikanal'})
data['CenterNew']=data['CenterNew'].replace({'lemon':'mumbai'})
data['CenterNew']=data['CenterNew'].replace({'mantri':'bengaluru'})
data['CenterNew']=data['CenterNew'].replace({'new':'new_delhi'})
data['CenterNew']=data['CenterNew'].replace({'radisson':'hyderabad'})
data['CenterNew']=data['CenterNew'].replace({'grand':'mysuru'})
#Nohotal has 2 citys so extracting that city name

data['CenterNew2']=data['Center'].apply(lambda s: s.split("_")[1])
data['CenterNew2']=data['CenterNew2'].replace({'ahmedabad-ahmedabad':'ahmedabad'})
data['CenterNew2']=data['CenterNew2'].replace({'hicc':'hyderabad'})
mask = data['CenterNew'] == 'novotel'
data.loc[mask, 'CenterNew'] = data.loc[mask, 'CenterNew2']


#streaming app
with st.container():
    st.title("WELCOME TO ODE SPA")
    st.sidebar.title("Navigation")
    x = st.sidebar.selectbox("which city data do u want", data['CenterNew'].unique())
    city_data = data[data['CenterNew'] == x]


    def get_sentiment(text):
        analysis = TextBlob(text)
        sentiment = analysis.sentiment.polarity
        if sentiment > 0:
            return 'Positive'
        elif sentiment == 0:
            return 'Neutral'
        else:
            return 'Negative'


    city_data['Sentiment'] = city_data['Review'].apply(get_sentiment)

    # Count the occurrences of each sentiment label
    sentiment_counts = city_data['Sentiment'].value_counts()

    # Streamlit app
    st.subheader('Sentiment Analysis App')

    # Display sentiment distribution using a bar chart
    st.subheader('Sentiment Distribution')
    fig, ax = plt.subplots(figsize=(6,3))
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values, ax=ax)
    plt.title('Sentiment Distribution')
    plt.xlabel('Sentiment')
    plt.ylabel('Count')
    st.pyplot(fig)
