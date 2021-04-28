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


def get_aapl_df():
    url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/apple_reports/apple_mobility_report.csv'
    df = pd.read_csv(url)
    return df


def get_goog_df():
    url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/google_reports/mobility_report_countries.csv'
    df = pd.read_csv(url)
    return df


def get_waze_df():
    url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/waze_reports/waze_mobility.csv'
    df = pd.read_csv(url)
    return df


def get_tom_df():
    url = 'https://raw.githubusercontent.com/ActiveConclusion/COVID19_mobility/master/tomtom_reports/tomtom_trafic_index.csv'
    df = pd.read_csv(url)
    return df


layout = html.Div([
    html.Div([
        html.H2('Mobility Report'),
        html.P('Data from Apple. Report reflects requests for directions in Apple Maps.')
    ])
])
