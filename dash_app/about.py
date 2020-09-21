import dash_html_components as html

layout = html.Div([
    html.P('Created and maintained by Laura Thomson.'),
    html.Div([html.A("GitHub Repo", href='https://github.com/lithomson/pangea_dashboard_demo', target="_blank")]),
    html.Div(id='about-content'),
])
