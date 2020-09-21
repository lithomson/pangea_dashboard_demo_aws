import sys

import aws_lambda_wsgi
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

sys.path.append('..')
from dash_app.pages import about, sampling_numbers, sampling_period
from dash_app.app import app

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

CHECKBOX_STYLE = {
    'fontSize': "14px"
}

sidebar = html.Div(
    [
        html.H2("Dashboard Demo", className="display-5"),
        html.Hr(),
        html.P("Navigation", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", id="home-link"),
                dbc.NavLink("Sampling Numbers", href="/sampling-numbers", id="sampling-numbers-link"),
                dbc.NavLink("Sampling Period", href="/sampling-period", id="sampling-period-link"),
                dbc.NavLink("About", href="/about", id="about-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    content
])

server = app.server

index_layout = html.Div([
    html.H5('Welcome to the PANGEA Dashboard Demo!'),
    html.Br(),
    html.P('I hope you are having a lovely day :)')
])


@app.callback(
    Output('page-content', 'children'),
    [Input(component_id='url', component_property='pathname')]
)
def display_page(pathname):
    pathname = pathname.replace('/Prod/dash_app', '/') if pathname else pathname
    if pathname == '/':
        return index_layout
    elif pathname == "/sampling-numbers":
        return sampling_numbers.layout
    elif pathname == "/sampling-period":
        return sampling_period.layout
    elif pathname == "/about":
        return about.layout
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


def lambda_handler(event, context):
    return aws_lambda_wsgi.response(server, event, context)
