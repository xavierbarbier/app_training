import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import base64
import os
import numpy as np
from collections import Counter
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.util import ngrams
from bs4 import BeautifulSoup
import re
import pandas as pd
import plotly.express as px
import requests
import tweepy
#import time

twitter_candidats = {               
                     "Philippe Poutou" : "PhilippePoutou",
                     "Nathalie Arthaud" : "n_arthaud",
                     "Jean-Luc Mélenchon" : "JLMelenchon",
                     "Fabien Roussel" : "Fabien_Roussel",
                     "Arnaud Montebourg" : "montebourg",
                     "Yannick Jadot" :"yjadot" ,
                     "Anne Hidalgo" : "Anne_Hidalgo",
                     "Christiane Taubira" : "ChTaubira",
                     "Emmanuel Macron" : "EmmanuelMacron",
                     "Valérie Pecresse" : "vpecresse",
                     "Jean Lassalle":"jeanlassalle",
                     "Nicolas Dupont-Aignan" : "dupontaignan",
                     "Marine Le Pen" : "MLP_officiel",
                     "Eric Zemmour" : "ZemmourEric"
                      } 



# creating function with previously tested steps
def text_to_words( raw_text ):
    wordnet_lemmatizer = WordNetLemmatizer()
    # Function to convert a raw text to a string of words
    # The input is a single string (a raw text), and 
    # the output is a single string (a preprocessed text)
    
    text = BeautifulSoup(raw_text).get_text() 

    text = " ".join(filter(lambda x:x[0]!='@', text.split()))

    text = " ".join(filter(lambda x:x[0]!='#', text.split()))

    #text = " ".join(filter(lambda x:x[0]!='https://', text.split()))    

    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', text)

    cleanr = re.compile('{.*?}')
    cleantext = re.sub(cleanr, ' ', cleantext) 

    cleantext = re.sub(r'[^\w\s]',' ',cleantext) 

    cleantext = re.sub(r'http\S+', '', cleantext)   

    cleantext = re.sub(r'co', '', cleantext)  

    words = cleantext.lower().split()        

    lemmatized_words = [wordnet_lemmatizer.lemmatize(w) for w in words] 
    
    stops = set(stopwords.words("french"))                  
    
    meaningful_words = [w for w in lemmatized_words if not w in stops]   
   
    return( " ".join( meaningful_words)) 


#### API TWITTER


auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
# Construct the API instance
api = tweepy.API(auth)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([html.P("Sélectionnez un(e) candidat(e):"),
        dcc.Dropdown(
                        id='candidat',
                        value='Toutes',
                        clearable=True,
                        options=[
                            {'label': name, 'value': name}
                            for name in twitter_candidats.keys()]),
        html.Div(id='container-button-basic')
])
# update bar chart #1
@app.callback(
    Output('container-button-basic', 'children'),
    Input("candidat",'value'),
)
def update_bar_chart(cand):
    
    tweet = []
    date = []

    ID = twitter_candidats[str(cand)]
    list_tweets = api.user_timeline(ID, count = 100)

    for t in range(len(list_tweets)):
      
      id = list_tweets[t].id
      status = api.get_status(id, tweet_mode="extended")
      try:
          tweet.append(status.retweeted_status.full_text)
          date.append(status.created_at.strftime('%y-%m-%d'))
      except AttributeError:  # Not a Retweet
          tweet.append(status.full_text)
          date.append(status.created_at.strftime('%y-%m-%d'))

    text = []
    for t in tweet:
      text.append(text_to_words(t))

    corpus = ' '.join(text)

    words = corpus.split()
    

    fdist1 = nltk.FreqDist(words)

    filtered_word_freq = dict((word, freq) for word, freq in fdist1.items() if not word.isdigit())

    freq = pd.DataFrame.from_dict(filtered_word_freq, orient='index').sort_values(0).tail(25)
    freq.reset_index(inplace=True)
    freq.columns = ["Mot", "Quantité"]

    polarity = []
    for pub in text:
      polarity.append(TextBlob(pub,pos_tagger=PatternTagger(),analyzer=PatternAnalyzer()).sentiment[0])

    temp = pd.DataFrame({"Date":date,"Sentiment":polarity, "Tweet":tweet})

    fig = px.scatter(temp, x="Date", y="Sentiment",
                 title='Polarité des sentiments des 100 derniers Tweets (+1: positif | -1: négatif)',
                 hover_data=["Sentiment", "Tweet"],
                 color = "Sentiment")
    fig.update_layout(yaxis_range=[-1,1])

    return html.Div([dcc.Graph(figure=fig)])


if __name__ == '__main__':
    app.run_server(debug=True)
