import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import base64
import joblib 
import os
import numpy as np
import emoji
import nltk
from nltk.corpus import stopwords
from nltk.util import ngrams
from bs4 import BeautifulSoup
import re
import pandas as pd
import requests
import tweepy
import time
#import tensorflow as tf
#from tensorflow import keras
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from transformers import TextClassificationPipeline
import plotly.express as px

model_name = "xavierbarbier/camembert-flue"
tokenizer_name = "camembert-base"


nlp = TextClassificationPipeline(model=TFAutoModelForSequenceClassification.from_pretrained(model_name),
                            tokenizer=AutoTokenizer.from_pretrained(tokenizer_name),
                            return_all_scores = True)



twitter_candidats = {               
                     "Philippe Poutou" : "PhilippePoutou",
                     "Nathalie Arthaud" : "n_arthaud",
                     "Jean-Luc Mélenchon" : "JLMelenchon",
                     "Fabien Roussel" : "Fabien_Roussel",
                     "Florian Philippot" : "f_philippot",
                     "Yannick Jadot" :"yjadot" ,
                     "Anne Hidalgo" : "Anne_Hidalgo",
                     "Christiane Taubira" : "ChTaubira",
                     "Emmanuel Macron" : "EmmanuelMacron",
                     "Valérie Pecresse" : "vpecresse",
                     "Jean Lassalle":"jeanlassalle",
                     "Nicolas Dupont-Aignan" : "dupontaignan",
                     "Marine Le Pen" : "MLP_officiel",
                     "Eric Zemmour" : "ZemmourEric",
                      "François Asselineau" : "UPR_Asselineau",
                      "Hélène Thouy" : "HeleneThouy"  
                      } 



# creating function with previously tested steps
def text_to_words( raw_text ):
    
    # Function to convert a raw text to a string of words
    # The input is a single string (a raw text), and 
    # the output is a single string (a preprocessed text)
    text = BeautifulSoup(raw_text).get_text() 

    text = " ".join(filter(lambda x:x[0]!='@', text.split()))

    text = " ".join(filter(lambda x:x[0]!='#', text.split()))

    text = re.sub(r'http\S+', '', text)
    
    text = emoji.demojize(text, delimiters=("", ""), language = "fr")

    text = text.replace("_"," ")

    words = text.lower().split()        

    #lemmatized_words = [stemmer.stem(w) for w in words] 
    
    stops = set(stopwords.words("french"))                  
    
    meaningful_words = [w for w in words if not w in stops]  
       
    return( " ".join( meaningful_words))


#### API TWITTER
API_KEY = "mgNKxsjIZmT39T9dwIENFP8Q6"
API_SECRET_KEY = "DSO5Uugz4YezqonmlbM0BDYdlmARsqv2Jn8OPLswoL8mDnuRqx"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAABdKQgEAAAAAkiYc1xJIIJAWs80iUXT31UF5RDU%3DbprET2yBMEtLEJ1sGBRSmT5mq7JETBjpEA9RGWt0slezlTQkpg"
auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
# Construct the API instance
api = tweepy.API(auth)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([html.H1("Exploration Twitter des candidats(es) à l'élection présidentielle 2022."),
            dcc.Link("Liste mise à jour le 5/02/2022 à partir de l'article en lien",
                     target='_blank',
                      href = "https://www.francetvinfo.fr/elections/sondages/derniers-sondages-sur-election-presidentielle-2022-en-france-infographies-explorez-les-tendances-visualisez-les-marges-d-erreur-agregateur_4879975.html" ),
            html.Plaintext('By Xavier Barbier - @xavbarbier'),
            html.P("Sélectionnez un(e) candidat(e):"),
        dcc.Dropdown(
                        id='candidat',
                        value='Toutes',
                        clearable=True,
                        options=[
                            {'label': name, 'value': name}
                            for name in twitter_candidats.keys()]),
                       html.Button('Submit', id='submit-val', n_clicks=0),
        html.Div(id='container-button-basic'),
                       html.Div(id='container-button-basic2')
])
# update bar chart #1
@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
  [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.Input("candidat",'value')])
def update_bar_chart(n_clicks , cand):
  changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
  if 'submit-val' in changed_id: 
    
    tweet = []
    date = []

    ID = twitter_candidats[str(cand)]
    list_tweets = api.user_timeline(ID, count = 100)

    for t in range(len(list_tweets)):
      
      id = list_tweets[t].id
      status = api.get_status(id, tweet_mode="extended")
      try:
          tweet.append(status.retweeted_status.full_text)
          date.append(status.created_at)
      except AttributeError:  # Not a Retweet
          tweet.append(status.full_text)
          date.append(status.created_at)

    text = []
    for t in tweet:
      text.append(text_to_words(t))

    corpus = ' '.join(text)

    words = corpus.split()    

    polarity = []
    for pub in text:
      
      polarity.append(nlp(pub)[0][1]["score"])

    temp = pd.DataFrame({"Date":date,"Sentiment":polarity, "Tweet":tweet})
    size = 3
    temp["size"] = size

    fig = px.scatter(temp, x="Date", y="Sentiment",size = "size",
                 title='Polarité des sentiments des 100 derniers Tweets (+1: positif | -1: négatif)',
                 hover_data=["Sentiment", "Tweet"],range_color = [0,1],
                 color = "Sentiment")
    fig.update_layout(yaxis_range=[0,1])

    return html.Div([dcc.Graph(figure=fig)
                     ])
# update bar chart #1
@app.callback(
    dash.dependencies.Output('container-button-basic2', 'children'),
  [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.Input("candidat",'value')])
def update_bar_chart2(n_clicks , cand):
  changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
  if 'submit-val' in changed_id: 
    ID = twitter_candidats[str(cand)]
    # replies
    reponses = []
    replies_dates = []
    count = 0  
    replies = tweepy.Cursor(api.search, q='to:{}'.format(ID),
                                    #since_id=tweet_id,
                            tweet_mode='extended').items()
    for r in replies:
      if count != 50:
        status = api.get_status(r.id, tweet_mode="extended")
        reponses.append(status.full_text)
        replies_dates.append(status.created_at)
        count += 1
      else:
        break
    
    rep_text = []
    for t in reponses:
      rep_text.append(text_to_words(t))

    rep_polarity = []
    for pub in rep_text:
      
      rep_polarity.append(nlp(pub)[0][1]["score"])

    rep_temp = pd.DataFrame({"Date":replies_dates,"Sentiment":rep_polarity, "Tweet":reponses})
    size = 3
    rep_temp["size"] = size
    
    rep_fig = px.scatter(rep_temp, x="Date", y="Sentiment",size = "size",
                    title='Polarité des sentiments des 50 dernières réponses (+1: positif | 0: négatif)',
                    hover_data=["Sentiment", "Tweet"],range_color = [0,1],
                    color = "Sentiment")
    rep_fig.update_layout(yaxis_range=[0,1])
 

    return html.Div([dcc.Graph(figure=rep_fig)
                     ])
