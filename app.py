import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State# Load Data
import joblib
import nltk
from nltk.stem import WordNetLemmatizer
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
body_count_vect = joblib.load("body_count_vect.pkl")
title_count_vect = joblib.load("title_count_vect.pkl")
body_Transformer = joblib.load("body_Transformer.pkl")
title_Transformer = joblib.load("title_Transformer.pkl")

lda_count_vect = joblib.load("lda_count_vect.pkl")
lda_Transformer = joblib.load("lda_Transformer.pkl")
lda_model= joblib.load("lda_model.pkl")

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

# preparing topics form LDA
def save_topics(model, feature_names, no_top_words=4):  
  for topic_idx, topic in enumerate(model.components_):
        topix_id = topic_idx
        lda_tags.append((" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]])))
# getting topics
lda_tags = []
save_topics(lda_model, lda_count_vect.get_feature_names())



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src="https://www.ranklogos.com/wp-content/uploads/2015/06/Stack-Overflow-Logo.png",
             style={ "height": "75px"}),
            html.H3('Question automatic tagger'),
            html.H6('By Xavier Barbier - @xavbarbier')
        ], className="four columns"),
        
        html.Div([
            html.Div(["Title: ",
              dcc.Input(id='my-title', placeholder="Enter your title here...", type='text',style={'width': '100%'})]),
    
    
            html.Div(["Body: ",
              dcc.Input(id='my-body', placeholder="Enter your body here...",
                        type='text',style={'width': '100%', "height": "250px","text-align": "top-left","line-height": "3.5"})]),
    
       
            html.Button('Submit', id='button'),
    
            html.Div(id='the-tags')
        ], className="six columns"),
        ], className="row")
])


@app.callback(dash.dependencies.Output(component_id='the-tags', component_property='children'),
              [dash.dependencies.Input(component_id='button', component_property='n_clicks')],
              [dash.dependencies.State(component_id='my-title', component_property='value'),
              dash.dependencies.State(component_id='my-body', component_property='value')])
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
      body_tfidf  = body_Transformer.transform(body_counts)
      # stack inputs
      X = np.hstack([title_tfidf.toarray(),body_tfidf.toarray()])
      #predict
      pred = loaded_model.predict(X)
      # inverse transform
      svm_tags = multilabel_binarizer.inverse_transform(pred)

      tags=[]
      for item in svm_tags:
          if item!=():
            tags.append(item)
      # checking if at least 1 tag is predicted, if not, run LDA 
      if len(tags) == 0 :
        # concat title and body
        full_text = clean_title + clean_body
        # body counts
        full_counts = lda_count_vect.transform([full_text])
        # prediction
        pred = lda_model.transform(full_counts)
        prediction = pd.DataFrame()
        prediction["prob"] = pred.reshape(-1,)
        prediction["tag"] = lda_tags
        prediction = prediction.sort_values("prob", ascending=False)
        prediction.reset_index(inplace=True)
        tags = prediction["tag"]
        tags = tags[0].split()
        
        return "Tag(s): {}".format(tags)

      else:      
        return  "Tag(s): {}".format(tags)

if __name__ == '__main__':
    app.run_server(debug=True)
