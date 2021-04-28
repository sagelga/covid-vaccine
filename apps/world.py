import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from plotly import graph_objects as go
from datetime import datetime, timedelta
import time

from app import app

# Data Import
url = 'https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv'
df = pd.read_csv(url)

# Data selection
df = df[['iso_code', 'continent', 'location', 'date', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths',
         'total_cases_per_million', 'new_cases_per_million', 'total_deaths_per_million', 'new_deaths_per_million',
         'icu_patients', 'icu_patients_per_million', 'hosp_patients', 'hosp_patients_per_million', 'new_tests',
         'total_tests', 'total_tests_per_thousand', 'new_tests_per_thousand', 'positive_rate', 'tests_per_case',
         'tests_units', 'total_vaccinations', 'people_vaccinated', 'people_fully_vaccinated', 'new_vaccinations',
         'stringency_index', 'population']]

# NA Data Drop
df = df.dropna(subset=[
    'date'
    , 'continent'
    , 'location'
])

# Data Transform
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['date', 'location'])
df['date_str'] = df['date'].dt.date.apply(lambda x: str(x))

# Calculate fields
df['people_vaccinated_per_population'] = 100 * (df['people_vaccinated'] / df['population'])
df['people_fully_vaccinated_per_population'] = 100 * (df['people_fully_vaccinated'] / df['population'])
df['case_per_population'] = 100 * (df['total_cases'] / df['population'])

# all_country = sorted(df["location"].unique())
all_country = df["location"].unique()

a = int((time.time() / 900 - 3) / 2 % 24)
curr_time = chr(128336 + a // 2 + a % 2 * 12)

# Website Builder
layout = html.Div([
    html.Div([
        html.H2('World Trends'),

        dcc.Graph(id='world-graph-choroplethview'),

        html.Div([
            html.Div(children=[
                html.Label('{} Time Range'.format(curr_time)),
                dcc.Dropdown(
                    id="world-dropdown-choroplethview-timerange",
                    options=[
                        {'label': 'All time', 'value': 'all'}
                        , {'label': '7 Days', 'value': '7'}
                        , {'label': '14 Days', 'value': '14'}
                        , {'label': '30 Days', 'value': '30'}
                        , {'label': '90 Days', 'value': '90'}
                        , {'label': '180 Days', 'value': '180'}
                        , {'label': '365 Days', 'value': '365'}
                    ]
                    , placeholder="Select a range"
                    , value='14'
                    , multi=False
                    , clearable=False
                    , searchable=False
                    , persistence=True
                    , persistence_type='session'
                ),
            ], className="three columns"),
        ], className='row'),
    ]),

    html.Br(),

    html.H2('Global Situation'),
    html.Div([
        html.Div([dcc.Graph()], className='six columns'),
        html.Div([dcc.Graph()], className='six columns'),
    ], className='row'),

    html.Br(),

    html.H3('Situation by Region'),
    dcc.Graph(),
    html.Div([
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
    ]),

    html.Br(),

    html.H3('Situation by Country'),
    html.Div([
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
        html.Div([dcc.Graph()], className='three columns'),
    ]),
])


@app.callback(
    Output("world-graph-choroplethview", "figure"),
    Input("world-dropdown-choroplethview-timerange", "value")
)
def sth(time_range):
    # - Time Range -
    time_max = datetime.today()
    time_list = []

    if time_range == 'all':
        time_range = time_max = timedelta(df['date'].min())

    for _ in range(1, int(time_range) + 1):
        time_check = time_max - timedelta(days=_)
        # if time_check in df['date']:
        time_check = time_check.strftime("%Y-%m-%d")
        time_list.append(time_check)

    # - Apply mask -
    mask = df['date'].isin(time_list)

    return px.choropleth(df[mask]
                         , locations="iso_code"
                         , color='case_per_population'
                         , hover_name="location"
                         , animation_frame="date_str"
                         , color_continuous_scale=px.colors.sequential.Viridis
                         , projection='kavrayskiy7'
                         )
