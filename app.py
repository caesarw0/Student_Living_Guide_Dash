import dash
import dash_bootstrap_components as dbc
import pandas as pd

from ui import layout
from server import register_callbacks

df = pd.read_csv('data/processed_data.csv')


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = layout

register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
