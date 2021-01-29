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
              dcc.Input(id='my-title', type='text',style={'width': '100%'})]),
    
    
    html.Div(["Body: ",
              dcc.Input(id='my-body', type='text',style={'width': '100%', "height": "300px"})]),
    
       
    html.Button('Submit', id='button'),
    
    
    
    html.Div(id='my-output')
    
])


@app.callback(Output(component_id='my-output', component_property='children'),
              Input(component_id='button', component_property='n_clicks'),
              State(component_id='my-title', component_property='value'),
              State(component_id='my-body', component_property='value'))
def update_output(n_clicks, input1, input2):
    if n_clicks is None:
        raise PreventUpdate
    else:
      #clean title
      #clean body
      # preprocess title

      # prepocess body

      # stack inputs

      #predict
        return str(input1), " ",str(input2)
    

if __name__ == '__main__':
    app.run_server(debug=True)
