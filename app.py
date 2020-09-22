import dash
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, compress=False, requests_pathname_prefix='/Prod/',
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True,
                title="PANGEA Dashboard Demo")
