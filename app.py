import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input
import pandas as pd
import plotly.express as px
import math
import json

url = "essonne.csv"

essonne = pd.read_csv(url)
essonne.drop("Unnamed: 0", axis = 1 , inplace = True)

url = "essonne_geo.json"

# Read data from file:
essonne_geo = json.load( open( url ) )

cpts_list = ['Val d Orge', 'PEPS', 'Val d Essonne et des 2 Vallées',
       'C\x9cur Santé Orge Yvette', 'Sud Hurepoix', 'Val d Yvette',
       'Centre Essonne', 'Nord Essonne - Hygie', 'Noé Santé',
       'Santé Seine Essonne', 'C\x9cur Essonne', 'Val d Yerres',
       'Val de Seine', 'Sans Cpts']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([html.H1("Tableau de suivi CPTS"),
    html.Div([
        
        dcc.Graph(id="cpts-map1"),
        
        dcc.Graph(id="cpts-map2"),
        
        
    ],className='four columns', style={"height": "80%", "width": "20%"}),
    
    html.Div([
        html.P("Sélectionnez une CPTS:"),
        dcc.Dropdown(
                        id='cpts1',
                        value='Toutes',
                        clearable=True,
                        options=[
                            {'label': name, 'value': name}
                            for name in cpts_list]),
        
        dcc.Graph(id="cpts-chart1"),
        html.P("Sélectionnez une CPTS:"),
        dcc.Dropdown(
                        id='cpts2',
                        value='Toutes',
                        clearable=True,
                        options=[
                            {'label': name, 'value': name}
                            for name in cpts_list]),
        
        dcc.Graph(id="cpts-chart2"), 

    ],className='six columns', style={"height": "80%", "width": "60%"})
    
                        ], className='row')


# update bar chart #1
@app.callback(
    Output('cpts-chart1','figure'),
    Input("cpts1",'value'),
)
def update_bar_chart(c1):
    
    mask = essonne["cpts"] == c1
    dff = essonne[mask]
    dff = essonne[mask]
    dff = dff.groupby("cpts").sum().reset_index()
    dff.drop(["cpts" , "essonne" , "id", "cpts_code"], axis = 1 , inplace = True)
    dff = dff.T.reset_index()
    dff.columns = ["cpts", c1]
    bar=px.bar(dff, y='cpts', x=c1, color = "cpts", orientation='h')
    bar.update_xaxes(showline=True, linewidth=2, linecolor='black')
    bar.update_yaxes(showline=True, linewidth=2, linecolor='black', color='crimson',title_text='Indicateurs')
    bar.update_xaxes(range=[0, 200])
    bar.update_layout(showlegend=False)

    return bar

# update bar chart #2
@app.callback(
    Output('cpts-chart2','figure'),
    Input("cpts2",'value'),
)
def update_bar_chart(c2):

    mask = essonne["cpts"] == c2
    dff = essonne[mask]
    dff = essonne[mask]
    dff = dff.groupby("cpts").sum().reset_index()
    dff.drop(["cpts" , "essonne" , "id", "cpts_code"], axis = 1 , inplace = True)
    dff = dff.T.reset_index()
    dff.columns = ["cpts", c2]
    bar2=px.bar(dff, y='cpts', x=c2, color = "cpts", orientation='h')
    bar2.update_xaxes(showline=True, linewidth=2, linecolor='black')
    bar2.update_yaxes(showline=True, linewidth=2, linecolor='black', color='crimson',title_text='Indicateurs')
    bar2.update_xaxes(range=[0, 200])
    bar2.update_layout(showlegend=False)
    
    return bar2

# Update map

@app.callback(
    Output('cpts-map1','figure'),
    Input("cpts1",'value'),
)
def update_map_chart(m1):
    if m1 == "Toutes" : 
        fig = px.choropleth(essonne, geojson=essonne_geo, locations = "id", color = "cpts_code",
                        featureidkey="properties.code",
                        projection="mercator",hover_data=["nom", "cpts"] )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(showlegend=False)
        fig.update_coloraxes(showscale=False)
    
        return fig
    
    else :
        focus = essonne.copy()
        focus.loc[focus["cpts"]!= m1, "cpts_code"] = 99
        focus["cpts_code"] = focus["cpts_code"].astype("int")
        focus.sort_values("cpts_code", inplace = True, ascending = False )
        focus["cpts_code"] = focus["cpts_code"].astype("O")
        fig = px.choropleth(focus, geojson=essonne_geo, locations = "id", color = "cpts_code",
                    featureidkey="properties.code",                            
                    color_discrete_sequence=["white", "green"],
                    projection="mercator",hover_data=["nom", "cpts"]  )

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig.update_layout(showlegend=False)
        fig.update_coloraxes(showscale=False)
        return fig
    

# Update map02

@app.callback(
    Output('cpts-map2','figure'),
    Input("cpts2",'value'),
)
def update_map_chart(m2):
    if m2 == "Toutes" : 
        map2 = px.choropleth(essonne, geojson=essonne_geo, locations = "id", color = "cpts_code",
                featureidkey="properties.code",
            
                projection="mercator",hover_data=["nom", "cpts"] )

        map2.update_geos(fitbounds="locations", visible=False)
        map2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        map2.update_layout(showlegend=False)
        map2.update_coloraxes(showscale=False)
    
        return map2
    
    else :
        focus = essonne.copy()
        focus.loc[focus["cpts"]!= m2, "cpts_code"] = 99
        focus["cpts_code"] = focus["cpts_code"].astype("int")
        focus.sort_values("cpts_code", inplace = True, ascending = False )
        focus["cpts_code"] = focus["cpts_code"].astype("O")
        map2 = px.choropleth(focus, geojson=essonne_geo, locations = "id", color = "cpts_code",
                    featureidkey="properties.code", 
                    color_discrete_sequence=["white", "green"],
                    projection="mercator",hover_data=["nom", "cpts"]  )

        map2.update_geos(fitbounds="locations", visible=False)
        map2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        map2.update_layout(showlegend=False)
        map2.update_coloraxes(showscale=False)
        return map2



if __name__ == '__main__':
    app.run_server(debug=True)
