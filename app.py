import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
        
    html.Div(["Title: ",
              dcc.Input(id='my-title', value='...', type='text')]),
    html.Br(),
    
    html.Div(["Body: ",
              dcc.Input(id='my-body', value='...', type='text')]),
    html.Br(),
       
    html.Button('Submit', id='button',n_clicks = 0),
    
    html.Br(),
    
    html.Div(id='the-title'),
    html.Div(id='the-body')
    
])



if __name__ == '__main__':
    app.run_server(debug=True)
