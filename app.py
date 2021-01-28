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
              dcc.Input(id='my-title', value='initial value', type='text',style={'width': '100%'})]),
    html.Br(),
    html.Div(["Body: ",
              dcc.Input(id='my-body', value='initial value', type='text',style={'width': '100%'})]),
    html.Br(),
    html.Div(id='my-output')
    
])

@app.callback(
    dash.dependencies.Output(component_id='my-output', component_property='children'),
    [dash.dependencies.Input(component_id='my-title', component_property='value')]
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
