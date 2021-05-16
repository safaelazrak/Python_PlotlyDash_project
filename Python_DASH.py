from seaborn.palettes import color_palette
import dash as ds
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time

import plotly.io as pio

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = ds.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR],suppress_callback_exceptions = True,
 meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}])

df = pd.read_csv("https://raw.githubusercontent.com/charlesp1996/Pythonproject/main/for_appli2.csv")
geodata = {'type':'FeatureCollection', 'features': []}
sources = df.loc[:,["Production éolienne (GWh)", "Production solaire (GWh)","Vitesse du vent à 100m (m/s)", 
"Rayonnement solaire global (W/m2)"]]



SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": " #f8f9fa ",
}
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Dashboard", className="display-4", ),
        html.Hr(),
        html.P(
            "Feel free to navigate through all pages", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home page", href="/", active="exact"),
                dbc.NavLink("Energy Map", href="/page-0", active="exact"),
                dbc.NavLink("Energy production and consumption", href="/page-1", active="exact"),
                dbc.NavLink("Solar and wind power", href="/page-2", active="exact"),
                
                dbc.NavLink("Data sources", href="/page-3", active="exact")
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])

def render_page_content(pathname):
    if pathname == "/page-0":
        return [html.H1('Energy heat map', style={'textAlign':'center','font-weight':'bold', 'color':'white'}),

                html.Br(),
                html.Br(),
                
                dcc.Graph(id ='map-with-slider'
                
                ), 
                html.Br(),
                html.H3('Choose the data to display',style={'font-weight':'bold', 'color':'lightblue'}),
                 html.Br(),
                 dcc.Dropdown(
                id="choice",
                options=[{'label': i , 'value': i} for i in sources],
                value="Production éolienne (GWh)",
            
                ),
                 
                 html.Br(),
                 
                 
                 html.H3('Choose a year',style={'font-weight':'bold', 'color':'lightblue'}),
                 html.Br(),
                   dcc.Slider(
                id ='slct_year',
                min = df['Year'].min(), 
                max = df['Year'].max(),
                value = df['Year'].min(),
                marks = {str(year) : str(year) for year in df['Year'].unique()},
                step = None),
html.Br(),
                 html.Br()
                 
       
]
    elif pathname == "/":
        return [
        html.Div(children=[
        html.H1('Renewable Energy in France',style={'textAlign':'center', 'font-weight':'bold', 'color':'white'}),
        html.Br(),
        html.Br(),
        html.H2("Renewable energy sources impressively expand around us, but do these energies provide important part of production? ",style={'textAlign':'center'}),
        html.H2("Are natural resources used effectively?",style={'textAlign':'center'}),
        html.Br(),
        html.H2("We explored wind and solar energy production in France for 2014 - 2020 in order to answer these questions.",style={'textAlign':'center'}),
        html.Br(),
        html.Div(children= html.Img(
            src="https://media.istockphoto.com/photos/solar-power-plant-picture-id584487610?k=6&m=584487610&s=612x612&w=0&h=W3RPC3JBcOl9F-JS7cdunQDTRAz4eapacLSbLxVlZJI=",
            style={'width': 900,'height': 900 }),
        style={'textAlign': 'center'})
        ])]
      
    elif pathname == "/page-2":
        return [html.H1('Load factors compared to weather', style={'textAlign':'center', 'font-weight':'bold', 'color':'white'}),
         html.Br(),
                html.H2('Wind power', style={'textAlign':'center'}),
                html.Br(),
                dcc.Graph(id ='graph2'), 
                html.Br(),
                html.H3('Choose a year',style={'font-weight':'bold', 'color':'lightblue'}),
                
               dcc.Slider(
                id ='slct_year3',
                min = 2016, 
                max = df['Year'].max(),
                value = 2016,
                marks = {str(year) : str(year) for year in df['Year'].unique()},
                step = None),
html.Br(),
 html.H2('Solar energy', style={'textAlign':'center'}),
 html.Br(),
                dcc.Graph(id ='graph6')
               
               
      
]
    elif pathname == "/page-1":
        return [html.H1('Energy production and consumption by region', style={'textAlign':'center', 'font-weight':'bold', 'color':'white'}),

                html.Br(),
               # dcc.Graph(id ='graph4'), 
                html.Br(),
               

               
               dcc.Graph(id ='graph5'),
                html.Br(),
                
                html.H3('Choose a year',style={'font-weight':'bold', 'color':'lightblue'}),
                dcc.Slider(
                id ='slct_year2',
                min = df['Year'].min(), 
                max = df['Year'].max(),
                value = df['Year'].min(),
                marks = {str(year) : str(year) for year in df['Year'].unique()},
                step = None),
                  html.Br(),
 html.H2('Comparison of load factors', style={'textAlign':'center', 'font-weight':'bold', 'color':'white'}),
 html.Br(),
                dcc.Graph(id ='graph4')
                
        ]
    elif pathname == "/page-3":
        return [html.H1('Data sources used for the analysis', style={'textAlign':'center', 'font-weight':'bold', 'color':'white'}),
        html.Br(),
        html.H2('Open Data - Réseaux Energies:',style={'textAlign':'center'}),
        html.Br(),
       
    dbc.Alert([html.A('https://opendata.reseaux-energies.fr/explore/dataset/parc-regional-annuel-prod-eolien-solaire/information/?disjunctive.region',href="#", className="alert-link")],color="light"),
    dbc.Alert([html.A('https://opendata.reseaux-energies.fr/explore/dataset/production-regionale-mensuelle-filiere/export/?disjunctive.region',href="#", className="alert-link")],color="light"),
    dbc.Alert([html.A('https://opendata.reseaux-energies.fr/explore/dataset/equilibre-regional-mensuel-prod-conso-brute/information/?disjunctive.region',href="#", className="alert-link")],color="light"),
    dbc.Alert([html.A('https://opendata.reseaux-energies.fr/explore/dataset/fc-tc-regionaux-mensuels-enr/information/?disjunctive.region',href="#", className="alert-link")],color="light"),
    dbc.Alert([html.A('https://opendata.reseaux-energies.fr/explore/dataset/rayonnement-solaire-vitesse-vent-tri-horaires-regionaux/information/?disjunctive.region',href="#", className="alert-link")],color="light"),
                    html.Br(),
    html.Br(),
          html.Br(),
                    html.H2('Who made this Dash ? ',style={'textAlign':'center', 'font-weight':'bold', 'color':'white'}) ,
                    html.Br(),
   
            html.H3("Students in Msc Data Analytics at the Data Science Tech Institute",style={'textAlign':'center'}),
            html.Br(),
        
            html.H4("Safa EL AZRAK   -   Charles POULLE   -    Ekaterina MAZANCHENKO",style={'textAlign':'center', 'font-weight':'bold', 'color':'lightblue'}),
        
    
        ]
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )



@app.callback(
    Output('map-with-slider', 'figure'),
    [Input('choice','value'),
    Input('slct_year', 'value')]
)

def update_figure(choice, slct_year):
    filtered_df = df[df["Year"] == slct_year]

    for row in filtered_df.itertuples():
        region_code = row[2]
        coord = eval(row[13])
        temp_d = {}
        temp_d['type'] = 'Feature'
        temp_d['geometry'] = coord
        temp_d['id'] = region_code
        geodata['features'].append(temp_d)

    fig = px.choropleth_mapbox(filtered_df, geojson = geodata, 
                               locations = 'Région', color = filtered_df[choice],
                               color_continuous_scale = "Blues", 
                               mapbox_style = "carto-positron",
                               zoom = 5, center = {"lat": 47, "lon": 1.7},opacity = 0.5)
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
       
    return fig

@app.callback(
    Output('graph2', 'figure'),
    [Input('slct_year3', 'value')]
)   

def update_figure(slct_year3):
    dff = df[df["Year"] == slct_year3]

    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig2=px.bar(dff, x="Région", y="Vitesse du vent à 100m (m/s)",labels = {"value": "W/m2", "variable": ""},color_discrete_map = {"Vitesse du vent à 100m (m/s)": "Mint"})
    fig2.update_traces(marker_color='lightblue')
    fig2.update_traces(yaxis = "y2")
    fig3=px.bar(dff, x="Région", y="FC moyen mensuel éolien",labels = {"value": "%", "variable": ""})
    
    subfig.add_traces(fig2.data + fig3.data)
    subfig.layout.xaxis.title = "Région"
    subfig.layout.yaxis2.title = "Vitesse du vent à 100m (m/s)"
    subfig.layout.yaxis.title = "FC, %"
    subfig.update_layout(template='simple_white')
    
    return subfig



@app.callback(
    Output('graph4', 'figure'),
    [Input('slct_year2', 'value')]
)   

def update_figure(slct_year2):
    dff = df[df["Year"] == slct_year2]

    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig2=px.bar(dff, x="Région", y="FC moyen mensuel solaire")
    fig2.update_traces(marker_color='lightblue')
    fig3 = px.bar(dff, x='Région', y= "FC moyen mensuel éolien")
    subfig.add_traces(fig2.data + fig3.data)
    subfig.layout.yaxis.title = "FC, %"
    subfig.layout.xaxis.title = "Région"
    subfig.update_layout(template='simple_white')
    return subfig

@app.callback(
    Output('graph5', 'figure'),
    [Input('slct_year2', 'value')]
)   

def update_figure(slct_year2):
    dff = df[df["Year"] == slct_year2]

    subfig = make_subplots(specs=[[{"secondary_y": True}]])
    fig2=px.bar(dff, x="Région", y="Production totale (MWh)")
    fig2.update_traces(marker_color='lightblue')
    fig3 = px.bar(dff, x='Région', y= "Consommation brute (MWh)")
    subfig.add_traces(fig2.data + fig3.data)
    subfig.layout.yaxis.title = "MWh"
    subfig.layout.xaxis.title = "Région"
    subfig.update_layout(template='simple_white')
    return subfig

@app.callback(
    Output('graph6', 'figure'),
    [Input('slct_year3', 'value')]
)   

def update_figure(slct_year3):
    dff = df[df["Year"] == slct_year3]

    subfig = make_subplots(specs=[[{"secondary_y": True}]],shared_xaxes=True)
    fig2=px.bar(dff, x="Région", y="FC moyen mensuel solaire",labels = {"value": "%", "variable": ""})
    fig2.update_traces(yaxis = "y2")
    fig2.update_traces(marker_color='lightblue')
    fig3 = px.bar(dff, x='Région', y= "Rayonnement solaire global (W/m2)",labels = {"value": "W/m2", "variable": ""})
    

    subfig.add_traces(fig2.data + fig3.data)
    subfig.layout.xaxis.title = "Région"
    subfig.layout.yaxis2.title = "FC, %"
    subfig.layout.yaxis.title = "Rayonnement solaire global (W/m2)"
    subfig.update_layout(template='simple_white')
    return subfig



if __name__ == '__main__':
    app.run_server(debug=True)