import dash
from dash import html
from dash import dcc
from dash import Input
from dash import Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px


from app import app

covid = pd.read_csv('https://raw.githubusercontent.com/shaqmck/DataVisCA2smk/main/covid_data.csv')
covid1 =covid
covid1['date'] = pd.to_datetime(covid1['date'])
#covid['month_year'] = pd.to_datetime(covid['month_year'],format='%Y-%m').dt.to_period('M') 

df1 = covid1[covid1['date'].dt.strftime('%Y-%m-%d') == '2022-05-09']
fig = px.scatter_geo(df1, locations="iso_code", color="continent",
                     hover_name="location", size="total_deaths",title="Total Covid-19 Deaths by April 2022",
                     projection="natural earth")
fig2 = px.line(covid, x="month_year", y="total_deaths", color="location",title = 'Total Amount of Covid-19 Deaths per Country', labels={
             "month_year": "Timeline",
             "total_cases": "Total Cases",
             "location": "Country"})
fig3 = px.line(covid, x="date", y="new_deaths", color="location",title = 'Total Amount of Covid-19 New Deaths per Day per Country', labels={
             "date": "Timeline",
             "new_cases": "New Deaths",
             "location": "Country"})


global_deaths = "{:,}".format(df1['total_deaths'].sum())


# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            dbc.Col(html.H1("Covid-19 Mortality Dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H2(children= "Global Deaths",  style={"textAlign" : "center", "color" : "black"})),
        ]),
        dbc.Row([
            dbc.Col(html.H2(global_deaths, style = {"textAlign" : "center", "color" : "black"})),
        ]),
        
    ]),
    html.Div(children=[
        dcc.Graph(id="deaths2022", figure = fig)
    ]),
    html.Div(children=[
        dcc.Graph(id="deathsline", figure = fig2),
        dcc.Checklist(id = 'Checklistd',options = covid.continent.unique())
    ]),
    html.Div(children=[
        dcc.Graph(id="deathlinenew", figure = fig3),
        dcc.Checklist(id = 'Checklistd2',options = covid.continent.unique())
    ]),
    
])


@app.callback(
    Output(component_id='deathsline', component_property='figure'),
    Input(component_id='Checklistd', component_property='value')
)
def update_line_chart(continents):
    df = covid
    mask = df.continent.isin(continents)
    fig = px.line(df[mask], x="month_year", y="total_cases", color="location")
    return fig

@app.callback(
    Output(component_id='deathlinenew', component_property='figure'),
    Input(component_id='Checklistd2', component_property='value')
)
def update_line_chart1(continents):
    df = covid
    mask = df.continent.isin(continents)
    fig = px.line(df[mask], x="date", y="new_deaths", color="location")
    return fig

