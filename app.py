import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
    
    html.Div(["Input: ",     
        dcc.Textarea(id='title',
        placeholder='Enter a title for your question...',
        style={'width': '100%'})]),
    
    html.Br(),
    
    html.Div(["Input: ",     
        dcc.Textarea(id='body',
        placeholder='Enter a body for your question...',
        style={'width': '100%'})]),
    
    html.Br(),
    
    html.Button('Submit', id='button'),
              
    html.Div(id='my-output')
    
    
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='title', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

if __name__ == '__main__':
    app.run_server(debug=True)
