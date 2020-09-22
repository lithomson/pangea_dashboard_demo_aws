import sys
from os.path import join, dirname, abspath

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

sys.path.append('..')
from app import app  # noqa: E402

CSV = join(dirname(abspath(__file__)), 'assets', 'pangea_dashboard_demo.csv')

df = pd.read_csv(CSV)
df = df[['geo_country', 'sex', 'main_cohort_id']]
df = df.groupby(['geo_country', 'sex', 'main_cohort_id']).size().reset_index()
df.rename(columns={0: 'count'}, inplace=True)

COHORT_CATEGORIES = df['main_cohort_id'].unique()
SEX_CATEGORIES = df['sex'].unique()

CHECKBOX_STYLE = {
    'fontSize': "14px"
}

layout = [
    dcc.Graph(id='my-graph'),

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
    Output('my-graph', 'figure'),
    [Input('mcohort-checkbox', 'value'),
     Input('sex-checkbox', 'value')])
def update_graph(mcohort_checkbox, sex_checkbox):
    dff = df[df['main_cohort_id'].isin(mcohort_checkbox) &
             df['sex'].isin(sex_checkbox)]

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
