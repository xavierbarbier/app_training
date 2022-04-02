import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import base64
import joblib 
import os
import numpy as np
import re
import pandas as pd


import plotly.express as px


data = pd.read_csv("datatweets_sentiments.csv")

candidats = ['Philippe Poutou',
            'Nathalie Arthaud',
            'Jean-Luc Mélenchon',
            'Fabien Roussel',
            'Yannick Jadot',
            'Anne Hidalgo',
            'Emmanuel Macron',
            'Valérie Pecresse',
            'Jean Lassalle',
            'Nicolas Dupont-Aignan',
            'Marine Le Pen',
            'Eric Zemmour']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = hhtml.Div(
              [html.H1("Exploration Twitter des candidats(es) à l'élection présidentielle 2022."),
              dcc.Link("Liste mise à jour le 8/01/2022 à partir de l'article en lien",
                      target='_blank',
                      href = "https://www.francetvinfo.fr/politique/christiane-taubira/presidentielle-2022-les-choses-sont-encore-tres-serrees-a-droite-face-a-emmanuel-macron-qui-domine-le-premier-tour-selon-notre-sondage_4909153.html" ),
              html.Plaintext('By Xavier Barbier - @xavbarbier'),
              html.P("Sélectionnez un(e) candidat(e):"),
              dcc.Dropdown(
                        id='candidat',
                        value='Toutes',
                        clearable=True,
                        options=[
                            {'label': name, 'value': name}
                            for name in candidats]),
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
    
    temp = data[data["candidat"] == cand]

    fig = px.scatter(temp, x="dates", y="Sentiment",size = "size",
                 title='Polarité des sentiments des Tweets depuis le 1er janvier 2022 (+1: positif | 0: négatif)',
                 hover_data=["Sentiment", "tweets"],range_color = [0,1],
                 color = "Sentiment")
    fig.update_layout(yaxis_range=[0,1])
    return html.Div([dcc.Graph(figure=fig)
                     ])
