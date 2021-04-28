import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, ALL, MATCH
from dash.exceptions import PreventUpdate
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

# Calculate fields
df['people_vaccinated_per_population'] = 100 * (df['people_vaccinated'] / df['population'])
df['people_fully_vaccinated_per_population'] = 100 * (df['people_fully_vaccinated'] / df['population'])
df['lethal_rate'] = 100 * (df['total_deaths'] / df['total_cases'])

# all_country = sorted(df["location"].unique())
all_country = np.sort(df["location"].unique())

a = int((time.time() / 900 - 3) / 2 % 24)
curr_time = chr(128336 + a // 2 + a % 2 * 12)

# Reused Components
option_case_type = [
    {'label': 'New confirmed cases', 'value': 'new_cases'}
    , {'label': 'New deaths attributed', 'value': 'new_deaths'}
    , {'label': 'Total confirmed cases', 'value': 'total_cases'}
    , {'label': 'Total deaths attributed', 'value': 'total_deaths'}
    , {'label': 'Lethality Rate', 'value': 'lethal_rate'}
    , {'label': 'Vaccinated one dose', 'value': 'people_vaccinated'}
    , {'label': 'Vaccinated all doses', 'value': 'people_fully_vaccinated'}
    , {'label': 'Patient in Hospital', 'value': 'hosp_patients'}
    , {'label': 'Patient in ICU', 'value': 'icu_patients'}
    , {'label': 'Government Response Stringency Index', 'value': 'stringency_index'}
    , {'label': 'Total confirmed cases per million people', 'value': 'total_cases_per_million'}
    , {'label': 'Total deaths per million people', 'value': 'total_deaths_per_million'}
    , {'label': 'Vaccinated one dose per population', 'value': 'people_vaccinated_per_population'}
    , {'label': 'Vaccinated all doses per population', 'value': 'people_fully_vaccinated_per_population'}
]

# Website Builder
layout = html.Div([
    html.Div(children=[
        html.H2('Explore'),
        html.P('Select indicators from the dropdown menu.')
    ]),
    # Options
    html.Div(children=[
        html.Div(children=[
            html.Label('🌎 Countries'),
            dcc.Dropdown(
                id="home-dropdown-country"
                , options=[{"label": x, "value": x}
                           for x in all_country]
                , placeholder="Select a country"
                , value=['Thailand']
                , multi=True
                , clearable=True
                , searchable=True
                , persistence=True
                , persistence_type='session'
            ),
        ], className="nine columns"),

        html.Div(children=[
            html.Label('📂 Case Type'),
            dcc.Dropdown(
                id="home-dropdown-casetype"
                , options=option_case_type
                , placeholder="Select a type of case"
                , value='new_cases'
                , multi=False
                , clearable=False
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className="three columns"),
    ], className="row"),

    html.Br(),

    html.Div(children=[
        html.Div(children=[
            html.Label('📊 Chart Type'),
            dcc.Dropdown(
                id="home-dropdown-charttype"
                , options=[
                    {'label': '📈 Line Chart', 'value': 'line'}
                    , {'label': '📊 Scatter Plot', 'value': 'scatter'}
                    , {'label': '📊 Stacked Bar Chart', 'value': 'bar'}
                    , {'label': '📈 Stacked Area Chart', 'value': 'area'}
                ]
                , placeholder="Select a data source"
                , value='line'
                , multi=False
                , clearable=False
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className="three columns"),

        html.Div(children=[
            html.Label(curr_time + ' Time Range'),
            dcc.Dropdown(
                id="home-dropdown-timerange",
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

        html.Div(children=[
            html.Label('📊 Chart Indicators'),
            dcc.Dropdown(
                id="home-dropdown-chartindicator"
                , options=[
                    {'label': 'Highest Threshold', 'value': 'max'}
                    , {'label': 'Average Threshold', 'value': 'avg'}
                    , {'label': 'Lowest Threshold', 'value': 'min'}
                ]
                , placeholder="Select an option (optional)"
                , multi=True
                , clearable=True
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className='three columns'),

        html.Div(children=[
            html.Label('📊 Regression Line'),
            dcc.Dropdown(
                id="home-dropdown-chartregressionline"
                , options=[
                    {'label': 'Linear Regression Trend Line', 'value': 'linear'}
                    , {'label': 'Log-linear Trend Line', 'value': 'log_linear'}
                ]
                , placeholder="Select an option (optional)"
                , disabled=True
                , multi=True
                , clearable=True
                , searchable=False
                , persistence=True
                , persistence_type='session'
            ),
        ], className='three columns'),
    ], className='row'),

    html.Br(),

    # Chart
    html.Div(children=[
        dcc.Graph(id="home-result-chart")
    ], className="twelve columns"),

    html.Br(),

    html.H2('Statistics'),

    html.Div(children=[
        html.Label('🌎 Countries'),
        dcc.Dropdown(
            id="home-dropdown-stats-country"
            , options=[{"label": x, "value": x}
                       for x in all_country]
            , placeholder="Select a country"
            , multi=True
            , clearable=True
            , searchable=True
            , persistence=True
            , persistence_type='session'
        ),
    ]),

    html.Br(),

    html.Div(id='home-overall-card', children=[]),

])


@app.callback(
    Output("home-result-chart", "figure"),
    [
        Input("home-dropdown-country", "value")
        , Input("home-dropdown-casetype", "value")
        , Input("home-dropdown-charttype", "value")
        , Input("home-dropdown-timerange", "value")
        , Input("home-dropdown-chartindicator", "value")
    ]
)
def update_graph(countries, case_type, chart_type, time_range, chart_indicator):
    # - Check a required column
    if not len(countries):
        return go.Figure(go.Indicator(
            mode="number", value=400,
            title={
                "text": "Bad Request<br><span style='font-size:0.8em;color:gray'>Please select <b>at least one</b> country to continue</span>"},
            domain={'y': [0, 1], 'x': [0.25, 0.75]}))

    # - Time Range -
    time_list = []
    if time_range != 'all':
        for _ in range(1, int(time_range) + 1):
            time_check = (datetime.today() - timedelta(days=_)).strftime("%Y-%m-%d")
            time_list.append(time_check)
        mask = df['location'].isin(countries) & df['date'].isin(time_list)
    else:
        mask = df['location'].isin(countries)
        time_list = df['date'].unique().tolist()

    # - Chart Type -
    if chart_type == "area":  # Line Chart
        fig = px.area(df[mask]
                      , x="date"
                      , y=case_type
                      , color="location"
                      , hover_name="location"
                      , hover_data=[case_type]
                      )
        fig.update_traces(connectgaps=True
                          , mode="markers+lines"
                          , hovertemplate=None)
        fig.update_layout(hovermode="x unified")

    elif chart_type == "bar":  # Bar Chart
        fig = px.bar(df[mask]
                     , x="date"
                     , y=case_type
                     , color="location"
                     , hover_data=[case_type]
                     , barmode="stack"
                     )

    elif chart_type == "scatter":
        fig = px.scatter(df[mask]
                         , x="date"
                         , y=case_type
                         , color="location"
                         )
    else:
        fig = px.line(df[mask]
                      , x="date"
                      , y=case_type
                      , color="location"
                      , hover_data=[case_type]
                      )
        fig.update_traces(connectgaps=True)

    # Add chart templates + layouts
    fig.update_traces(hovertemplate=None)
    fig.update_layout(title=generate_title(countries, case_type)
                      , xaxis_title="Date"
                      , yaxis_title=get_casetype(case_type)
                      , hovermode="x")

    # - Chart Indicator -
    if type(chart_indicator) == list:
        if 'max' in chart_indicator:  # Max Line
            y = df[mask][case_type].max()
            fig.add_shape(
                type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y"
            )

        if 'avg' in chart_indicator:  # Average Line
            # y = (df[mask][case_type].sum()) / len(time_list)
            y = (df[mask][case_type]).mean()
            fig.add_shape(
                type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y"
            )

        if 'min' in chart_indicator:  # Min Line
            y = df[mask][case_type].min()
            fig.add_shape(
                type="line", line_color="salmon", line_width=3, opacity=1, line_dash="dot",
                x0=0, x1=1, xref="paper", y0=y, y1=y, yref="y"
            )

    return fig


@app.callback(
    Output('home-overall-card', "children"),
    [Input("home-dropdown-stats-country", "value")]
)
def template_overall_card(country):
    if not country:
        raise PreventUpdate

    new_children = []
    for country_name in country:
        children = html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H5(country_name),
                    ], className='nine columns'),

                    html.Div([
                        dcc.Dropdown(
                            id={"type": "home-dropdown-statistics-option", 'index': country_name}
                            , options=[
                                {'label': 'by Population', 'value': 'population'}
                            ]
                            , placeholder="Select an option..."
                            , multi=False
                            , searchable=False
                            , persistence=True
                            , persistence_type='session'
                        ),
                    ], className='three columns'),
                ], className='row'),

                html.Div([
                    html.Div([
                        html.P('New Case'),
                        html.Div(id={'type': 'label-new_cases', 'index': country_name}),
                        dcc.Graph(id={'type': 'new_cases', 'index': country_name}),

                        html.P('Total Case'),
                        html.Div(id={'type': 'label-total_cases', 'index': country_name}),
                        dcc.Graph(id={'type': 'total_cases', 'index': country_name}),

                    ], className='three columns'),
                    html.Div([
                        html.P('New Deaths'),
                        html.Div(id={'type': 'label-new_deaths', 'index': country_name}),
                        dcc.Graph(id={'type': 'new_deaths', 'index': country_name}),

                        html.P('Total Deaths'),
                        html.Div(id={'type': 'label-total_deaths', 'index': country_name}),
                        dcc.Graph(id={'type': 'total_deaths', 'index': country_name}),
                    ], className='three columns'),
                    html.Div([
                        html.P('New Dose Administered'),
                        html.Div(id={'type': 'label-new_vaccinations', 'index': country_name}),
                        dcc.Graph(id={'type': 'new_vaccinations', 'index': country_name}),

                        html.P('Total Dose Administered'),
                        html.Div(id={'type': 'label-total_vaccinations', 'index': country_name}),
                        dcc.Graph(id={'type': 'total_vaccinations', 'index': country_name}),
                    ], className='three columns'),
                    html.Div([
                        html.P('New People Vaccinated'),
                        html.Div(id={'type': 'label-people_vaccinated', 'index': country_name}),
                        dcc.Graph(id={'type': 'people_vaccinated', 'index': country_name}),

                        html.P('Total People Vaccinated'),
                        html.Div(id={'type': 'label-people_fully_vaccinated', 'index': country_name}),
                        dcc.Graph(id={'type': 'people_fully_vaccinated', 'index': country_name}),
                    ], className='three columns'),
                ], className='row'),

            ], style={'border-radius': '10px', 'border': '2px solid #3d4e76', 'padding': '20px'}),
            html.Br(),
        ])

        new_children.append(children)

    return new_children


@app.callback(
    Output({'index': MATCH, 'type': 'label-new_cases'}, "children"),
    Output({'index': MATCH, 'type': 'new_cases'}, "figure"),
    Output({'index': MATCH, 'type': 'label-new_deaths'}, "children"),
    Output({'index': MATCH, 'type': 'new_deaths'}, "figure"),
    Output({'index': MATCH, 'type': 'label-new_vaccinations'}, "children"),
    Output({'index': MATCH, 'type': 'new_vaccinations'}, "figure"),
    Output({'index': MATCH, 'type': 'label-total_cases'}, "children"),
    Output({'index': MATCH, 'type': 'total_cases'}, "figure"),
    Output({'index': MATCH, 'type': 'label-total_deaths'}, "children"),
    Output({'index': MATCH, 'type': 'total_deaths'}, "figure"),
    Output({'index': MATCH, 'type': 'label-total_vaccinations'}, "children"),
    Output({'index': MATCH, 'type': 'total_vaccinations'}, "figure"),
    Output({'index': MATCH, 'type': 'label-people_vaccinated'}, "children"),
    Output({'index': MATCH, 'type': 'people_vaccinated'}, "figure"),
    Output({'index': MATCH, 'type': 'label-people_fully_vaccinated'}, "children"),
    Output({'index': MATCH, 'type': 'people_fully_vaccinated'}, "figure"),
    [Input({'index': MATCH, 'type': 'home-dropdown-statistics-option'}, "value")
        , State({'index': MATCH, 'type': 'home-dropdown-statistics-option'}, "id")]
)
def update_overall_card(stats_option, id):
    # Compute the values by pulling data from DF
    def get_value(type):
        ddf = df[['date', 'location', x]]
        ddf = ddf.dropna(subset=[x])
        ddf = ddf.loc[ddf['location'] == id['index']]
        ddf = ddf.loc[ddf['date'] == ddf['date'].max()]
        try:
            value = ddf.iloc[0][x]
        except IndexError:
            value = np.nan
        try:
            time = "(on {})".format(ddf.iloc[0]['date'].strftime('%d %b %Y'))
        except IndexError:
            time = 'N/A'

        return {'time': time, 'value': value}

    def update_layout(layout):
        return layout.update_layout(autosize=False, height=200, margin={'l': 20, 'r': 20, 't': 20, 'b': 20},
                                    font={'size': 12})

    figure = []

    figure_options = ['new_cases', 'new_deaths', 'new_vaccinations', 'total_cases', 'total_deaths',
                      'total_vaccinations', 'people_vaccinated',
                      'people_fully_vaccinated']
    for x in figure_options:
        query = get_value(x)

        new_label = html.Label('{}'.format(query['time']))

        new_figure = go.Figure(go.Indicator(
            mode="number", value=query['value'],
            delta={"reference": 512, "valueformat": ".0f"},
            domain={'x': [0, 1], 'y': [0, 1]}))

        new_figure = update_layout(new_figure)

        figure.append(new_label)
        figure.append(new_figure)

    return figure[0], figure[1], figure[2], figure[3], figure[4], figure[5], figure[6], figure[7], figure[8], \
           figure[9], figure[10], figure[11], figure[12], figure[13], figure[14], figure[15]


def generate_title(countries, case_type):
    # Case type search
    case_type = get_casetype(case_type)

    # Country list builder
    if len(countries) < 3:
        title_country = ' and '.join([str(_) for _ in countries])
    else:
        title_country = str(len(countries)) + " selected countries"

    return "{} in {}".format(case_type, title_country)


def get_casetype(case_type):
    return next((item['label'] for item in option_case_type if item["value"] == case_type), case_type)
