import os

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H2('Hello World'),
    
    dcc.Textarea(
    placeholder='Enter a title for your question...',
    style={'width': '100%'}),
    
    dcc.Textarea(
    placeholder='Enter a title for your question...',
    style={'width': '100%'}),
    
    html.Button('Submit', id='button'),
    
    
])

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
