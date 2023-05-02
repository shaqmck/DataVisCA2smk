import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# needed only if running this as a single page app
#external_stylesheets = [dbc.themes.LUX]
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

from app import app

covid = pd.read_csv('https://raw.githubusercontent.com/shaqmck/DataVisCA2smk/main/covid_data.csv')
covid['date'] = pd.to_datetime(covid['date'])
covid['month_year'] = pd.to_datetime(covid['month_year'],format='%Y-%m').dt.to_period('M') 

df1 = covid[covid['date'].dt.strftime('%Y-%m-%d') == '2022-05-09']
fig = px.scatter_geo(df1, locations="iso_code", color="continent",
                     hover_name="location", size="total_cases",title="Total Covid-19 Cases by April 2022",
                     projection="natural earth")
fig1 = px.scatter_geo(df1, locations="iso_code", color="continent",
                     hover_name="location", size='total_deaths',title="Total Covid-19 Deaths by April 2022",
                     projection="natural earth")

global_cases = "{:,}".format(df1['total_cases'].sum())
global_deaths= "{:,}".format(df1['total_deaths'].sum())

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("Welcome to the CA2 Covid-19 Dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This app presents Covid-19 data from 2019 until April 2022'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='It consists of two main pages: Infections which details the amount of total and new cases across the world and Deaths- this page shows the amount of deaths caused by covid-19 across the world ')
                    , className="mb-5")
        ]),
        dbc.Row([
            dbc.Col(html.H2(children= "Global Cases",  style={"textAlign" : "left", "color" : "black"})),
            dbc.Col(html.H2(children= "Global Deaths",  style={"textAlign" : "right", "color" : "black"}))
        ]),
        dbc.Row([
            dbc.Col(html.H2(global_cases, style = {"textAlign" : "left", "color" : "black"})),
            dbc.Col(html.H2(global_deaths, style = {"textAlign" : "right", "color" : "black"}))
        ]),
        
    ]),
    html.Div(children=[
        dcc.Graph(id="inf2022", figure = fig, className="six columns", style={"width":950, "margin": 0, 'display': 'inline-block'}),
        dcc.Graph(id="death2022", figure = fig1, className="six columns",style={"width":950, "margin": 0, 'display': 'inline-block'})
    ]),
])

# needed only if running this as a single page app
#if __name__ == '__main__':
#    app.run_server(port=8098,debug=True)
#HERE IS PLOT FOR MAIN  PAGE SHOWINGTOTAL CASES FOR 2022 / CURRENT DATA
