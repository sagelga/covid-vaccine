import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from app import server

# Connect to your app pages
from apps import home
from apps import world
from apps import candidate
from apps import mobility

# Website Builder
app.layout = html.Div([
    html.Div([
        html.Div([], className="one columns"),
        html.Div([
            html.H1('COVID-19 Data Explorer'),

            html.Nav([
                dcc.Location(id='url', refresh=False),
                html.Div([
                    dcc.Link('Home', href='/'),
                    dcc.Link(' ● ', href=''),
                    dcc.Link('Mobility Report', href='/mobility'),
                    dcc.Link(' ● ', href=''),
                    dcc.Link('World Trends', href='/world'),
                    dcc.Link(' ● ', href=''),
                    dcc.Link('Vaccine Candidate', href='/candidate'),
                ], className="row"),
            ]),

            html.Br(),

            html.Div([
                html.Div(id='page-content', children=[])
            ]),

        ], className="ten columns"),

        html.Div([], className="one columns"),

    ], className="row"),

    # Footer Area
    html.Br(),
    html.Div(children=[
        html.P(['Source : '
                   , html.A("Our World in Data", href="https://ourworldindata.org/")
                   , ", ",
                html.A("Graduate Institute", href="https://www.knowledgeportalia.org/covid19-vaccine-arrangements")]),
        html.P(['This Data Explorer is '
                   , html.A("Open Source", href="https://github.com/sagelga/covid-vaccine")
                   , '. Buy us a ☕ by '
                   , html.A('Donate via Crypto',
                            href='https://commerce.coinbase.com/checkout/aed305a0-d6ae-4d98-b993-b1e85e0a99f6')
                   , ' or '
                   , html.A('via PayPal',
                            href='https://paypal.me/son9912')
                ]),

        html.P(['Created with ❤️ by ', html.A("@sagelga", href="https://github.com/sagelga/covid-vaccine")]),
    ], className="footer", style={'background-color': '#e5ecf6', 'text-align': 'center'}),

])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')]
              )
def display_page(pathname):
    if pathname == '/world':
        return world.layout
    if pathname == '/candidate':
        return candidate.layout
    if pathname == '/mobility':
        return mobility.layout

    # If URL does not match any page, returns to home layout
    return home.layout


if __name__ == '__main__':
    app.run_server(debug=True)
