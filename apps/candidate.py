import pandas as pd
import numpy as np
import dash
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_core_components as dcc
import dash_html_components as html
from plotly import express as px
from plotly import graph_objects as go
from datetime import datetime, timedelta
import time

from app import app

# Data Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-primary.csv'
df = pd.read_csv(url)

# Select data
df = df[['Buyer/recipient', 'Vaccine candidate', 'Deal Type', 'Finalized Commitment', 'Doses committed (in millions)',
         'Price (in USD million)', 'Price/Dose (in USD)', 'Doses/capita', 'Population covered']]
df = df.dropna()

# Sort data using Buyer + Vaccine candidate
df = df.sort_values(by=['Buyer/recipient', 'Vaccine candidate'])

all_buyer = df['Buyer/recipient'].unique()
# all_candidates = df['Vaccine candidate'].unique()
price_options = [
    {'label': 'Vaccine Name', 'value': 'name'}
    , {'label': 'Vaccine Price', 'value': 'price'}
]

# Vaccine Provider Card Import
url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-vaccineProvider.csv'
vp_df = pd.read_csv(url)


# Secondary Trade Data Import
# url = 'https://raw.githubusercontent.com/sagelga/covid-vaccine/main/data/knowledgeportalia-secondary.csv'
# l2_df = pd.read_csv(url)


def generate_dropdown_option(label, id, options, value, placeholder='Select the option ...', multi=False):
    layout = html.Div([
        html.Label(label),
        dcc.Dropdown(
            id=id
            , options=options
            , value=value
            , placeholder=placeholder
            , multi=multi, clearable=multi
            , searchable=False
            , persistence=True, persistence_type='session'
        )
    ])

    return layout


def generate_candidateinfo_card():
    vaccine_candidate = vp_df['Vaccine candidate'].tolist()
    location = vp_df['Developer Location'].tolist()
    phase = vp_df['Trial Phase'].tolist()
    doses = vp_df['Doses'].tolist()

    layout = []
    for x in range(len(vaccine_candidate)):
        graphid = "candidate-graph-candidateinfo-{}".format(x)

        layout.append(html.Div([dcc.Graph(id=graphid)], className="six columns"))
        layout.append(html.Div([
            html.H5(vaccine_candidate[x])
            , html.Li("Developer Location : {}".format(location[x]))
            , html.Li("Development Phase : {}".format(phase[x]))
            , html.Li("Dose(s) required : {}".format(doses[x]))
        ], className="six columns"))

    layout2 = []
    loop_count = len(layout) // 2
    for x in range(loop_count):
        pointer = x * 2
        layout2.append(html.Div(children=[layout[pointer], layout[pointer + 1]], className='six columns'))

    layout3 = []
    loop_count = len(layout2) // 2
    for x in range(loop_count):
        pointer = x * 2
        layout3.append(html.Div(children=[layout2[pointer], layout2[pointer + 1]], className='row'))

    if len(layout2) % 2:
        layout3.append(html.Div(children=[layout2[-1]], className='row'))

    return html.Div(layout3)


# Website Builder
layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H2('Vaccine on Hand'),
            ], className='ten columns'),
            html.Div([
                html.Button(children='Switch to ... mode', id='candidate-button-chartoption-buyer', n_clicks=0),
            ], className='two columns'),
        ], className='row'),

        html.Div([
            generate_dropdown_option(label='📊 Vaccine Buyer', id='candidate-dropdown-chartoption-buyer',
                                     options=[{'label': x, 'value': x} for x in all_buyer],
                                     value=all_buyer,
                                     placeholder='Filter by Buyer'
                                     , multi=True),
            # html.Button('Reset', id='candidate-button-chartoption-buyer', n_clicks=0),
        ]),

        html.Div(children=[
            dcc.Graph(id="candidate-graph-vaccinecount")
        ], className="twelve columns"),
    ]),  # Vaccine on Hand

    html.Div([
        html.H2('Vaccine Price'),
        html.P('DISCLAIMER : Only showing Public prices. Any private Private price deals are excluded.'),
        html.Div([
            html.Div([], className='ten columns'),
            html.Div([
                generate_dropdown_option(label='Order by'
                                         , id='candidate-dropdown-priceoption-category'
                                         , options=price_options
                                         , value='name'
                                         , placeholder='Order by ...'
                                         , multi=False),
                generate_dropdown_option(label='Order by'
                                         , id='candidate-dropdown-priceoption-order'
                                         , options=[{'label': 'Ascending', 'value': 'asc'},
                                                    {'label': 'Descending', 'value': 'desc'}]
                                         , value='asc'
                                         , placeholder='Order by ...'
                                         , multi=False),
            ], className='two columns'),
        ], className='row'),

        html.Div(children=[
            dcc.Graph(id="candidate-graph-price")
        ], className="twelve columns"),

    ]),  # Vaccine Price

    html.Div([
        html.H2('Insights'),

        html.Div(children=[
            dcc.Graph(id="company-insight-dashboard")
        ], className="twelve columns"),

    ]),  # Insights

    html.Div([
        html.H2('About each Vaccine'),
        html.P(
            'DISCLAIMER : This information listed here might be outdated. Please trust a latest information from reliable source.'),
        html.Br(),

        html.Div(children=[
            html.Div(children=[
                html.H4('Showing x of x available candidates'
                        # , id=''
                        )
            ], className='eight columns'),

            html.Div(children=[
                generate_dropdown_option(label='Filter by'
                                         , id='candidate-dropdown-candidateinfo-filter'
                                         , options=[]
                                         , value=[]
                                         , placeholder='Filter by ...'
                                         , multi=True)
            ], className='two columns'),
            html.Div(children=[
                generate_dropdown_option(label='Order by'
                                         , id='candidate-dropdown-candidateinfo-order'
                                         , options=[]
                                         , value=[]
                                         , placeholder='Order by ...'
                                         , multi=True)
            ], className='two columns'),
        ], className='row'),

        html.Br(),

        html.Div(children=[
            generate_candidateinfo_card()
        ]),
    ]),  # Vaccine Info Card

])


@app.callback(
    Output("candidate-graph-vaccinecount", "figure"),
    Input("candidate-dropdown-chartoption-buyer", "value")
)
def candidate_graph_vaccinecount(buyer):
    mask = df['Buyer/recipient'].isin(buyer)

    fig = px.bar(df[mask], x="Buyer/recipient", y="Doses committed (in millions)", color="Vaccine candidate")
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return fig


@app.callback(
    Output("candidate-graph-price", "figure"),
    [Input("candidate-dropdown-priceoption-category", "value")
        , Input("candidate-dropdown-priceoption-order", "value")]
)
def candidate_graph_vaccineprice(order_category, order):
    fig = px.box(df, x='Vaccine candidate', y='Price/Dose (in USD)')
    return fig
# @app.callback(
#     Output("candidate-heading-candidateinfo-cards", "children")
#     [
#         Input('candidate-dropdown-candidateinfo-filter', 'value')
#         , Input("candidate-dropdown-candidateinfo-ordercategory", "value")
#         , Input("candidate-dropdown-candidateinfo-order", "value")
#     ]
# )
# def candidate_candidateinfo_(filter,order_category, order):
#     return True
