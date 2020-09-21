import sys
from os.path import join, dirname, abspath

import aws_lambda_wsgi
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

sys.path.append('..')
from dash_app import about, index, sampling_period

CSV = join(dirname(abspath(__file__)), 'assets', 'pangea_dashboard_demo.csv')
df = pd.read_csv(CSV)

COHORT_CATEGORIES = df['main_cohort_id'].unique()
SEX_CATEGORIES = df['sex'].unique()

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

app = dash.Dash(__name__, compress=False, requests_pathname_prefix='/Prod/',
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                title="PANGEA Dashboard Demo")

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

df_sampling_numbers = pd.read_csv(CSV)
df_sampling_numbers = df_sampling_numbers[['geo_country', 'sex', 'main_cohort_id']]
df_sampling_numbers = df_sampling_numbers.groupby(['geo_country', 'sex', 'main_cohort_id']).size().reset_index()
df_sampling_numbers.rename(columns={0: 'count'}, inplace=True)

sampling_numbers_layout = [
    dcc.Graph(id='sampling-numbers-graph'),

    html.Div([
        html.H6('Cohort'),
        dbc.Checklist(
            id='mcohort-checkbox',
            options=[{'label': i, 'value': i} for i in COHORT_CATEGORIES],
            value=COHORT_CATEGORIES,
            inline=True
        ),
        html.Br(),
        html.H6('Sex'),
        dbc.Checklist(
            id='sex-checkbox',
            options=[{'label': i, 'value': i} for i in SEX_CATEGORIES],
            value=SEX_CATEGORIES,
            inline=True,
        )]),
    html.Div(id='sampling-numbers-content'),
]


@app.callback(
    Output('sampling-numbers-graph', 'figure'),
    [Input('mcohort-checkbox', 'value'),
     Input('sex-checkbox', 'value')])
def update_sampling_numbers_graph(mcohort_checkbox, sex_checkbox):
    dff = df_sampling_numbers[df_sampling_numbers['main_cohort_id'].isin(mcohort_checkbox) &
                              df_sampling_numbers['sex'].isin(sex_checkbox)]

    fig = px.histogram(dff, x="geo_country", y="count", color="geo_country", barmode="stack")
    fig.update_layout(
        title={
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title='Country',
        yaxis_title='Number of samples',
        legend_title='Country',
        hovermode="x")
    fig.update_traces(hovertemplate=None)
    return fig


@app.callback(
    Output('page-content', 'children'),
    [Input(component_id='url', component_property='pathname')]
)
def display_page(pathname):
    pathname = pathname.replace('/Prod/dash_app', '/') if pathname else pathname
    if pathname == '/':
        return index.layout
    elif pathname == "/sampling-numbers":
        return sampling_numbers_layout
    elif pathname == "/sampling-period":
        return sampling_period.layout
    elif pathname == "/about":
        return about.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


def lambda_handler(event, context):
    return aws_lambda_wsgi.response(server, event, context)
