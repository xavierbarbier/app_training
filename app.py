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
              dcc.Input(id='my-title', value='...', type='text',style={'width': '100%'})]),
    html.Br(),
    
    html.Div(["Body: ",
              dcc.Input(id='my-body', value='...', type='text',style={'width': '100%'})]),
    html.Br(),
       
    html.Button('Submit', id='button',n_clicks = 0),
    
    html.Br(),
    
    html.Div(id='the-title'),
    html.Div(id='the-body')
    
])

@app.callback(
    dash.dependencies.Output('the-title', 'children'),dash.dependencies.Output('the-body', 'children'),
    [dash.dependencies.Input('button', 'n_clicks')],
    [dash.dependencies.State('my-title', 'value'),dash.dependencies.State('my-body', 'value')]    
def update_title(n_clicks,value):
    if n_clicks is None:
        raise PreventUpdate
    else:
        return 'Output : {}'.format(value)
    

if __name__ == '__main__':
    app.run_server(debug=True)
