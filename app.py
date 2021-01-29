import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State# Load Data
from sklearn.externals import joblib
import nltk
nltk.download('stopwords')
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('punkt')
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import pandas as pd  
from bs4 import BeautifulSoup

# load model and preprocessing
loaded_model = joblib.load("classifier.pkl")
body_count_vect = joblib.load("classifier.pkl")
title_count_vect = joblib.load("title_count_vect.pkl")
body_Transformer = joblib.load("body_Transformer.pkl")
title_Transformer = joblib.load("title_Transformer.pkl")

multilabel_binarizer = joblib.load("multilabel_binarizer.pkl")

wordnet_lemmatizer = WordNetLemmatizer()
stops = set(stopwords.words("english")) 

def text_to_words( raw_text ):

    text = BeautifulSoup(raw_text).get_text()
         
    letters_only = re.sub("[^a-zA-Z]", " ", text) 
    
    words = letters_only.lower().split()        

    lemmatized_words = [wordnet_lemmatizer.lemmatize(w) for w in words] 
      
    meaningful_words = [w for w in lemmatized_words if not w in stops]   

    return (" ".join( meaningful_words)) 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    html.H2('Hello World'),
        
    html.Div(["Title: ",
              dcc.Input(id='my-title', type='text',style={'width': '100%'})]),
    
    
    html.Div(["Body: ",
              dcc.Input(id='my-body', type='text',style={'width': '100%', "height": "300px"})]),
    
       
    html.Button('Submit', id='button'),
    
    
    
    html.Div(id='the-title')
    
])


@app.callback(Output(component_id='the-title', component_property='children'),
              Input(component_id='button', component_property='n_clicks'),
              State(component_id='my-title', component_property='value'),
              State(component_id='my-body', component_property='value'))
def update_output(n_clicks, input1, input2):
    if n_clicks is None:
        raise PreventUpdate
    else:
      #clean title      
      clean_title = text_to_words(input1)
      #clean body
      clean_body = text_to_words(input2)
      #  title counts
      title_counts = title_count_vect.transform([clean_title])
      # body counts
      body_counts = body_count_vect.transform([clean_body])
      # title tfidf
      title_tfidf  = title_Transformer.transform(title_counts)
      # body tfidf
      body_tfidf  = body_Transformer.transform(title_counts)
      # stack inputs
      X = np.hstack([title_tfidf.toarray(),body_tfidf.toarray()])
      #predict
      pred = loaded_model.predict(X)
      # inverse transform
      tags = multilabel_binarizer.inverse_transform(pred)
      return  "Tag(s): {}".format(tags)

if __name__ == '__main__':
    app.run_server(debug=True)
