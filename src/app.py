import dash
import dash_bootstrap_components as dbc
import pandas as pd

from dash.dependencies import Input, Output
from dash import dcc, html

df = pd.read_csv('../data/processed_data.csv')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

server = app.server
# =========================
# UI
# =========================
# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "13rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


sidebar = html.Div([
        html.H2("Filter"),
        html.Hr(),
        dbc.Nav(
            [dcc.Dropdown(id='country_select',
                        options=[{'label': i, 'value': i} for i in df['Country'].unique()],
                        multi=False,
                        placeholder="Select countries"
                        )
            ],
            vertical=True,
            pills=True
        )
    ]
    , style=SIDEBAR_STYLE)

content = html.Div([
        dbc.Row(html.H2("Title")),
        dbc.Row([
            dbc.Col(html.Div(id='output-tab1'), width=6),
            dbc.Col(html.Div([
                        html.H4("2nd col"),
                        html.Hr()
                        ]
                    ), width=6)
        ])
])


# layout = html.Div([sidebar,content])
layout = html.Div([
    dbc.Row([
        dbc.Col(sidebar, width=2),
        dbc.Col(content, width=10)
    ])
])
app.layout = layout
# =========================
# Server
# =========================


@app.callback(Output('output-tab1', 'children'),
            [
            Input('country_select', 'value')])
def update_output_tab1(country):
    if country == []:
        return html.Div('Please select a continent and a country.')
    else:
        filtered_df = df[df['Country'] == country]
        return dcc.Graph(
            figure={
                'data': [
                    {'x': filtered_df['Country'], 'y': filtered_df['Cost of Living Index'], 'type': 'bar', 'name': 'Cost of Living Index'},
                    {'x': filtered_df['Country'], 'y': filtered_df['Rent Index'], 'type': 'bar', 'name': 'Rent Index'}
                ],
                'layout': {
                    'title': 'Cost of Living Index and Rent Index by Selected Country',
                    'xaxis': {'title': 'Country'},
                    'yaxis': {'title': 'Value'},
                    'barmode': 'group'
                }
            }
        )

if __name__ == '__main__':
    app.run_server(debug=True)
